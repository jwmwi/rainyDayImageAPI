from flask import Flask, render_template, Response, request
from werkzeug.utils import secure_filename

# obviously don't do this, fun for testing
allimages = []

app = Flask(__name__)

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
    allimages.append([image,filename,mimetype])
    return 'image uploaded', 200

@app.route('/lastimage')
def getlastimage():
    last = allimages[-1]
    return Response(last[0], last[2])

if __name__ == "__main__":
    app.run()
    
