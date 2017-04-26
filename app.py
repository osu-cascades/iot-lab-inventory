from flask import Flask
app = Flask(__name__)

@app.route('/')
@app.route('/index.html')
def index():
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

@app.route("/category_controllers.html")
def category_controllers():
    return app.send_static_file('category_controllers.html')

@app.route("/detail_controllers.html")
def detail_controllers():
    return app.send_static_file('detail_controllers.html')

if __name__ == "__main__":
    app.run()

