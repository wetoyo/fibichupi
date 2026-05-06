from flask import Flask
app = Flask(__name__)
@app.route("/", methods=["GET", "POST"])
def homepage():
    return "fiibi jewpyun"
if __name__ == "__main__":
    app.debug = True
    app.run() 
