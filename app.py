from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return app.send_static_file('index.html') 

@app.route("/main.css")
def css():
    return app.send_static_file('main.css')
    
if __name__ == "__main__":
    app.run()

