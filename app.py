from decimal import Decimal
from flask import Flask, redirect, render_template, request, url_for
from sqlalchemy import create_engine, text
import ctypes
from datetime import date

conn_str = "mysql://root:cset155@localhost/ecommerce"
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
        
        return render_template('baseCustomer.html')
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

    query = text("INSERT INTO Carts (User_ID, Total_Price) VALUES (:User_ID, 0)")
    conn.execute(query, {"User_ID": result[0]})
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
    warrantyYR = request.form['WarrantyYR']
    warrantyMN = request.form['WarrantyMN']
    category = request.form['Category']
    colors = request.form['Colors']
    sizes = request.form['Sizes']
    number = request.form['Number']
    price = request.form['Price']
    discount = request.form['DiscountAmt']
    discountLength = request.form['DiscountLength']

    query = text("INSERT INTO Products (Title, Description, Category, Number_Available, Price, User_ID) VALUES (:Title, :Description, :Category, :Number, :Price, :User_ID)")
    conn.execute(query, {'Title': title, 'Description': description, 'Category': category, 'Number': number, 'Price': price, 'User_ID': AcctID})
    conn.commit()

    product_id = conn.execute(text("SELECT MAX(Product_ID) FROM Products")).scalar()

    query = text("INSERT INTO Warranty VALUES (:Product_ID, :WarrantyYR, :WarrantyMN)")
    conn.execute(query, {'Product_ID': product_id, 'WarrantyYR': warrantyYR, 'WarrantyMN': warrantyMN})
    conn.commit()

    query = text("INSERT INTO Discount VALUES (:Product_ID, :discountLength, :discount)")
    conn.execute(query, {'Product_ID': product_id, 'discountLength': discountLength, 'discount': discount})
    conn.commit()

    for image in images.split(', '):
        query = text("INSERT INTO Images (Product_ID, Image) VALUES (:Product_ID, :Image)")
        conn.execute(query, {'Product_ID': product_id, 'Image': image})
        conn.commit()

    for color in colors.split(', '):
        query = text("INSERT INTO Colors (Product_ID, Color) VALUES (:Product_ID, :Color)")
        conn.execute(query, {'Product_ID': product_id, 'Color': color})
        conn.commit()

    for size in sizes.split(', '):
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
    warrantyYR = request.form['WarrantyYR']
    warrantyMN = request.form['WarrantyMN']
    category = request.form['Category']
    colors = request.form['Colors']
    sizes = request.form['Sizes']
    number = request.form['Number']
    price = request.form['Price']
    id = request.form['ID']
    discount = request.form['DiscountAmt']
    discountLength = request.form['DiscountLength']

    query = text("SELECT Type FROM Users WHERE User_ID = :id")
    type = conn.execute(query, {"id": id}).fetchone()[0]
    if type == "Vendor":
        query = text("INSERT INTO Products (Title, Description, Category, Number_Available, Price, User_ID) VALUES (:Title, :Description, :Category, :Number, :Price, :User_ID)")
        conn.execute(query, {'Title': title, 'Description': description, 'Category': category, 'Number': number, 'Price': price, 'User_ID': id})
        conn.commit()

        product_id = conn.execute(text("SELECT MAX(Product_ID) FROM Products")).scalar()

        query = text("INSERT INTO Warranty VALUES (:Product_ID, :WarrantyYR, :WarrantyMN)")
        conn.execute(query, {'Product_ID': product_id, 'WarrantyYR': warrantyYR, 'WarrantyMN': warrantyMN})
        conn.commit()

        query = text("INSERT INTO Discount VALUES (:Product_ID, :discountLength, :discount)")
        conn.execute(query, {'Product_ID': product_id, 'discountLength': discountLength, 'discount': discount})
        conn.commit()

        for image in images.split(', '):
            query = text("INSERT INTO Images (Product_ID, Image) VALUES (:Product_ID, :Image)")
            conn.execute(query, {'Product_ID': product_id, 'Image': image})
            conn.commit()

        for color in colors.split(', '):
            query = text("INSERT INTO Colors (Product_ID, Color) VALUES (:Product_ID, :Color)")
            conn.execute(query, {'Product_ID': product_id, 'Color': color})
            conn.commit()

        for size in sizes.split(', '):
            query = text("INSERT INTO Sizes (Product_ID, Size) VALUES (:Product_ID, :Size)")
            conn.execute(query, {'Product_ID': product_id, 'Size': size})
            conn.commit()

        return render_template('adminLanding.html')
    else:
        return render_template('add_itemAdmin.html')

@app.route('/itemList.html')
def itemList():
    query = text('''
        SELECT p.Product_ID, p.Title, p.Description, p.Price 
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
    return render_template('/baseCustomer.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        search_term = request.form.get('search')
        if search_term:
            query = text(f'''
                SELECT p.Product_ID, p.Title, p.Description, p.Price, 
                    (SELECT Image FROM Images WHERE Product_ID = p.Product_ID LIMIT 1) AS Image
                FROM Products p
                WHERE p.Title LIKE :search_term;
            ''')
            result = conn.execute(query, {'search_term': f'%{search_term}%'}).fetchall()
            if result:
                global product_data
                product_data = []
                for row in result:
                    product_info = {
                        'product_id': row[0],
                        'title': row[1],
                        'price': '{:.2f}'.format(row[3]),
                        'image': row[4]
                    }
                    product_data.append(product_info)
                return render_template('products.html', product_data=product_data)
            else:
                return render_template('no_results.html')
        else:
            return render_template('baseCustomer.html')
    else:
        return render_template('baseCustomer.html')
    
@app.route('/no_results.html')
def no_results():
    return render_template('no_results.html')

@app.route('/orders.html', methods=['GET'])
def orders():
    order = conn.execute(text(f'SELECT * FROM ORDERS WHERE USER_ID = {userID}')).all()
    print(order)
    return render_template('orders.html', orders=order)

@app.route('/orderDetails.html', methods=['GET'])
def orderDetails():
    # allOrderDetails = conn.execute(text(f'SELECT * FROM ORDER_ITEMS WHERE ORDER_ID = {ORDER_ID}')).all()
    # print(allOrderDetails)
    return render_template('/orderDetails.html')

@app.route('/complaint.html')
def complaint():
    return render_template('complaint.html')

@app.route('/cart.html', methods=["GET"])
def cart():
    query = text(f'''
        SELECT Cart_ID
        FROM Carts
        WHERE User_ID = :user_id
                ''')
    cart_id = conn.execute(query, {'user_id': userID}).fetchone()[0]

    query = text(f'''
        SELECT * 
        FROM Cart_Items
        WHERE Cart_ID = :cart_id
                 ''')
    cart_items = conn.execute(query, {'cart_id': cart_id}).fetchall()

    query = text(f'''
        SELECT Total_Price 
        FROM Carts
        WHERE Cart_ID = :cart_id
                 ''')
    cart_price = conn.execute(query, {'cart_id': cart_id}).fetchone()[0]

    return render_template('cart.html', cart_items=cart_items, cart_price=cart_price)

@app.route('/cart.html', methods=["POST"])
def cartGo():
    query = text('''
        SELECT Cart_ID
        FROM Carts
        WHERE User_ID = :user_id
    ''')
    cart_id = conn.execute(query, {'user_id': userID}).fetchone()[0]

    query = text('''
        SELECT Total_Price
        FROM Carts
        WHERE User_ID = :user_id
    ''')
    price = conn.execute(query, {'user_id': userID}).fetchone()[0]

    query = text('''
        SELECT *
        FROM Cart_Items
        WHERE Cart_ID = :cart_id
    ''')
    cart_items = conn.execute(query, {'cart_id': cart_id}).fetchall()

    return render_template('payment.html', cart_items=cart_items, price=price)

@app.route('/payment.html', methods=["POST"])
def paymentGo():
    current_date = date.today()

    query = text('''
        SELECT Total_Price
        FROM Carts
        WHERE User_ID = :user_id
    ''')
    price = conn.execute(query, {'user_id': userID}).fetchone()[0]

    query = text('''
        INSERT INTO Orders (User_ID, Order_Date, Total_Price, Order_Status)
        VALUES (:user_id, :current_date, :price, "PENDING")
    ''')
    conn.execute(query, {'user_id': userID, 'current_date': current_date, 'price': price})
    conn.commit()

    query = text('''
        SELECT MAX(Order_ID)
        FROM Orders
        WHERE User_ID = :user_id
    ''')
    OrderID = conn.execute(query, {'user_id': userID}).fetchone()[0]

    query = text('''
        SELECT Cart_ID
        FROM Carts
        WHERE User_ID = :user_id
    ''')
    CartID = conn.execute(query, {'user_id': userID}).fetchone()[0]

    query = text('''
        SELECT *
        FROM Cart_Items
        WHERE Cart_ID = :cart_id
    ''')
    cart_items = conn.execute(query, {'cart_id': CartID}).fetchall()

    for item in cart_items:
        product_id = item[1]
        title = item[3]
        amount = item[4]
        color = item[5]
        size = item[6]
        image = item[7]
        indPrice = Decimal(item[8]) * int(amount)

        query = text('''
            SELECT Warranty_Year
            FROM Warranty
            WHERE Product_ID = :product_id
        ''')
        warranty_years = conn.execute(query, {'product_id': product_id}).fetchone()[0]

        query = text('''
            SELECT Warranty_Month
            FROM Warranty
            WHERE Product_ID = :product_id
        ''')
        warranty_months = conn.execute(query, {'product_id': product_id}).fetchone()[0]

        if (current_date.month + warranty_months) > 12:
            expiry_date = current_date.replace(year=current_date.year + warranty_years + 1, month=current_date.month + warranty_months - 12)
        else:
            expiry_date = current_date.replace(year=current_date.year + warranty_years, month=current_date.month + warranty_months)

        query = text('''
            INSERT INTO Order_Items (Order_ID, Title, Expiry, Amount, Color, Size, Image, Price)
            VALUES (:OrderID, :title, :expiry_date, :amount, :color, :size, :image, :indPrice)
        ''')
        conn.execute(query, {'OrderID': OrderID, 'title': title, 'expiry_date': expiry_date, 'amount': amount, 'color': color, 'size': size, 'image': image, 'indPrice': indPrice})
        conn.commit()

    query = text('''
        DELETE FROM Cart_Items
        WHERE Cart_ID = :CartID
    ''')
    conn.execute(query, {'CartID': CartID})
    conn.commit()

    query = text('''
        UPDATE Carts
        SET Total_Price = 0
        WHERE User_ID = :userID
    ''')
    conn.execute(query, {'userID': userID})
    conn.commit()

    return render_template('baseCustomer.html')


@app.route('/account.html', methods=["GET"])
def account():
    account = conn.execute(text(f'SELECT * FROM USERS WHERE USER_ID = {userID}')).all()
    print(account)
    return render_template('/account.html', account=account)

@app.route('/view_accounts.html')
def view_accounts():
    users = conn.execute(text('SELECT * FROM Users')).fetchall()
    return render_template('view_accounts.html', users=users)

@app.route('/dashboard.html')
def dashboard():
    # def Mbox(title,text,style):
    #     return ctypes.windll.user32.MessageBoxW(0, text, title, style) 
    # Mbox("Your Title", "Your Text", 0)
    return render_template('/dashboard.html')


@app.route('/chats.html', methods=["GET"])
def chats():
    vendors = conn.execute(text('SELECT * FROM USERS WHERE TYPE = "VENDOR"')).all()
    return render_template('/chats.html', chats=vendors)

@app.route('/chatting/<User_id>', methods=["POST", "GET"])
def chatting(User_id):
    # If chat doesn't already exist: ?
    start = conn.execute(text(f"INSERT INTO CHATS (Sender_id, Receiver_id, Content) VALUES ({userID}, {User_id}, 'Chat has Started.')"))
    chatStarted = conn.execute(text(f"SELECT * FROM chats WHERE Sender_id = {userID}  AND Receiver_ID = {User_id}")).all()
    print(chatStarted)
    # else:?
        # chatStarted = conn.execute(text("SELECT * FROM CHATS"))
    return render_template(f'/chatting.html', chatting=chatStarted)

@app.route('/products')
def products():
    query = text('''
        SELECT p.Product_ID, p.Title, p.Price, MIN(i.Image) AS Image
        FROM Products p
        JOIN Images i ON p.Product_ID = i.Product_ID
        GROUP BY p.Product_ID, p.Title;
    ''')
    data = conn.execute(query)
    global product_data
    product_data = []
    for row in data:
        product_info = {
            'product_id': row[0],
            'title': row[1],
            'price': '{:.2f}'.format(row[2]),
            'image': row[3]
        }
        product_data.append(product_info)
    return render_template('products.html', product_data=product_data)

@app.route('/product_details/<product_id>')
def product_details(product_id):
    query = text('''
        SELECT *
        FROM Products
        WHERE Product_ID = :product_id;
    ''')
    product_data = conn.execute(query, {'product_id': product_id}).fetchone()

    query = text('''
        SELECT Image
        FROM Images
        WHERE Product_ID = :product_id;
    ''')
    images = conn.execute(query, {'product_id': product_id}).fetchall()

    query = text('''
        SELECT Color
        FROM Colors
        WHERE  Product_ID = :product_id;
    ''')
    colors = conn.execute(query, {'product_id': product_id}).fetchall()

    query = text('''
        SELECT Size
        FROM Sizes
        WHERE  Product_ID = :product_id;
    ''')
    sizes = conn.execute(query, {'product_id': product_id}).fetchall()

    query = text('''
        SELECT Warranty_Year, Warranty_Month
        FROM Warranty
        WHERE Product_ID = :product_id
    ''')

    warranties = conn.execute(query,  {'product_id': product_id}).fetchone()

    query = text("SELECT * FROM Discount WHERE Product_ID =:product_id AND Discount_Period >= CURRENT_DATE")
    discounts = conn.execute(query, {'product_id': product_id, 'current_date': date.today()}).fetchall()
    
    if discounts:
        discount = discounts[0]
        if discount.Discount_Amount != 0:
            discounted_price = Decimal(product_data.Price) - Decimal(product_data.Price) * (Decimal(discount.Discount_Amount) / Decimal(100))
        else:
            discounted_price = None
    else:
        discounted_price = None

    return render_template('productDetails.html', product_data=product_data, images=images, warranties=warranties, colors=colors, sizes=sizes, discounts=discounts, discounted_price=discounted_price,current_date=date.today())

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    product_id = request.form['product_id']
    user_id = userID
    color = request.form['color']
    size = request.form['size']
    amount = request.form['amount']

    query = text("SELECT * FROM Discount WHERE Product_ID =:product_id AND Discount_Period >= CURRENT_DATE")
    discounts = conn.execute(query, {'product_id': product_id, 'current_date': date.today()}).fetchall()
    
    if discounts:
        discount = discounts[0]
        if discount.Discount_Amount != 0:
            query = text('''
                SELECT Price
                FROM Products
                WHERE Product_ID = :product_id;
            ''')
            price = conn.execute(query, {'product_id': product_id}).fetchone()[0]
            price = Decimal(price) - Decimal(price) * (Decimal(discount.Discount_Amount) / Decimal(100))
        else:
            query = text('''
                SELECT Price
                FROM Products
                WHERE Product_ID = :product_id;
            ''')
            price = conn.execute(query, {'product_id': product_id}).fetchone()[0]
    else:
        query = text('''
            SELECT Price
            FROM Products
            WHERE Product_ID = :product_id;
        ''')
        price = conn.execute(query, {'product_id': product_id}).fetchone()[0]
    
    query = text('''
        SELECT Total_Price
        FROM Carts
        WHERE User_ID = :user_id;
    ''')
    price2 = conn.execute(query, {'user_id': user_id}).fetchone()[0]
    
    totalPrice = float(price) * int(amount) + float(price2)

    query = text('''
        SELECT Title
        FROM Products
        WHERE Product_ID = :product_id;
    ''')
    title = conn.execute(query, {'product_id': product_id}).fetchone()[0]

    query = text('''
        SELECT Image
        FROM Images
        WHERE Product_ID = :product_id;
    ''')
    image = conn.execute(query, {'product_id': product_id}).fetchone()[0]

    query = text('''
        SELECT Cart_ID
        FROM Carts
        WHERE User_ID = :user_id;
    ''')
    cart_id = conn.execute(query, {'user_id': user_id}).fetchone()[0]

    query = text('''
        UPDATE Carts SET Total_Price = :totalPrice WHERE User_ID = :user_id;
    ''')
    conn.execute(query, {'user_id': user_id, 'totalPrice': totalPrice})
    conn.commit()

    query = text('''
        INSERT INTO Cart_Items (Cart_ID, Product_ID, Title, Price, Amount, Color, Size, Image)
        VALUES (:cart_id, :product_id, :title, :price, :amount, :color, :size, :image);
    ''')
    conn.execute(query, {'cart_id': cart_id, 'product_id': product_id, 'title': title, 'price': price, 'amount': amount, 'color': color, 'size': size, 'image': image})
    conn.commit()

    return redirect(url_for('products'))

@app.route('/payment.html')
def payment():
    return render_template('payment.html')

@app.route('/delete_product_cart/<cart_item_id>', methods=['POST'])
def delete_product_cart(cart_item_id):
    query = text('''
        SELECT Price
        FROM Cart_Items
        WHERE Cart_Item_ID = :cart_item_id;
    ''')
    price = conn.execute(query, {'cart_item_id': cart_item_id}).fetchone()[0]

    query = text('''
        SELECT Amount
        FROM Cart_Items
        WHERE Cart_Item_ID = :cart_item_id;
    ''')
    amount = conn.execute(query, {'cart_item_id': cart_item_id}).fetchone()[0]

    price = Decimal(price) * int(amount)

    query = text('''
        SELECT Total_Price
        FROM Carts
        WHERE User_ID = :user_id
    ''')
    price2 = conn.execute(query, {'user_id': userID}).fetchone()[0]

    price3 = Decimal(price2) - Decimal(price)

    if price3 < 0:
        price3 = 0

    query = text('''
        UPDATE Carts
        SET Total_Price = :price3
        WHERE User_ID = :user_id
    ''')
    conn.execute(query, {'price3': price3, 'user_id': userID})
    conn.commit()

    query = text('''
        DELETE FROM Cart_Items
        WHERE Cart_Item_ID = :cart_item_id;
    ''')
    conn.execute(query, {'cart_item_id': cart_item_id})
    conn.commit()

    query = text(f'''
        SELECT Cart_ID
        FROM Carts
        WHERE User_ID = :user_id
                ''')
    cart_id = conn.execute(query, {'user_id': userID}).fetchone()[0]

    query = text(f'''
        SELECT * 
        FROM Cart_Items
        WHERE Cart_ID = :cart_id
                 ''')
    cart_items = conn.execute(query, {'cart_id': cart_id}).fetchall()

    query = text(f'''
        SELECT Total_Price 
        FROM Carts
        WHERE Cart_ID = :cart_id
                 ''')
    cart_price = conn.execute(query, {'cart_id': cart_id}).fetchone()[0]

    return render_template('cart.html', cart_items=cart_items, cart_price=cart_price)

@app.route('/delete_product/<product_id>', methods=['POST'])
def delete_product(product_id):
    query = text('''
        DELETE FROM Images
        WHERE Product_ID = :product_id;
    ''')
    conn.execute(query, {'product_id': product_id})
    conn.commit()

    query = text('''
        DELETE FROM Sizes
        WHERE Product_ID = :product_id;
    ''')
    conn.execute(query, {'product_id': product_id})
    conn.commit()

    query = text('''
        DELETE FROM Warranty
        WHERE Product_ID = :product_id;
    ''')
    conn.execute(query, {'product_id': product_id})
    conn.commit()

    query = text('''
        DELETE FROM Discount
        WHERE Product_ID = :product_id;
    ''')
    conn.execute(query, {'product_id': product_id})
    conn.commit()

    query = text('''
        DELETE FROM Colors
        WHERE Product_ID = :product_id;
    ''')
    conn.execute(query, {'product_id': product_id})
    conn.commit()

    query = text('''
        DELETE FROM Products
        WHERE Product_ID = :product_id;
    ''')
    conn.execute(query, {'product_id': product_id})
    conn.commit()

    return redirect(url_for('itemList'))

@app.route('/itemListVendor.html')
def itemListVendor():
    query = text('''
        SELECT p.Product_ID, p.Title, p.Description, p.Price 
        FROM Products p WHERE User_ID = :AcctID;
    ''')
    data = conn.execute(query, {"AcctID": AcctID})
    product_data = []
    for row in data:
        product_info = {
            'product_id': row[0],
            'title': row[1],
            'description': row[2],
            'price': '{:.2f}'.format(row[3]),
        }
        product_data.append(product_info)
    return render_template('itemListVendor.html', product_data=product_data)

@app.route('/delete_product_vendor/<product_id>', methods=['POST'])
def delete_product_vendor(product_id):
    query = text('''
        DELETE FROM Images
        WHERE Product_ID = :product_id;
    ''')
    conn.execute(query, {'product_id': product_id})
    conn.commit()

    query = text('''
        DELETE FROM Sizes
        WHERE Product_ID = :product_id;
    ''')
    conn.execute(query, {'product_id': product_id})
    conn.commit()

    query = text('''
        DELETE FROM Colors
        WHERE Product_ID = :product_id;
    ''')
    conn.execute(query, {'product_id': product_id})
    conn.commit()

    query = text('''
        DELETE FROM Warranty
        WHERE Product_ID = :product_id;
    ''')
    conn.execute(query, {'product_id': product_id})
    conn.commit()

    query = text('''
        DELETE FROM Discount
        WHERE Product_ID = :product_id;
    ''')
    conn.execute(query, {'product_id': product_id})
    conn.commit()

    query = text('''
        DELETE FROM Products
        WHERE Product_ID = :product_id;
    ''')
    conn.execute(query, {'product_id': product_id})
    conn.commit()

    return redirect(url_for('itemListVendor'))


@app.route('/productFilter.html/<category>')
def productFilter(category):
    query = text('''
        SELECT p.Product_ID, p.Title, p.Price, MIN(i.Image) AS Image
        FROM Products p
        JOIN Images i ON p.Product_ID = i.Product_ID
        WHERE p.Category LIKE :category
        GROUP BY p.Product_ID, p.Title;
    ''')
    data = conn.execute(query,  {'category': category + '%'})
    global product_data
    product_data = []
    for row in data:
        product_info = {
            'product_id': row[0],
            'title': row[1],
            'price': '{:.2f}'.format(row[2]),
            'image': row[3]
        }
        product_data.append(product_info)
    return render_template('productFilter.html', product_data=product_data)

# --------------------------------------- END CUSTOMER -----------------------------------------

if __name__ == '__main__':
    app.run(debug=True)