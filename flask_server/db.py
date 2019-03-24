import MySQLdb

def insert_barcode(title, barcode):
    # Open database connection
    # Arguments are: host, username, password, database name
    db = MySQLdb.connect("localhost","root","root","test_stankless" )

    # prepare a cursor object using cursor() method
    cursor = db.cursor()

    # execute SQL query using execute() method.
    cursor.execute("INSERT INTO barcodes (title, number, count) VALUES (\"{}\", \"{}\", 0);".format(title, barcode))

    # Fetch a single row using fetchone() method.
    data = cursor.fetchone()
    print("MySQL Response : %s " % data)

    # disconnect from server
    db.close()