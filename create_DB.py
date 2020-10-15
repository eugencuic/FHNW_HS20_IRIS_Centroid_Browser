import sqlalchemy
from sqlalchemy import create_engine

#create Database called iris with the role postgres
engine = create_engine('postgres://postgres@/postgres')
con = engine.connect()
con.execute("commit")
con.execute("create database iris")
con.close()

#connect to DB iris with the role postgres
engine = create_engine('postgres://postgres@/iris')
con = engine.connect()

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
    ypixels varchar(100),
    image varchar(100) )
    ''')
# Add primary key and foreign key
con.execute('ALTER TABLE "ypixels" ADD PRIMARY KEY ("id_ypixels")')
con.execute('ALTER TABLE "ypixels" ADD FOREIGN KEY ("id_observation") REFERENCES "observation"("id_observation")')

#close connection
sqlalchemy.engine.Connection.close(con)

print('Database "iris" was created and relations were defined')