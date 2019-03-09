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
    #value = json.dumps(data)

    if resp['status'] == "200":
        title = data['items'][0]['title']
        barcode = data['items'][0]['ean']
        return {"response": resp['status'], "barcode" : barcode, "title" : title}

    #print("\n\nTitle is: {}\nBarcode: is {}\n\n".format(title, barcode))
    

    return {"response": "Barcode not found!"}

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
    #value = json.dumps(data)

    title = data['items'][0]['title']
    barcode = data['items'][0]['ean']

    #print("\n\nTitle is: {}\nBarcode: is {}\n\n".format(title, barcode))
    

    return {"response" : resp['status'], "barcode" : barcode, "title" : title}