from irisreader.data.mg2k_centroids import LAMBDA_MIN, LAMBDA_MAX, assign_mg2k_centroids
from irisreader import obs_iterator
from sqlalchemy import create_engine
import pandas as pd
import sqlalchemy
import numpy as np
import datetime

VM_DB_adress = "postgresql+psycopg2://postgres:lukas4president@213.136.68.142/IRIS" #add connection in order to work
startdate = "2014,1,1" #startdate included
enddate = "2014,1,2" #enddate not included

def drop_tables(con):
    #Deleting all tabels
    con.execute('''
        DROP TABLE "ypixels", "centroid_count", "observation"
        ''')
    print("Tables ypixels, centroid_count and observation were droped")

def create_tables(con):
    # Create table observation
    con.execute('''
        CREATE TABLE observation (
        id_observation smallserial,
        observation varchar(37) 
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

    # Create table centroid_count
    con.execute('''
        CREATE TABLE ypixels (
        id_ypixels serial,
        id_observation smallint,
        step smallint,
        ypixels int [],
        image varchar(100) )
        ''')
    # Add primary key and foreign key
    con.execute('ALTER TABLE "ypixels" ADD PRIMARY KEY ("id_ypixels")')
    con.execute('ALTER TABLE "ypixels" ADD FOREIGN KEY ("id_observation") REFERENCES "observation"("id_observation")')
    print('Database relations were defined')

def fill_DB(startdate, enddate, con): #date in Format 2014,12,31
    '''
    date in Format 2014,12,31
    enddate is not included
    '''
    starttime = datetime.datetime.now()

    start = datetime.datetime(startdate)
    end = datetime.datetime(enddate) #last day not included
    daterange = [start + datetime.timedelta(days=x) for x in range(0, (end-start).days)]

    highest_entry = 0 #for correct id_observation

    for date in daterange:
        obsit = obs_iterator("/data2/iris/20{}".format(date.strftime("%y/%m/%d")), read_v4=False) # iterate through dates
        print("starting:", date.strftime("%y/%m/%d"))
        #create empty variables for table centroid_count
        col_names =  ['id_observation', 'step', 'centroid', 'count']
        centroid_count_oneday  = pd.DataFrame(columns = col_names) #panda DF for table centroid_count
        n_obs = 0

        #create empty variables for table observation
        obs_path = [] #list that will append the observation path


        #create empty variables for table ypixels
        col_names =  ['id_observation', 'step', 'ypixels', 'image']
        ypixels_oneday  = pd.DataFrame(columns = col_names)



        for obs in obsit: #iterate through each observation
            if obs.raster.has_line("Mg II k"):
                n_obs +=1 #used to for indexing observation
                obs_path.append(obs.path) # appends list with all observations path
                raster = obs.raster("Mg II k")
                steps = raster.n_steps

                for step in range( steps ): #iterate through each step 
                    img = raster.get_interpolated_image_step( step, LAMBDA_MIN, LAMBDA_MAX, n_breaks=216 )
                    centroids = assign_mg2k_centroids( img ) #cetroid is a np.array which lists the centroids of each step

                    (unique, counts) = np.unique(np.array(centroids), return_counts=True) #two lists with the frequency and count

                    centroid_step_data = {'id_observation': n_obs, 'step': step, 'centroid': unique, 'count': counts}
                    centroid_step = pd.DataFrame(centroid_step_data)
                    centroid_count_oneday = centroid_count_oneday.append(centroid_step) #append each step

                    ypixels_step_data = {'id_observation': n_obs, 'step': step, 'ypixels': [centroids]}
                    ypixels_step = pd.DataFrame(ypixels_step_data)
                    ypixels_oneday = ypixels_oneday.append(ypixels_step)#append each step
                    
        
        if n_obs > 0:
            observation = pd.DataFrame({'observation': obs_path}) #creates observation panda DF to write to DB 

            #get the las id_observation and add 1
            highest_entry = con.execute('SELECT "id_observation" FROM "observation" ORDER BY "id_observation" DESC LIMIT 1', con) #last obdervation id
            try: highest_entry = [row[0] for row in highest_entry][0] #new id for observation
            except: highest_entry = 0 #new id for observation

            #add to dataframe for correct id_observation
            centroid_count_oneday['id_observation'] = centroid_count_oneday['id_observation'] + highest_entry
            ypixels_oneday['id_observation'] = ypixels_oneday['id_observation'] + highest_entry


            #observation to DB
            observation['observation'] = observation['observation'].str.slice(start=12)
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

##start code

#check if database exists
connection = None
try:
    connection = psycopg2.connect("VM_DB_adress")
    print("connected to Database")

except:
    print('Database does not exist or is offline.')

if connection is None:
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
fill_DB(startdate, enddate, con)


# close the connection to database
sqlalchemy.engine.Connection.close(con)