from irisreader.data.mg2k_centroids import LAMBDA_MIN, LAMBDA_MAX, assign_mg2k_centroids
from irisreader import obs_iterator
from sqlalchemy import create_engine
import pandas as pd
import sqlalchemy
import numpy as np
import datetime
import psycopg2

VM_DB_adress = "postgresql+psycopg2://astronaut:lukas4president@147.86.8.71:5432/IRIS" #add connection in order to work
startdate = datetime.datetime(2014,1,1) #startdate included
enddate = datetime.datetime(2015,1,1) #enddate not included

def drop_tables(con):
    #Deleting all tabels
    con.execute('''
        DROP TABLE "ypixels", "centroid_count";
        DROP TABLE"observation", "images"
        ''')
    print("Tables ypixels, centroid_count, images and observation were droped")

def create_tables(con):
    con.execute('''
        CREATE TABLE observation (
        id_observation smallserial,
        observation varchar(26),
        x_pixels smallint,
        y_pixels smallint,
        n_steps smallint,
        hek_url varchar(200)
        )
        ''')
    # Add primary key
    con.execute('ALTER TABLE "observation" ADD PRIMARY KEY ("id_observation")')


    # Create table centroid_count
    con.execute('''
        CREATE TABLE centroid_count (
        id_centroid_count serial,
        id_observation smallint,
        step smallint,
        centroid smallint,
        count smallint )
        ''')
    # Add primary key and foreign key
    con.execute('ALTER TABLE "centroid_count" ADD PRIMARY KEY ("id_centroid_count")')
    con.execute('ALTER TABLE "centroid_count" ADD FOREIGN KEY ("id_observation") REFERENCES "observation"("id_observation")')


    # Create table images
    con.execute('''
        CREATE TABLE images (
        id_image serial,
        path varchar(75), 
        slit_pos smallint)
        ''')
    # Add primary key and foreign key
    con.execute('ALTER TABLE "images" ADD PRIMARY KEY ("id_image")')



    # Create table ypixels
    con.execute('''
        CREATE TABLE ypixels (
        id_ypixels serial,
        id_observation smallint,
        step smallint,
        ypixels int [],
        "1330" int,
        "1400" int,
        "2796" int,
        "2832" int)
        ''')
    # Add primary key and foreign key
    con.execute('ALTER TABLE "ypixels" ADD PRIMARY KEY ("id_ypixels")')
    con.execute('ALTER TABLE "ypixels" ADD FOREIGN KEY ("id_observation") REFERENCES "observation"("id_observation")')
    con.execute('ALTER TABLE "ypixels" ADD FOREIGN KEY ("1330") REFERENCES "images"("id_image")')
    con.execute('ALTER TABLE "ypixels" ADD FOREIGN KEY ("1400") REFERENCES "images"("id_image")')
    con.execute('ALTER TABLE "ypixels" ADD FOREIGN KEY ("2796") REFERENCES "images"("id_image")')
    con.execute('ALTER TABLE "ypixels" ADD FOREIGN KEY ("2832") REFERENCES "images"("id_image")')


    print('Database relations were defined')

def create_index():
    # Add index to centroid_count
    con.execute('''
    CREATE INDEX centroid_id_observation_idx
    ON centroid_count (centroid, id_observation);''')

    # Add index to ypixels
    con.execute('''
    CREATE INDEX id_observation_step_idx
    ON ypixels (id_observation, step);''')
    
    # Add index to images
    con.execute('''
    CREATE INDEX id_image_idx
    ON images (id_image);''')
    
    print("finished creating indexes")

def get_and_write_image(con):
    #read csv file
    col_names =  ['obs_id', 'line_info', 'step', 'slit_pos', 'xpixels', 'ypixels', 'date']
    sji_info=pd.read_csv("https://www.cs.technik.fhnw.ch/iris/sji_png/sji_info.csv", names = col_names)
    sji_info['id_image'] = [x+1 for x in range(len(sji_info))] #id 0 is reserved for "no filter"
    sji_info['step'] = sji_info['step'].astype(int)
    sji_info['slit_pos'] = sji_info['slit_pos'].round().astype(int)

    #create image df for further use
    images = sji_info[['obs_id', 'line_info', 'date', 'xpixels', 'ypixels', 'id_image']]
    images['line_info'] = images['line_info'].str.slice(start=-4)
    images['date'] = pd.to_datetime(images['date'])
    images = images.set_index('date')

    #construct table images
    sql_images = sji_info[['id_image', 'obs_id', 'step', 'line_info', 'slit_pos']]
    sql_images['path'] = (sji_info['obs_id'].astype(str) + "/" + sji_info['obs_id'].astype(str) + '_' + 
                          sji_info['line_info'].str.slice(start=-4) + '_' + sji_info['step'].astype(str) + '.jpg')

    #create and append row for an empty image
    no_image = {'id_image':0, 'path':'no_image'}
    sql_images = sql_images.append(no_image, ignore_index = True)
    
    #write to DB
    sql_images = sql_images[['id_image', 'path', 'slit_pos']]
    sql_images.to_sql('images', con, index=None, if_exists='append')
    
    return images

def fill_DB(startdate, enddate, images_obs, con): #date in Format 2014,12,31
    '''
    date in Format 2014,12,31
    enddate is not included
    '''
    starttime = datetime.datetime.now()
    daterange = [startdate + datetime.timedelta(days=x) for x in range(0, (enddate-startdate).days)]
    highest_entry = 0 #for correct id_observation

    for date in daterange:
        obsit = obs_iterator("/data2/iris/20{}".format(date.strftime("%y/%m/%d")), read_v4=False) # iterate through dates
        print("starting:", date.strftime("%y/%m/%d"))

        #create empty variables for table centroid_count
        col_names =  ['id_observation', 'step', 'centroid', 'count']
        centroid_count_oneday  = pd.DataFrame(columns = col_names) #panda DF for table centroid_count
        n_obs = 0

        #create empty lists for table observation
        obs_path = [] #list that will append the observation path
        obs_hek_url = []
        obs_x_pixels = []
        obs_y_pixels = []
        obs_n_steps = []



        #create empty variables for table ypixels
        col_names =  ['id_observation', 'step', 'ypixels', '1330', '1400', '2796', '2832']
        ypixels_oneday  = pd.DataFrame(columns = col_names)


        for obs in obsit: #iterate through each observation
            if obs.raster.has_line("Mg II k"):
                n_obs +=1 #used to for indexing observation
                raster = obs.raster("Mg II k")
                steps = raster.n_steps           
                time_obs = raster.get_timestamps() #get all timestams as a list

                #list for observation
                obs_n_steps.append(steps)
                obs_path.append(obs.full_obsid) # appends list with all observations path
                obs_hek_url.append(obs.get_hek_url(html=False))


                #get the information from the images and create a df for each line_info
                images_obs = images[images['obs_id'] == obs.full_obsid] #select the current observation
                images_obs = images_obs.sort_index()

                #x and ypixels for table observation
                obs_x_pixels.append(images_obs['xpixels'][1])
                obs_y_pixels.append(images_obs['ypixels'][1])

                #dataframes for each line info
                images_obs = images_obs[['line_info', 'id_image']]
                images_obs_1330 = images_obs[images_obs['line_info'] == '1330']
                images_obs_1400 = images_obs[images_obs['line_info'] == '1400']
                images_obs_2796 = images_obs[images_obs['line_info'] == '2796']
                images_obs_2832 = images_obs[images_obs['line_info'] == '2832']




                for step in range( steps ): #iterate through each step 
                    img = raster.get_interpolated_image_step( step, LAMBDA_MIN, LAMBDA_MAX, n_breaks=216 )
                    centroids = assign_mg2k_centroids( img ) #cetroid is a np.array which lists the centroids of each step
                    timestamp = pd.Timestamp(time_obs[step], unit='s') 

                    (unique, counts) = np.unique(np.array(centroids), return_counts=True) #two lists with the frequency and count

                    centroid_step_data = {'id_observation': n_obs, 'step': step, 'centroid': unique, 'count': counts}
                    centroid_step = pd.DataFrame(centroid_step_data)
                    centroid_count_oneday = centroid_count_oneday.append(centroid_step) #append each step

                    if len(images_obs_1330) > 0:
                        row = images_obs_1330.index.get_loc(timestamp, method='nearest')
                        image_1330 = images_obs_1330.iloc[row]['id_image']
                    else: 
                        image_1330 = 0

                    if len(images_obs_1400) > 0:
                        row = images_obs_1400.index.get_loc(timestamp, method='nearest')
                        image_1400 = images_obs_1400.iloc[row]['id_image']
                    else: 
                        image_1400 = 0

                    if len(images_obs_2796) > 0:
                        row = images_obs_2796.index.get_loc(timestamp, method='nearest')
                        image_2796 = images_obs_2796.iloc[row]['id_image']
                    else: 
                        image_2796 = 0

                    if len(images_obs_2832) > 0:
                        row = images_obs_2832.index.get_loc(timestamp, method='nearest')
                        image_2832 = images_obs.iloc[row]['id_image']
                    else: 
                        image_2832 = 0


                    ypixels_step_data = {'id_observation': n_obs, 'step': step, 'ypixels': [centroids],
                                        '1330': image_1330, '1400': image_1400, '2796': image_2796, '2832': image_2832}
                    ypixels_step = pd.DataFrame(ypixels_step_data)
                    ypixels_oneday = ypixels_oneday.append(ypixels_step)#append each step


        if n_obs > 0:
            observation = pd.DataFrame({'observation': obs_path, 'hek_url': obs_hek_url, 'x_pixels': obs_x_pixels,
                                       'y_pixels': obs_y_pixels, 'n_steps':obs_n_steps}) #creates observation panda DF to write to DB 

            #get the last id_observation and add 1
            highest_entry = con.execute('SELECT "id_observation" FROM "observation" ORDER BY "id_observation" DESC LIMIT 1', con) #last obdervation id
            try: highest_entry = [row[0] for row in highest_entry][0] #new id for observation
            except: highest_entry = 0 #new id for observation

            #add to dataframe for correct id_observation
            centroid_count_oneday['id_observation'] = centroid_count_oneday['id_observation'] + highest_entry
            ypixels_oneday['id_observation'] = ypixels_oneday['id_observation'] + highest_entry


            #observation to DB
            observation['observation'] = observation['observation']
            observation.to_sql('observation', con, index=False, if_exists='append')

            #centroid_count to DB
            centroid_count_oneday.to_sql('centroid_count', con, index=False, if_exists='append')

            #ypixels to DB
            ypixels_oneday['ypixels'] = ypixels_oneday['ypixels'].apply(lambda x: x.tolist()) #psycopg2 can't handle np.ndarry 
            ypixels_oneday.to_sql('ypixels', con, index=False, if_exists='append')

        else: 
            print("NO observations in directory on {}".format(date.strftime("%y/%m/%d")))

    endtime = datetime.datetime.now()
    runtime = endtime -  starttime
    print("Runtime to fill DB: {} hours".format(runtime.total_seconds()/3600))



#check if database exists
con = None
try:
    engine = create_engine(VM_DB_adress)
    con = engine.connect()
    print("connected to Database")

except:
    print('Database does not exist or is offline.')
       
    if input("Do you want to try to create the Database iris? (y/n)") == ("y"):
        try: 
            #create Database called iris with the role postgres
            engine = create_engine(VM_DB_adress[:-5]) #slice -5 becaue iris is not yet created
            con = engine.connect()
            con.execute("commit")
            con.execute("CREATE DATABASE iris")
            con.close()
            print("Database was created.")
        except: 
            print("error while trying to create the Database")
            exit()
    else:
        exit()

#create engine for DB
engine = create_engine(VM_DB_adress)
con = engine.connect()

if input('''type "drop" to drop tabels ypixels, cetroid_count and observation and after recreate them''') == ("drop"):
    drop_tables(con)


try: 
    con.execute('''SELECT "id_observation" FROM "observation" LIMIT 1;
        SELECT "id_observation" FROM "centroid_count" LIMIT 1;
        SELECT "id_observation" FROM "ypixels" LIMIT 1;
        ''', con) #to check it Tabels exist
except: 
    create_tables(con)
    print("tables were created")


print("starting to extract data and write into database")

images = get_and_write_image(con)
print("wrote images to DB")
fill_DB(startdate, enddate, images, con)
create_index()


# close the connection to database
sqlalchemy.engine.Connection.close(con)