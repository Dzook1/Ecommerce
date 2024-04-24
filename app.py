from flask import Flask, render_template, request, redirect
from sqlalchemy import create_engine, text

conn_str = "mysql://root:cset155@localhost/ecommerce"
engine = create_engine(conn_str, echo=True)
conn = engine.connect()

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/baseCustomer.html')
def baseCustomer():
    return render_template('baseCustomer.html')

@app.route('/loginUser.html', methods=['GET'])
def loginUser():
    return render_template('loginUser.html')
  
@app.route('/admin_vendor')
def avhome():
    return render_template('admin_vendor.html')

@app.route('/loginUser.html', methods=['POST'])
def loginUserGo():
    username = request.form['Username']
    password = request.form['Password']

    query = text("SELECT User_ID FROM Users WHERE Username = :username OR Email = :username AND Password = :password AND Type = 'User'")
    result = conn.execute(query, {'username': username, 'password': password}).fetchone()

    if result:
        global userID
        userID = result[0]
        
        return render_template('userLanding.html')
    else:
        return render_template('index.html')

@app.route('/signup.html', methods=['GET'])
def signup():
    return render_template('signup.html')

@app.route('/signup.html', methods=['POST'])
def signupGo():
    email = request.form['Email']
    password = request.form['Password']

    first = request.form['First_Name']
    last = request.form['Last_Name']

    conn.execute(text("INSERT INTO Users (First_Name, Last_Name, Username, Email, Password, Type) VALUES (:First_Name, :Last_Name, :Username, :Email, :Password, 'User')"), request.form)
    conn.commit()

    query = text('SELECT User_ID from Users WHERE Email = :email AND Password = :password')
    result = conn.execute(query, {"email": email, "password": password}).fetchone()

    query = text("INSERT INTO Customers VALUES (:result, :First_Name, :Last_Name)")
    conn.execute(query, {"result": result[0], "First_Name": first, "Last_Name": last})
    conn.commit()

    return render_template('index.html')

@app.route('/loginEmp.html', methods=['GET'])
def loginEmp():
    return render_template('loginEmp.html')

@app.route('/loginEmp.html', methods=['POST'])
def loginEmpGo():
    username = request.form['Username']
    password = request.form['Password']

    query = text("SELECT User_ID FROM Users WHERE Username = :username AND Password = :password AND Type = 'Admin' OR Type = 'Vendor'")
    result = conn.execute(query, {'username': username, 'password': password}).fetchone()

    if result:
        global AcctID
        AcctID = result[0]
        
        return render_template('empLanding.html')
    else:
        return render_template('index.html')
    
@app.route('/products.html')
def products():
    return render_template('products.html')

if __name__ == '__main__':
    app.run(debug=True)
