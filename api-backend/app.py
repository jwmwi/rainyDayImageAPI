from flask import Flask, render_template, Response, request
from werkzeug.utils import secure_filename
import hashlib
import os
from datetime import datetime
from elasticsearch import Elasticsearch

app = Flask(__name__)

## look for env vars
## not really sure proto should be an option. 
es_proto = os.environ.get('CONFIG_ES_PROTO', "https")
es_server = os.environ.get('CONFIG_ES_SERVER', "127.0.0.1")
es_port = os.environ.get('CONFIG_ES_PORT', "9200")
es_index = os.environ.get('CONFIG_ES_INDEX', "default_test_index")
## BASE64 API_KEY
es_api_key = os.environ.get('CONFIG_ES_API_KEY', "api_key")
es_api_key = es_api_key.strip('"')   # remove quotes from env file

### sample ES 
#
#   get the certs right when you do it.. good from home testing for now.
#
# es = Elasticsearch(hosts='https://127.0.0.1:9200', verify_certs=False, api_key='')
es = Elasticsearch(hosts=es_proto+'://'+es_server+':'+es_port, verify_certs=False, api_key=es_api_key)

base_image_dir = "/images"

## global lastimage

@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/imageUpload', methods=["POST"])
def upload():
    picture = request.files['picture']
    if not picture:
        return 'no picture uploaded', 400
    filename = secure_filename(picture.filename)
    mimetype = picture.mimetype
    image = picture.read()
    uniquehash = hashlib.md5(image).hexdigest()

    # no longer writing out to file. 
    # j = '{ filename = "' + filename + '", mimetype = "' + mimetype + '", hash = "' + uniquehash + '" } '

    doc = { "filename": filename, 
             "mimetype": mimetype, 
             "hash": uniquehash,
             "uploadtime": datetime.now() 
             }

    ## definitly do something to prevent over write, 
    with open(base_image_dir + "/" + uniquehash , 'wb') as f:
        f.write(image)
    with open(base_image_dir + "/last", 'wb') as f:
        f.write(image)

    # image data goes to ES.. 
    es.index(index=es_index,document=doc)

    return 'image uploaded' + j , 200

@app.route('/lastimage')
def getlastimage():
    return getImagebyHash("last")

@app.route('/image/<uniquehash>')
def getImagebyHash(uniquehash):
    
    if type(uniquehash) is not str:
        return "Image not found", 404

    uniquehash = secure_filename(uniquehash)
    full_filename = base_image_dir + "/" + uniquehash 

    if os.path.exists(full_filename):
        image = open(base_image_dir + "/" + uniquehash , 'rb').read()
        return Response(image, mimetype="image/jpeg")
    else:
        return "Image not found",404

@app.route('/imagelist')
def showimages():
    return render_template(
        'results.html', results= listimages()
        )

def listimages():
    results = []
    r = es.search(index=es_index)
    for p in r['hits']['hits']:
        results.append(p['_source']['hash'])
    return results

if __name__ == "__main__":
    app.run()
