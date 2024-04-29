from flask import Flask, redirect, render_template, request, url_for
from sqlalchemy import create_engine, text


conn_str = "mysql://root:Dougnang1@localhost/ecommerce"
engine = create_engine(conn_str, echo=True)
conn = engine.connect()

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


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
    
@app.route('/products.html')
def products():
    query = text('''
        SELECT p.Product_ID, p.Title, p.Description, p.Price, 
            (SELECT Image FROM Images WHERE Product_ID = p.Product_ID LIMIT 1) AS Image
        FROM Products p;
    ''')    
    data = conn.execute(query)
    product_data = []
    for row in data:
        product_info = {
            'title': row[1],
            'price': '{:.2f}'.format(row[3]),
            'image': row[4]
        }
        product_data.append(product_info)
    return render_template('products.html', product_data=product_data)

@app.route('/productDetails.html')


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

@app.route('/itemList.html')
def itemList():
    query = text('''
        SELECT p.Product_ID, p.Title, p.Description, p.Price, 
            (SELECT Image FROM Images WHERE Product_ID = p.Product_ID LIMIT 1) AS Image
        FROM Products p;
    ''')    
    data = conn.execute(query)
    product_data = []
    for row in data:
        product_info = {
            'product_id': row[0],
            'title': row[1],
            'description': row[2],
            'price': '{:.2f}'.format(row[3]),
            'image': row[4]
        }
        product_data.append(product_info)
    return render_template('itemList.html', product_data=product_data)

@app.route('/edit_product/<product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    if request.method == 'GET':
        query = text('''
            SELECT p.Product_ID, p.Title, p.Description, p.Price, p.Warranty_Period, p.Category, p.Number_Available, p.User_ID,
                (SELECT Image FROM Images WHERE Product_ID = p.Product_ID LIMIT 1) AS Image
            FROM Products p
            WHERE p.Product_ID = :product_id;
        ''')
        product_data = conn.execute(query, {'product_id': product_id}).fetchone()

        return render_template('edit_product.html', product_data=product_data)

    elif request.method == 'POST':
        title = request.form['Title']
        description = request.form['Description']
        price = request.form['Price']
        warranty = request.form['Warranty']
        category = request.form['Category']
        number = request.form['Number']

        query = text('''
            UPDATE Products
            SET Title = :title, Description = :description, Price = :price, Warranty_Period = :warranty, Category = :category, Number_Available = :number
            WHERE Product_ID = :product_id;
        ''')
        conn.execute(query, {'title': title, 'description': description, 'price': price, 'warranty': warranty, 'category': category, 'number': number, 'product_id': product_id})
        conn.commit()

        return redirect(url_for('itemList'))

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