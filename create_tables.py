import configparser
import psycopg2
from sql_queries import create_table_queries, drop_table_queries


def drop_tables(cur, conn):
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()


def create_tables(cur, conn):
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    print('1.connection established..')
    cur = conn.cursor()
    print('2.cursor created successfully')

    drop_tables(cur, conn)
    print('3.drop existing tables')
    create_tables(cur, conn)
    print('4.create or recreate dropped tables')

    conn.close()
    print('5. close connection to redshift')


if __name__ == "__main__":
    main()