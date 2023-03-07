from flask import Flask, redirect, url_for, render_template

app = Flask(__name__)

@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html")

@app.route("/scene")
def threes():
    return render_template("scene.html")

if __name__ == '__main__':
    app.run(debug=True, port=5000)
