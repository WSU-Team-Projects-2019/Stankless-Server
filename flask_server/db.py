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

# Delete the given barcode from the database
def remove_item(barcode):
    db = getDB()
    cursor = db.cursor()

    # build query
    query = 'DELETE FROM barcodes WHERE number = \"{}\"'.format(barcode)
    cursor.execute(query)
    db.commit()

    return "Item removed!"

# Add job to the database if there aren't already three
def insert_job(hours, mins):
    db = getDB()
    cursor = db.cursor()

    # check to see if the item already exists in the database
    query = "SELECT job_id FROM jobs WHERE hour = {} AND minute = {};".format(hours, mins)
    cursor.execute(query)
    # Fetch a single row and check if it is equal to None
    data = cursor.fetchone()
    if data != None: # If barcode already exists in the database
        return "This cleaning cycle is already scheduled!"

    # build query
    query = "INSERT INTO jobs (hour, minute) VALUES ({}, {});".format(hours, mins)
    cursor.execute(query)
    db.commit()

    return "Cleaning Job Scheduled"

# Remove job from the database
def remove_job(hours, mins):
    db = getDB()
    cursor = db.cursor()

    # build query
    query = 'DELETE FROM jobs WHERE hour = {} AND minute = {};'.format(hours, mins)
    cursor.execute(query)
    db.commit()

    return "Cleaning Job Removed"

# Get all jobs from the database
def get_jobs():
    db = getDB()
    cursor = db.cursor()
    query = "SELECT * FROM jobs;"
    cursor.execute(query)
    data = cursor.fetchall()
    return data

# Get database connection
def getDB():
    # Arguments are: host, username, password, database name
    return MySQLdb.connect("localhost","root","root","test_stankless" )