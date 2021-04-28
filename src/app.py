import StringMatching
from flask import Flask, render_template, request

app = Flask(__name__)
app.static_folder = 'static'

@app.route("/")
def index() :
    return render_template("index.html")

@app.route("/get")
def get_box_response():
    txtdariuser = request.args.get('msg')
    return str(inputCommand(txtdariuser))


if __name__ == "__main__":
    app.run()