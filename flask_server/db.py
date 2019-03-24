import MySQLdb

def insert_barcode(title, barcode):
    # Open database connection
    # Arguments are: host, username, password, database name
    db = MySQLdb.connect("localhost","root","root","test_stankless" )

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
        print("Got to here! Values are ({}, {})".format(data[0], data[1]))
        item_id = data[0] # Store values from the returned tuple
        count = data[1] + 1
        query = "UPDATE barcodes SET count = {} WHERE item_id = {}".format(count, item_id)

    # execute SQL query using execute() method.
    cursor.execute(query)

    # Commit the changes
    db.commit()

    # disconnect from server
    db.close()