from urllib.parse import urlparse
import httplib2 as http
import json


# Looks up information associated with the barcode passed as argument
def barcode_lookup(barcode):
    headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
    }
    ch = http.Http()
    url = 'https://api.upcitemdb.com/prod/trial/lookup?upc={}'.format(barcode)
    lookup = urlparse(url)
    resp, content = ch.request(lookup.geturl(), 'GET', '', headers)
    data = json.loads(content)
    value = json.dumps(data)
    

    return value

# Returns macaroni
def macaroni():
    headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
    }
    ch = http.Http()
    lookup = urlparse('https://api.upcitemdb.com/prod/trial/lookup?upc=021000658947')
    resp, content = ch.request(lookup.geturl(), 'GET', '', headers)
    data = json.loads(content)
    value = json.dumps(data)
    

    return value