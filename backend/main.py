from flask import Flask
from flask import request
import requests

app = Flask(__name__)

content = ""


@app.route("/", methods=['POST'])
def testPost():
    if request.method == 'POST':
        return "Received POST --->>> " + str(request.data)
    else:
        return "Post didnt work"


@app.route("/", methods=['GET'])
def hello():
    return "Hello from the interceptor!"


@app.route("/apiv2", methods=['GET'])
def api():
    return "hello from api GET"


@app.route("/api", methods=['POST'])
def apiv2():
    if request.method == 'POST':
        print("кто то меня дернул")
        return "hello from api POST"
    else:
        return "Post didnt work"


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=3000)
