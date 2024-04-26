from flask import Flask, render_template, request
from sqlalchemy import create_engine, text

conn_str = "mysql://root:Dougnang1@localhost/ecommerce"
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

@app.route('/loginUser.html', methods=['POST'])
def loginUserGo():
    username = request.form['Username']
    password = request.form['Password']

    query = text("SELECT User_ID FROM Users WHERE Username = :username AND Password = :password AND Type = 'User' OR Email = :username AND Password = :password AND Type = 'User'")
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

    query = text("SELECT User_ID FROM Users WHERE Username = :username AND Password = :password AND Type = 'Admin' OR Username = :username AND Password = :password AND Type = 'Vendor'")
    result = conn.execute(query, {'username': username, 'password': password}).fetchone()

    if result:
        global AcctID
        AcctID = result[0]

        query = text("SELECT Type FROM Users WHERE Username = :username AND Password = :password")
        result2 = conn.execute(query, {'username': username, 'password': password}).fetchone()
        
        if result2[0] == "Admin":
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
    title = request.form['Title']
    description = request.form['Description']
    images = request.form['Images']
    warranty = request.form['Warranty']
    category = request.form['Category']
    colors = request.form['Colors']
    sizes = request.form['Sizes']
    number = request.form['Number']
    price = request.form['Price']

    query = text("INSERT INTO Products (Title, Description, Warranty_Period, Category, Number_Available, Price, User_ID) VALUES (:Title, :Description, :Warranty, :Category, :Number, :Price, :User_ID)")
    conn.execute(query, {'Title': title, 'Description': description, 'Warranty': warranty, 'Category': category, 'Number': number, 'Price': price, 'User_ID': AcctID})
    conn.commit()

    product_id = conn.execute(text("SELECT MAX(Product_ID) FROM Products")).scalar()

    for image in images.split(','):
        query = text("INSERT INTO Images (Product_ID, Image) VALUES (:Product_ID, :Image)")
        conn.execute(query, {'Product_ID': product_id, 'Image': image})
        conn.commit()

    for color in colors.split(','):
        query = text("INSERT INTO Colors (Product_ID, Color) VALUES (:Product_ID, :Color)")
        conn.execute(query, {'Product_ID': product_id, 'Color': color})
        conn.commit()

    for size in sizes.split(','):
        query = text("INSERT INTO Sizes (Product_ID, Size) VALUES (:Product_ID, :Size)")
        conn.execute(query, {'Product_ID': product_id, 'Size': size})
        conn.commit()

    return render_template('empLanding.html')

@app.route('/add_itemAdmin.html', methods=['GET'])
def addItemAdmin():
    return render_template('add_itemAdmin.html')

@app.route('/add_itemAdmin.html', methods=['POST'])
def addItemAdminGo():
    title = request.form['Title']
    description = request.form['Description']
    images = request.form['Images']
    warranty = request.form['Warranty']
    category = request.form['Category']
    colors = request.form['Colors']
    sizes = request.form['Sizes']
    number = request.form['Number']
    price = request.form['Price']
    id = request.form['ID']

    query = text("SELECT Type FROM Users WHERE User_ID = :id")
    type = conn.execute(query, {"id": id}).fetchone()[0]
    if type == "Vendor":
        query = text("INSERT INTO Products (Title, Description, Warranty_Period, Category, Number_Available, Price, User_ID) VALUES (:Title, :Description, :Warranty, :Category, :Number, :Price, :User_ID)")
        conn.execute(query, {'Title': title, 'Description': description, 'Warranty': warranty, 'Category': category, 'Number': number, 'Price': price, 'User_ID': id})
        conn.commit()

        product_id = conn.execute(text("SELECT MAX(Product_ID) FROM Products")).scalar()

        for image in images.split(','):
            query = text("INSERT INTO Images (Product_ID, Image) VALUES (:Product_ID, :Image)")
            conn.execute(query, {'Product_ID': product_id, 'Image': image})
            conn.commit()

        for color in colors.split(','):
            query = text("INSERT INTO Colors (Product_ID, Color) VALUES (:Product_ID, :Color)")
            conn.execute(query, {'Product_ID': product_id, 'Color': color})
            conn.commit()

        for size in sizes.split(','):
            query = text("INSERT INTO Sizes (Product_ID, Size) VALUES (:Product_ID, :Size)")
            conn.execute(query, {'Product_ID': product_id, 'Size': size})
            conn.commit()

        return render_template('adminLanding.html')
    else:
        return render_template('add_itemAdmin.html')

if __name__ == '__main__':
    app.run(debug=True)