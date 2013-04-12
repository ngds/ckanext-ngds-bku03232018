from nose.tools import ok_, eq_
import httplib

def test_datastore_expose_as_layer():
    
    print ">>>>>>>>>>>>>>>>> sending create layer POST >>>>>>>>>>>>>>>>"
    
    #headers, response = cat.http.request(featureType_url, "POST", definition.serialize(), headers)
    hostname = '127.0.0.1'
    port = 5000
    url = '/api/action/datastore_expose_as_layer'
    body =  '''{
    "resource_id": "e82f6b50-c7b4-42f9-ab24-0a1a2903557c",
    "col_geography": "shape",
    "col_longitude": "LONGITUDE", 
    "col_latitude": "LATITUDE"
    }'''
    
    method = "POST"
    headers = {"Content-type": "text/xml"}

    httpServ = httplib.HTTPConnection(hostname, port)
    httpServ.connect()
    httpServ.request(method, url, body, headers)
    
    print ">>>>>>>>>>>>>>>>> getting response >>>>>>>>>>>>>>>>"
    response = httpServ.getresponse()
    if response.status == httplib.OK:
        assert True
    else:
        assert False
    print " Output from HTTP request:"
    print response.read()
        
    httpServ.close()
    
    
if __name__ == '__main__':
   test_datastore_expose_as_layer()