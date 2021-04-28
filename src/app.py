from StringMatching import *
from flask import Flask, render_template, request

app = Flask(__name__)
app.static_folder = 'static'

@app.route("/")
def home() :
    return render_template("index.html")

@app.route("/get")
def get_bot_response():
    txtdariuser = request.args.get('pesan')
    return str(inputCommand(txtdariuser))


if __name__ == "__main__":
    app.run()