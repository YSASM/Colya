from flask import Flask
from flask_cors import *
import waitress
api = Flask(__name__) 
CORS(api, supports_credentials=True, resources=r"/*")


@api.route("/",methods=['get'])
def Index():
    return 'OK'

def start(port="7796"):
    waitress.serve(api, host='0.0.0.0', port=port)