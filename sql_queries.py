import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS staging_events;"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs;"
songplay_table_drop = "DROP TABLE IF EXISTS songplays;"
user_table_drop = "DROP TABLE IF EXISTS users;"
song_table_drop = "DROP TABLE IF EXISTS songs;"
artist_table_drop = "DROP TABLE IF EXISTS artists;"
time_table_drop = "DROP TABLE IF EXISTS time;"

# CREATE TABLES

staging_events_table_create= ("""
CREATE TABLE IF NOT EXISTS staging_events
(
    artist             VARCHAR(1200)
    ,auth              VARCHAR(256)
    ,firstName         VARCHAR(256)
    ,gender            CHAR(1)
    ,iteminSession     CHAR(1)
    ,lastName          VARCHAR(256)
    ,length            FLOAT
    ,level             VARCHAR(20)
    ,location          VARCHAR(800)
    ,method            VARCHAR(256)
    ,page              VARCHAR(256)
    ,registration      FLOAT
    ,session           INTEGER
    ,song              VARCHAR(800)
    ,status            INTEGER
    ,ts                TIMESTAMP
    ,userAgent         VARCHAR(800)
    ,userId            INTEGER   
);
""")


staging_songs_table_create = ("""
CREATE TABLE IF NOT EXISTS staging_songs
(
    num_songs          INTEGER
    ,artist_id         VARCHAR(800)
    ,artist_latitude   FLOAT
    ,artist_longitude  FLOAT
    ,artist_location   VARCHAR(800)
    ,artist_name       VARCHAR(800)
    ,song_id           VARCHAR(800)
    ,title             VARCHAR(800)
    ,duration          FLOAT
    ,year              INTEGER
);
""")


songplay_table_create = ("""
CREATE TABLE IF NOT EXISTS songplays
(
    songplay_id        INTEGER      IDENTITY(0,1)
    ,start_time        TIMESTAMP    NOT NULL
    ,user_id           INTEGER      NOT NULL
    ,level             VARCHAR(20)
    ,song_id           VARCHAR(800) NOT NULL
    ,artist_id         VARCHAR(800) NOT NULL
    ,session_id        INTEGER      NOT NULL
    ,location          VARCHAR(800)
    ,user_agent        VARCHAR(800)
    ,PRIMARY KEY(songplay_id)
    ,FOREIGN KEY(start_time) REFERENCES time(start_time)
    ,FOREIGN KEY(user_id) REFERENCES users(user_id)
    ,FOREIGN KEY(song_id) REFERENCES songs(song_id)
    ,FOREIGN KEY(artist_id) REFERENCES artists(artist_id)
)
DISTKEY(start_time)
SORTKEY(start_time);
""")

user_table_create = ("""
CREATE TABLE IF NOT EXISTS users
(
    user_id            INTEGER      NOT NULL
    ,first_name        VARCHAR(256) NOT NULL 
    ,last_name         VARCHAR(256) NOT NULL
    ,gender            VARCHAR(256)
    ,level             VARCHAR(20)
    ,PRIMARY KEY(user_id)
)
SORTKEY(user_id);
""")

song_table_create = ("""
CREATE TABLE IF NOT EXISTS songs
(
    song_id            VARCHAR(256)
    ,title             VARCHAR(800) NOT NULL
    ,artist_id         VARCHAR(800) NOT NULL
    ,year              INTEGER
    ,duration          FLOAT        NOT NULL
    ,PRIMARY KEY(song_id)
)
SORTKEY(song_id);
""")

artist_table_create = ("""
CREATE TABLE IF NOT EXISTS artists
(
    artist_id          VARCHAR(800) NOT NULL
    ,name              VARCHAR(800) NOT NULL
    ,location          VARCHAR(800)
    ,lattitude         FLOAT 
    ,longitude         FLOAT
    ,PRIMARY KEY(artist_id)
)
SORTKEY(artist_id);
""")

time_table_create = ("""
CREATE TABLE IF NOT EXISTS time
(
    start_time         TIMESTAMP NOT NULL
    ,hour              INTEGER
    ,day               INTEGER
    ,week              INTEGER
    ,month             INTEGER
    ,year              INTEGER
    ,weekday           VARCHAR(100)
    ,PRIMARY KEY(start_time)
)
DISTKEY(start_time)
SORTKEY(start_time);
""")

# STAGING TABLES

staging_events_copy = ("""
    COPY staging_events FROM {s3_event_data}
    CREDENTIALS 'aws_iam_role={arn_id}'
    REGION 'us-west-2'
    FORMAT AS JSON {event_file_path};
""").format(s3_event_data=config['S3']['LOG_DATA'],
            arn_id=config['IAM_ROLE']['ARN'],
            event_file_path=config['S3']['LOG_JSONPATH'])

staging_songs_copy = ("""
    COPY staging_songs FROM {s3_songs_data}
    CREDENTIALS 'aws_iam_role={arn_id}'
    REGION 'us-west-2'
    FORMAT AS JSON 'auto';
""").format(s3_songs_data=config['S3']['SONG_DATA'],
            arn_id=config['IAM_ROLE']['ARN'])

# FINAL TABLES

songplay_table_insert = ("""
INSERT INTO songplays
    (start_time, user_id, level, song_id, artist_id, session_id, location, user_agent)
SELECT (se.ts) AS start_time
    ,se.userId AS userid
    ,se.level
    ,ss.song_id
    ,ss.artist_id
    ,se.sessionId AS session_id
    ,se.location
    ,se.userAgent AS user_agent
FROM staging_events se
JOIN staging_songs ss 
ON (se.song = ss.title AND se.artist = ss.artist_name)
AND se.method = "NextSong";
""")

user_table_insert = ("""
INSERT INTO users
    (user_id, first_name, last_name, gender, level)
SELECT userId AS user_id
    ,title
    ,artist_id
    ,year
    ,duration
FROM staging_songs
WHERE artist_id IS NOT NULL;
""")

song_table_insert = ("""
INSERT INTO songs
    (song_id, title, artist_id, year, duration)
SELECT song_id
    ,title
    ,artist_id
    ,year
    ,duration
FROM staging_songs
WHERE song_id IS NOT NULL;
""")

artist_table_insert = ("""
INSERT INTO artists
    (artist_id, name, location, lattitude, longitude)
SELECT artist_id
    ,artist_name AS name
    ,artist_location AS location
    ,artist_latitude AS latitude
    ,artist_longitude AS longitude
FROM staging_songs
WHERE artist_id IS NOT NULL;
""")

time_table_insert = ("""
INSERT INTO time
    (start_time, hour, day, week, month, year, weekday)
SELECT start_time
    ,EXTRACT(hour FROM start_time) AS hour
    ,EXTRACT(day FROM start_time) AS day
    ,EXTRACT(week FROM start_time) AS week
    ,EXTRACT(month FROM start_time) AS month
    ,EXTRACT(year FROM start_time) AS year
    ,EXTRACT(weekday FROM start_time) AS weekday
FROM songplays;
""")

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, user_table_create, song_table_create, artist_table_create, time_table_create, songplay_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [user_table_insert, song_table_insert, artist_table_insert, time_table_insert,songplay_table_insert]
