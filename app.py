from flask import Flask, jsonify, redirect, url_for, request, render_template 

app = Flask(__name__)

@app.route('/')
def index():
    return "This is yet another version!"

if __name__ == "__main__":
    app.run(debug=False)
