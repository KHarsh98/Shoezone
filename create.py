import sqlite3

def convertToBinaryData(filename):
    #Convert digital data to binary format
    with open(filename, 'rb') as file:
        blobData = file.read()
    return blobData

def insertBLOB(prodID, frontImage, backImage, price, stock, Ptype, desc, brand, gender, prodName):
    try:
        sqliteConnection = sqlite3.connect('sqlite.db')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")
        sqlite_insert_blob_query = """ INSERT INTO 'products'
                                  VALUES (?, ?, ?, ? ,?, ?, ?, ?, ? ,?)"""

        frontPhoto = convertToBinaryData(frontImage)
        backPhoto = convertToBinaryData(backImage)
        
        # Convert data into tuple format
        data_tuple = (prodID, frontPhoto, backPhoto, price, stock, Ptype, desc, brand, gender, prodName)
        cursor.execute(sqlite_insert_blob_query, data_tuple)
        sqliteConnection.commit()
        print("Image inserted successfully as a BLOB into a table")
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to insert blob data into sqlite table", error)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()
            print("the sqlite connection is closed")

def dropTable():
    con = sqlite3.connect('sqlite.db')
    con.execute('drop table products;')
    con.commit()
    con.close()

def createTable():
    con = sqlite3.connect('sqlite.db')
    con.execute("CREATE TABLE IF NOT EXISTS products (prodID TEXT PRIMARY KEY, prodName TEXT, price TEXT, stock NUMBER, color TEXT, altColor TEXT, photo BLOB)")
    con.commit()
    con.close()

insertBLOB(1,'/home/jarvis/sample/static/images/Nike-Run.jpg','/home/jarvis/sample/static/images/Nike-Run1.jpg',  999, 10, 'sports', 'Stupid Description', 'Nike', 'men', 'Nike Run')
