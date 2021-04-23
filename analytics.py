import configparser
import psycopg2
from sql_queries import analytic_queries


def get_results(cur, conn):
    """
    This function retrieves results for the analytic queries.
    Query1: Retrieves
    Query2: 
    Query3: 
    """
    for query in analytic_queries:
        cur.execute(query)
        results = cr.fetchall()
        
        for row in results:
            print(row)


def main():
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    print('1.connection established..')
    cur = conn.cursor()
    print('2.cursor created successfully')
    
    get_results(cur, conn)

    conn.close()
    print('close connection')


if __name__ == "__main__":
    main()