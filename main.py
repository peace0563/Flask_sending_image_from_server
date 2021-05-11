from flask import Flask, request, jsonify, make_response
from PIL import Image, ImageDraw
import PIL
from flask_cors import CORS, cross_origin
from io import BytesIO
import base64

app = Flask(__name__)
cors = CORS(app)
app.config["DEBUG"] = True
app.config['CORS_HEADERS'] = 'Content-Type'

@app.after_request
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    return response

#This is my logic to get the pic... you can put here yours
def pil2datauri(arg1, arg2):
    #converts PIL image to datauri
    # creating a image object (main image) 
    img = Image.open(r".\Wall 1.jpg")
    d = ImageDraw.Draw(img)
    d.text((10,10), arg1+" "+arg2, fill=(255,255,0))         
    data = BytesIO()
    img.save(data, "JPEG")
    data64 = base64.b64encode(data.getvalue())

    return u'data:img/jpeg;base64,'+data64.decode('utf-8')

#the OPTIONS method is just because of new policy of CORS
#if you are curious to know about it
#https://dev.to/p0oker/why-is-my-browser-sending-an-options-http-request-instead-of-post-5621#:~:text=As%20you%20can%20see%2C%20the,So...
#check the link


@app.route('/', methods=['OPTIONS', 'GET'])
def create_task():
    if request.method == "OPTIONS":
        return _build_cors_prelight_response()
    elif request.method == "GET":
        args = request.args
        print(args) # For debugging
        #if "type" not in args and "text" not in args:
        #    abort(400)
        arg1 = args['type']
        arg2 = args['text']
        
        g = pil2datauri(arg1, arg2)
        html = "<img src="+g+" width='80%' height='auto'></img >"
        return html, 201
    else:
        abort(400)

def _build_cors_prelight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response

app.run()