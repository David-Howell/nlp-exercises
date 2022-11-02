import os
import numpy as np
import pandas as pd
import env


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~<  GET_DB_URL  >~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

def get_db_url(schema):
    '''
    Constructs the DataBase URL to Access Codeup MySQL DB
    
    Must have an env.py file to import
    '''
    user = env.username
    password = env.password
    host = env.host
    conn = f'mysql+pymysql://{user}:{password}@{host}/{schema}'
    return conn

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~<  GDB! (Get DataBase) >~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

def gdb(db_name, query):
    '''
    gdb(db_name, query):
    
        takes in    a (db_name) schema name from the codeup database ;dtype int
        and         a (query) to the MySQL server ;dtype int

        and         returns the query using pd.read_sql(query, url)
        having      created the url from my environment file
    '''
    url = get_db_url(db_name)
    return pd.read_sql(query, url)