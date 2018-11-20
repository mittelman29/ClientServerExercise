import json
from lib.Data import Data

def monitoringClient(data, dataConn):
    base_path = './monitoring-site/build/'
    req = data.split(' ')
    method = req[0]
    path = req[1]
    path = path.lstrip('/')

    if path == '':
        path = base_path + 'index.html'
    else:
        path = base_path + path
    
    file = open(path,'rb')
    response = file.read()
    file.close()

    try:

        header = 'HTTP/1.1 200 OK\n'

        if(path.endswith(".jpg")):
            mimetype = 'image/jpg'
        elif(path.endswith(".css")):
            mimetype = 'text/css'
        else:
            mimetype = 'text/html'

        header += 'Content-Type: '+str(mimetype)+'\n\n'

    except Exception as e:
        print "EXCEPTION: %s" % str(e)
        header = 'HTTP/1.1 404 Not Found\n\n'
        response = """<html>
                        <body>
                            <center>
                            <h3>Error 404: File not found</h3>
                            <p>Python HTTP Server</p>
                            </center>
                        </body>
                        </html>""".encode('utf-8')

    final_response = header + response

    return final_response

def dataClient(data, dataConn):
    argList = []

    header = 'HTTP/1.1 200 OK\nContent-type: application/json\nAccess-Control-Allow-Origin: *\nAccess-Control-Allow-Methods: GET,PUT,POST,DELETE,OPTIONS\n\n'

    req = data.split(' ')

    # Grab the method (GET/POST/PUT/DELETE) from request. Not implementing here, but in a standard API
    # we'd decide on actions to take based on method AND path
    method = req[0]

    # Grab the path (/set) and args (?keyToAdd=value)
    if '?' in req[1]:
        path, args = req[1].split('?')

        # If there are multiple args (presence of an &), split on &
        argList = args.split('&')

    else:
        path = req[1]
    
    # Get all key/value pairs
    if path == '/':
        response = json.dumps(dataConn.getAll())

    # Set a key/value pair
    elif path == '/set':
        if len(argList) == 0:
            response = "You must provide at least one key/value pair to set" 

        for arg in argList:
            key, val = arg.split('=')
            if not dataConn.set(key, val):
                response = "One or more set commands failed"
            
        response = json.dumps(dataConn.getAll())

    # Delete a key/value pair
    elif path.startswith('/del/'):
        # Find the key from the path after /del/
        keyParts = path.split('/')

        if keyParts[1] == 'del':
            try:
                dataConn.delete(keyParts[2])
            except Exception as e:
                print('Error: %s' % str(e))

        response = json.dumps(dataConn.getAll())

    # Get a single key/value pair
    elif path.startswith('/'):
        key = path.replace('/','')
        print "FINDING: %s" % key
        response = json.dumps({ key: dataConn.get(key) })

    else:
        response = "METHOD: %s, PATH: %s" % (method,path)

    return header + response