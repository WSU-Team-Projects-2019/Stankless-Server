from flask import Flask
from flask import request
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
@app.route('/query')
def query_test():
	message = request.args.get('msg') # If the key does not exists, returns None
	
	return '''<h1>Your message is: {}</h1>'''.format(message)
