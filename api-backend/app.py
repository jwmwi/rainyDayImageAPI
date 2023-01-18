from flask import Flask, render_template, Response, request
from werkzeug.utils import secure_filename
import hashlib
import os

# obviously don't do this, fun for testing
# allimages = []

app = Flask(__name__)

## look for env vars
es_server = os.environ.get('CONFIG_ES_SERVER', "127.0.0.1")
es_port = os.environ.get('CONFIG_ES_PORT', "9200")
es_index = os.environ.get('CONFIG_ES_INDEX', "default_test_index")
es_user = os.environ.get('CONFIG_ES_USER', "elastic")
es_password = os.environ.get('CONFIG_ES_PW', "bad_password")

base_image_dir = "/images"

# until we figure out how we want to setup files.
allimages = []

@app.route('/')
def hello():
    #return '<h3>Hello</h3>'
    return render_template('index.html')

@app.route('/imageUpload', methods=["POST"])
def upload():
    picture = request.files['picture']
    if not picture:
        return 'no picture uploaded', 400
    filename = secure_filename(picture.filename)
    mimetype = picture.mimetype
    image = picture.read()
    uniquehash = hashlib.md5(image)
#    j = '{ filename = "' + filename + '", mimetype = "' + mimetype + '" } '
    j = '{ filename = "' + filename + '", mimetype = "' + mimetype + '", hash = "' + uniquehash.hexdigest() + '" } '
    allimages.append([image,filename,mimetype,j,uniquehash.hexdigest()])
    return 'image uploaded' + j , 200

@app.route('/lastimage')
def getlastimage():
    lastid=len(allimages)-1
    return getImagebyID(lastid)

@app.route('/image/<int:id>')
def getImagebyID(id):
    if id < len(allimages):
        return Response(allimages[id][0], mimetype=allimages[id][2])
    else:
        return "no such image", 400

@app.route('/imagelist')
def showimages():
    return render_template(
        'results.html', results=listimages()
        )

def listimages():
    results = []
    for i in range(len(allimages)):
        ## or prepend /image/
        link = str(i)
        results.append(link)
    return results
    ## figure out what to return
    ## array of links for jinja2 

@app.route('/save')
def saveimages():
    for i in range(len(allimages)):
        image,filename,mimetype,j,uniquehash = allimages[i]
        print("filename :" + filename)
        print("j = " + j )
        print("mime = " + mimetype)
        print("hash = " + uniquehash )
        print()
#        open(rw, base_image_dir + "/" + uniquehash )
        with open(base_image_dir + "/" + uniquehash , 'wb') as f:
            f.write(image)
        with open(base_image_dir + "/" + uniquehash + ".json" , 'w') as f:
            f.write(j)
    return showimages()


@app.route('/jdump')
def dumpJ():
    s=""
    for i in allimages:
        s=s+i[3]+'\n'
    return Response(s, 200)

if __name__ == "__main__":
    app.run()
    
