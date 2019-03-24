from flask import Flask
from flask import request
import MySQLdb

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

@app.route('/grocerylist')
def grocery_list():
	return 'TrashCAN grocery list'

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
