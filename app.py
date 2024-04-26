from flask import Flask, render_template, request
from sqlalchemy import create_engine, text

conn_str = "mysql://root:MySQL@localhost/ecommerce"
engine = create_engine(conn_str, echo=True)
conn = engine.connect()

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/loginUser.html', methods=['GET'])
def loginUser():
    return render_template('loginUser.html')

@app.route('/products.html')
def producthome():
    return render_template('products.html')

@app.route('/loginUser.html', methods=['POST'])
def loginUserGo():
    username = request.form['Username']
    password = request.form['Password']

    query = text("SELECT User_ID FROM Users WHERE Username = :username OR Email = :username AND Password = :password AND Type = 'User'")
    result = conn.execute(query, {'username': username, 'password': password}).fetchone()

    if result:
        global userID
        userID = result[0]
        
        return render_template('/baseCustomer.html')
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

    query = text("SELECT User_ID FROM Users WHERE Username = :username AND Password = :password AND Type = 'Admin' OR Username = :username AND Password = :password AND Type = 'Vendor'")
    result = conn.execute(query, {'username': username, 'password': password}).fetchone()

    if result:
        global AcctID
        AcctID = result[0]

        query = text("SELECT Type FROM Users WHERE Username = :username AND Password = :password")
        result2 = conn.execute(query, {'username': username, 'password': password}).fetchone()
        
        if result2[0] == "ADMIN":
            return render_template('adminLanding.html')
        else:
            return render_template('empLanding.html')
    else:
        return render_template('index.html')

@app.route('/adminLanding.html')
def adminLanding():
    return render_template('adminLanding.html')

@app.route('/add_item.html', methods=['GET'])
def addItem():
    return render_template('add_item.html')

@app.route('/add_item.html', methods=['POST'])
def addItemGo():    
    return render_template('add_item.html')


    # -------------------------- CUSTOMER PAGE ------------------------------------------

@app.route('/baseCustomer.html')
def baseCustomer():
    return render_template('baseCustomer.html')

@app.route('/orders.html', methods=['GET'])
def orders():
    order = conn.execute(text(f'SELECT * FROM ORDERS WHERE USER_ID = {userID}')).all()
    print(order)
    return render_template('orders.html', orders=order)

@app.route('/orderDetails/<ORDER_ID>', methods=['GET'])
def orderDetails(ORDER_ID):
    allOrderDetails = conn.execute(text(f'SELECT * FROM ORDER_ITEMS WHERE ORDER_ID = {ORDER_ID}')).all()
    print(allOrderDetails)
    return render_template('/orderDetails.html', orderDetails=allOrderDetails)

@app.route('/cart.html')
def cart():
    cart = conn.execute(text(f'SELECT * FROM CARTS NATURAL JOIN CART_ITEMS WHERE USER_ID = {userID}')).all()
    print(cart)
    return render_template('/cart.html', cart=cart)

@app.route('/account.html', methods=["GET"])
def account():
    account = conn.execute(text(f'SELECT * FROM USERS WHERE USER_ID = {userID}')).all()
    print(account)
    return render_template(f'/account.html', account=account)




# --------------------------------------- END CUSTOMER -----------------------------------------







if __name__ == '__main__':
    app.run(debug=True)