from flask import Flask, render_template, request
import sqlite3

def writeTofile(data, filename):
    # Convert binary data to proper format and write it on Hard Disk
    with open(filename, 'wb') as file:
        file.write(data)
    print("Stored blob data into: ", filename, "\n")

def readBlobData(prodID):
    try:
        sqliteConnection = sqlite3.connect('sqlite.db')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        sql_fetch_blob_query = "SELECT * from products where productid = (?)"
        cursor.execute(sql_fetch_blob_query, (prodID,))
        record = cursor.fetchall()
        for row in record:
            name  = row[9]
            frontPhoto = row[1]
            backPhoto = row[2]
            print("Storing image on disk \n")
            photoPath = "/home/jarvis/sample/static/images/" + name + ".jpeg"
            writeTofile(frontPhoto, photoPath)
            photoPath = "/home/jarvis/sample/static/images/" + name + "1.jpeg"
            writeTofile(backPhoto, photoPath)

        cursor.close()
    except sqlite3.Error as error:
        print("Failed to read blob data from sqlite table", error)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()
            print("sqlite connection is closed")
            


app = Flask(__name__)
app.debug = True

@app.route("/<name>")
def index(name):
    conn = sqlite3.connect("sqlite.db")
    cursor = conn.execute("SELECT * FROM products ;")

    
    return render_template('index.html', cursor=cursor)

@app.route("/product/  <prodID>")
def product(prodID):
    print(prodID)
    print(prodID.strip())
    readBlobData(prodID.strip())
    conn = sqlite3.connect("sqlite.db")
    cursor = conn.execute("SELECT * FROM products where productid=(?)", (prodID,))    
  
    return render_template('product.html', cursor = cursor)

@app.route("/cart")
def cart():
    return render_template('cart.html')
    
@app.route("/shop")
def shop():
    return render_template('shop-cat.html')

@app.route("/home")
def home():
    return render_template('homepage.html')

@app.route("/shop/men/<category>")
def cat_men(category):
    conn = sqlite3.connect('sqlite.db')
    cursor = conn.execute("SELECT * FROM products where type=(?) AND gender ='men';", (category,))
    return render_template('index.html', cursor=cursor)
@app.route("/shop/women/<category>")
def cat_women(category):
    conn = sqlite3.connect('sqlite.db')
    cursor = conn.execute("SELECT * FROM products where type=(?) AND gender ='women';", (category,))
    return render_template('index.html', cursor=cursor)
