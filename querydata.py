import mysql.connector
from address import hex_to_TRON_ADDR
import binascii


# Replace with your connection details
host = "localhost"
user = "root"
password = "hell0w0rld."
database = "tron"



def queryAddress(address):
    connection = None
    newAddr = address
    try:
        connection = mysql.connector.connect(host=host, user=user, password=password, database=database)
        cursor = connection.cursor()
       
        tableName = "t_"+address[-1:]  
        # Prepare data for insertion
        #data = ("GGAzd", "mm", "BF2A64E45D6B415FA894A1975F090B008854CCCD394B4FFBACB99BD027E12764")
        querySql = "select * from {tableName} where suffix like  BINARY '%{suffix3}' order by levenshtein(CONCAT(REVERSE(suffix),prefix),'{allfix}') limit 1".format(
            tableName=tableName,suffix3=address[-3:],allfix=address[-5:][::-1]+address[1:3])
        # Insert data
        cursor.execute(querySql)

        # Fetch all rows
        rows = cursor.fetchall()

        # Process the result
        for row in rows:
            suffix = row[0]
            prefix = row[1]
            prikey = binascii.hexlify( row[2]).decode('utf-8')

            print(f"Suffix: {suffix}, Prefix: {prefix}, Prikey: {prikey}")
            newAddr = hex_to_TRON_ADDR(prikey)
            break
        
        cursor.execute("INSERT IGNORE INTO addr_monit (addr)VALUES ('{newAddr}');".format(newAddr=newAddr))

        return newAddr

    except  mysql.connector.Error as err:
        print(f"Error: {err}")

        return newAddr
    finally:
        if connection:
            connection.close()
            cursor.close()
