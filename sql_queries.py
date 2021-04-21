import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

# DROP TABLES

staging_events_table_drop = ""
staging_songs_table_drop = ""
songplay_table_drop = "DROP TABLE IF EXISTS songplays;"
user_table_drop = "DROP TABLE IF EXISTS users;"
song_table_drop = "DROP TABLE IF EXISTS songs;"
artist_table_drop = "DROP TABLE IF EXISTS artists;"
time_table_drop = "DROP TABLE IF EXISTS time;"

# CREATE TABLES

staging_events_table_create= ("""
""")

staging_songs_table_create = ("""
""")


songplay_table_create = ("""
CREATE TABLE IF NOT EXISTS songplays
(
    songplay_id INTEGER NOT NULL IDENTITY(0,1)
    ,start_time TIMESTAMP
    ,user_id INT NOT NULL
    ,level VARCHAR(20)
    ,song_id VARCHAR(800) NOT NULL
    ,artist_id VARCHAR(800) NOT NULL
    ,session_id INT NOT NULL
    ,location VARCHAR(800)
    ,user_agent VARCHAR(800)
    ,PRIMARY KEY(songplay_id)
    ,FOREIGN KEY(start_time) REFERENCES time(start_time)
    ,FOREIGN KEY(user_id) REFERENCES users(user_id)
    ,FOREIGN KEY(song_id) REFERENCES songs(song_id)
    ,FOREIGN KEY(artist_id) REFERENCES artists(artist_id)
)
distkey(songplay_id);
""")

user_table_create = ("""
CREATE TABLE IF NOT EXISTS users
(
    user_id INT NOT NULL
    ,first_name VARCHAR(256) NOT NULL 
    ,last_name VARCHAR(256) NOT NULL
    ,gender VARCHAR(256)
    ,level VARCHAR(20)
    ,PRIMARY KEY(user_id)
)
""")

song_table_create = ("""
CREATE TABLE IF NOT EXISTS songs
(
    song_id VARCHAR(256)
    ,title VARCHAR(800) NOT NULL
    ,artist_id VARCHAR(800) NOT NULL
    ,year INT
    ,duration DECIMAL(8,5) NOT NULL
    ,PRIMARY KEY(song_id)
)
""")

artist_table_create = ("""
CREATE TABLE IF NOT EXISTS artists
(
    artist_id VARCHAR(800) NOT NULL
    ,name text NOT NULL
    ,location text 
    ,lattitude DECIMAL(2,6) 
    ,longitude DECIMAL(2,6)
    ,PRIMARY KEY(artist_id)
)
""")

time_table_create = ("""
CREATE TABLE IF NOT EXISTS time
(
    start_time TIMESTAMP
    ,hour INT
    ,day INT
    ,week INT
    ,month INT
    ,year INT
    ,weekday VARCHAR(100)
    ,PRIMARY KEY(start_time)
)
""")

# STAGING TABLES

staging_events_copy = ("""
""").format()

staging_songs_copy = ("""
""").format()

# FINAL TABLES

songplay_table_insert = ("""
""")

user_table_insert = ("""
""")

song_table_insert = ("""
""")

artist_table_insert = ("""
""")

time_table_insert = ("""
""")

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]
