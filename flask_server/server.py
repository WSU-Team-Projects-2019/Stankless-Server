from flask import Flask
from flask import request
import MySQLdb
import json

import barcode
import db


app = Flask(__name__)

# Application routes determine the functions to call when the user tries to access a particular URL
@app.route('/')
def server_init():
	return 'You have reached the home of the STANKLESS SERVER!'

@app.route('/weight')
def weight():
	return 'TrashCAN weight'

# Returns list of items in the data base
@app.route('/grocerylist')
def grocery_list():
    codes = db.get_barcodes()

    # Start of dictionary
    items = []
    for item in codes:
        items.append({"title" : item[1], "barcode" : item[2], "count" : item[3]})
    return json.dumps(items)


# Returns status of trash can
@app.route('/get-can-status')
def can_status():
    status = db.get_can_status()[0]

    json_status = {"lid_status" : status[0], "fan_status" : status[1], "led_status" : status[2], "bulb_status" : status[3]}
    return json.dumps(json_status)

# Test simple query
@app.route('/query-test')
def query_test():
	message = request.args.get('msg') # If the key does not exists, returns None
	
	return '''<h1>Your message is: {}</h1>'''.format(message)

# Look up barcode
@app.route('/barcode-lookup')
def barcode_query():
    message = request.args.get('upc') # If the key does not exists, returns None
    upc_req = barcode.barcode_lookup(message)
    if upc_req['response'] == "200":
        db.insert_barcode(upc_req['title'], upc_req['barcode'])
        return '''Item Name: {} EAN: {} Response is: {}'''.format(upc_req['title'], upc_req['barcode'], upc_req['response'])
    return '''Barcode not found!'''

# Update the can status
@app.route('/update-status')
def update_status():
    # Get all keys from arguments in the URL
    lid = request.args.get('lid') # If the key does not exists, returns None
    fan = request.args.get('fan')
    led = request.args.get('led')
    bulb = request.args.get('bulb')

    # Start building query
    query = 'UPDATE status SET'

    num_arguments = 0

    # Convert the keys to integers
    if lid == '1' or lid == '0':
        lid = int(lid)
        query += " lid_status = {},".format(lid)
        num_arguments += 1
    if fan == '1' or fan == '0':
        fan = int(fan)
        query += " fan_status = {},".format(fan)
        num_arguments += 1
    if led == '1' or led == '0':
        led = int(led)
        query += " led_status = {},".format(led)
        num_arguments += 1
    if bulb == '1' or bulb == '0':
        bulb = int(bulb)
        query += "bulb_status = {}".format(bulb)
    elif num_arguments > 0: # If we get to here and bulb status was not included and we have an argument, remove the last comma to insert properly
        query = query[:-1]
    
    if query != 'UPDATE status SET':
        query += " WHERE can_id = 'X';"
        db.update_can_status(query)
        
    return '''Can status updated!\n\nLid : {}\nFan: {}\nLED: {}\nBulb: {}'''.format(lid, fan, led, bulb)

# Delete a barcode from the database
@app.route('/delete-item')
def delete_item():
    # Get barcode to delete
    barcode = request.args.get('code')

    # If there is no barcode
    if barcode == None:
        return "No barcode supplied!"

    response = db.remove_item(barcode)

    return response

# Schedule a job
@app.route('/schedule-job')
def schedule_job():
    # These values should be changed to match UTC mobile app-side
    hours = request.args.get('hr')
    mins = request.args.get('min')

    # Make sure we have both minutes and hours
    if hours == None or mins == None:
        return "Invalid time entered"

    # Time will be given in military time
    if hours < 0 or hours >= 24 or mins < 0 or mins >= 60:
        return "Invalid time entered"

    response = db.insert_job(hours, mins)
    return response

# Remove a job
@app.route('/remove-job')
def remove_job():
    # These values should be changed to match UTC mobile app-side
    hours = request.args.get('hr')
    mins = request.args.get('min')

    # Make sure we have both minutes and hours
    if hours == None or mins == None:
        return "Invalid time entered"

    # Time will be given in military time
    if hours < 0 or hours >= 24 or mins < 0 or mins >= 60:
        return "Invalid time entered"

    response = db.remove_job(hours, mins)
    return response


# Test requesting barcode data from upcitemdb
@app.route('/barcode-test')
def barcode_test():
    mac = barcode.macaroni()
    return '''Response is: {}'''.format(mac['response'])

# Testing GET and POST requests
@app.route('/form-test', methods=['GET', 'POST']) #allow both GET and POST requests
def form_example():
    if request.method == 'POST':  #this block is only entered when the form is submitted
        name = request.form.get('name')
        age = request.form['age']

        return '''<h1>Hello, {}!</h1>
                  <h1>You are {} years old.</h1>'''.format(name, age)

    return '''<form method="POST">
                  Name: <input type="text" name="name"><br>
                  Age: <input type="text" name="age"><br>
                  <input type="submit" value="Submit"><br>
              </form>'''

# Test JSON requests.
# If testing with Postman make sure to select JSON (application/json) encoding, not just raw text
@app.route('/json-test', methods=['POST']) #GET requests will be blocked
def json_example():
    data = request.get_json() # Get the data passed in from POST request
    name = data['name']
    age = data['age']
    occupation = data['occupation']

    # Build response
    return '''
           Hello, {}!
           You are {} years old.
           You have a job as a {}.
           Look at how cool you are!
           '''.format(name, age, occupation)
