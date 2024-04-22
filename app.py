from flask import Flask, render_template, request, redirect
from sqlalchemy import create_engine, text

c_str = "mysql://root:MySQL@localhost/ecommerce"
engine = create_engine(c_str, echo=True)
connection = engine.connect()

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')







if __name__ == '__app__':
    app.run(debug=True)