import MySQLdb

# Inserts item into the database with given title and barcode
# If the item already exists, the count of the item is increased
def insert_barcode(title, barcode):
    db = getDB()

    # prepare a cursor object using cursor() method
    cursor = db.cursor()

    # count to hold the number of items already in database
    count = 1

    # check to see if the item already exists in the database
    query = "SELECT item_id, count FROM barcodes WHERE number = {};".format(barcode)
    cursor.execute(query)
    # Fetch a single row and check if it is equal to None
    data = cursor.fetchone()
    query = "INSERT INTO barcodes (title, number, count) VALUES (\'{}\', \'{}\', {});".format(title, barcode, count)
    if data != None: # If barcode already exists in the database
        # print("Got to here! Values are ({}, {})".format(data[0], data[1]))
        item_id = data[0] # Store values from the returned tuple
        count = data[1] + 1
        query = "UPDATE barcodes SET count = {} WHERE item_id = {}".format(count, item_id)

    # execute SQL query using execute() method.
    cursor.execute(query)

    # Commit the changes
    db.commit()

    # disconnect from server
    db.close()

# Pulls down all of the barcodes from the database.
def get_barcodes():
    db = getDB()
    cursor = db.cursor()
    query = "SELECT * FROM barcodes;"
    cursor.execute(query)
    data = cursor.fetchall()
    return data

# pulls down trash can status and returns it as JSON string
def get_can_status():
    db = getDB()
    cursor = db.cursor()
    query = "SELECT lid_status, fan_status, led_status, bulb_status FROM status WHERE can_id = 'X'"
    cursor.execute(query)
    data = cursor.fetchall()

    return data

# updates the can status on the server with the given query
def update_can_status(query):
    db = getDB()
    cursor = db.cursor()
    cursor.execute(query)
    db.commit()
    data = cursor.fetchall()

    return data

# Get database connection
def getDB():
    # Arguments are: host, username, password, database name
    return MySQLdb.connect("localhost","root","root","test_stankless" )