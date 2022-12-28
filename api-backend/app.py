from flask import Flask, render_template, Response, request
from werkzeug.utils import secure_filename

# obviously don't do this, fun for testing
# allimages = []

app = Flask(__name__)

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
    j = '{ filename = "' + filename + '", mimetype = "' + mimetype + '" } '
    allimages.append([image,filename,mimetype,j])
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

@app.route('/jdump')
def dumpJ():
    s=""
    for i in allimages:
        s=s+i[3]+'\n'
    return Response(s, 200)

if __name__ == "__main__":
    app.run()
    
