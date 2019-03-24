import MySQLdb

def connect():
    # Open database connection
    # Arguments are: host, username, password, database name
    db = MySQLdb.connect("localhost","root","root","test_stankless" )

    # prepare a cursor object using cursor() method
    cursor = db.cursor()

    # execute SQL query using execute() method.
    cursor.execute("SELECT VERSION()")

    # Fetch a single row using fetchone() method.
    data = cursor.fetchone()
    print("Database version : %s " % data)

    # disconnect from server
    db.close()