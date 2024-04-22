from flask import Flask, render_template, request, redirect
from sqlalchemy import create_engine, text

c_str = "mysql://root:MySQL@localhost/ecommerce"
engine = create_engine(c_str, echo=True)
connection = engine.connect()

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/admin_vendor')
def avhome():
    return render_template('admin_vendor.html')
    







if __name__ == '__main__':
    app.run(debug=True)