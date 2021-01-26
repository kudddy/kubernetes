from flask import Flask
from flask import request
import requests
import os
app = Flask(__name__)

address = os.environ['BACKENDHOST']
# @app.route("/")
# def hello():
#     address = 'http://interceptor-service:5002/'  # <--- this is the IP I want to get automatically
#     r = requests.post(address, data="---[Token]---")
#     return "Frontend Here. Response from Backend = " + str(r.content)


@app.route("/api", methods=['GET'])
def api():
    return "hello from api v 2"


@app.route("/apiv2", methods=['GET'])
def apiv2():
    print("мы дернули на сервис")
    r = requests.post(address, data="---[Token]---")
    return "handshake"


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8080)
