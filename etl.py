import configparser
import psycopg2
from sql_queries import copy_table_queries, insert_table_queries


def load_staging_tables(cur, conn):
    for query in copy_table_queries:
        cur.execute(query)
        conn.commit()


def insert_tables(cur, conn):
    for query in insert_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    print('1.connection established..')
    cur = conn.cursor()
    print('2.cursor created successfully')
    
    load_staging_tables(cur, conn)
    print('load data from s3 to staging tables')
    insert_tables(cur, conn)
    print('insert data from staging tables to redshift tables.')

    conn.close()
    print('close connection')


if __name__ == "__main__":
    main()