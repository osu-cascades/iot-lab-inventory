from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return app.send_static_file('index.html') 

@app.route("/main.css")
def css():
    return app.send_static_file('main.css')
    
@app.route("/main_admin.html")
def main_admin():
    return app.send_static_file('main_admin.html')

@app.route("/main_student.html")
def main_student():
    return app.send_static_file('main_student.html')

if __name__ == "__main__":
    app.run()

@app.after_request
def add_header(r):
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

