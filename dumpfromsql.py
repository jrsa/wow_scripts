import mysql.connector
from mysql.connector import errorcode

"""
this script looks at a MySQL database containing DBC data
and saves a dbc file with that data
"""

TABLE_NAME = 'dbc_map'

config = {
    'user': 'root',
    'password': '',
    'host': '127.0.0.1',
    'database': 'pfg_dbc_localtest'
}

try:
    cnx = mysql.connector.connect(**config)

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print('Something is wrong with your user name or password')
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)

else:
    cur = cnx.cursor()
    cur.execute("select * from {table};".format(table=TABLE_NAME))
    for row in cur.fetchall():
        print(row)

finally:
    if cur:
        cur.close()
    if cnx:
        cnx.close()
