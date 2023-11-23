from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:odegaard@localhost/aircraft_manufacturing'
db = SQLAlchemy(app)

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    mail_id = db.Column(db.String(255))
    dob = db.Column(db.String(50))
    age = db.Column(db.Integer)
    mobile = db.Column(db.Integer)
    name = db.Column(db.String(50))


class AircraftModel(db.Model):
    model_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    model_name = db.Column(db.String(255), nullable=False)
    manufacturer = db.Column(db.String(255), nullable=False)
    capacity = db.Column(db.Integer)
    max_range = db.Column(db.Integer)
    mtow = db.Column(db.Integer)


class AircraftComponent(db.Model):
    component_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    component_name = db.Column(db.String(255), nullable=False)
    manufacturer = db.Column(db.String(255), nullable=False)
    weight = db.Column(db.Integer)
    cost = db.Column(db.Integer)
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.supplier_id'))
    supplier = db.relationship('Supplier', backref='components')

class Supplier(db.Model):
    supplier_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    contact_info = db.Column(db.String(255), nullable=False)
    components = db.relationship('AircraftComponent', backref='supplier')
    inventories = db.relationship('ComponentInventory', backref='supplier')

class Employee(db.Model):
    employee_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fullname = db.Column(db.String(255), nullable=False)
    position = db.Column(db.String(255), nullable=False)
    contact_info = db.Column(db.String(255), nullable=False)

class ProductionLine(db.Model):
    line_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    line_name = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(255), nullable=False)
    capacity = db.Column(db.Integer)
    supervisor_id = db.Column(db.Integer, db.ForeignKey('employee.employee_id'))
    supervisor = db.relationship('Employee', backref='lines')

class AircraftOrder(db.Model):
    order_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.customer_id'))
    customer = db.relationship('Customer', backref='orders')
    date_placed = db.Column(db.Date, nullable=False)
    order_status = db.Column(db.String(255))
    total_cost = db.Column(db.Integer)

class Customer(db.Model):
    customer_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_name = db.Column(db.String(255), nullable=False)
    contact_info = db.Column(db.String(255), nullable=False)
    orders = db.relationship('AircraftOrder', backref='customer')
    inventories = db.relationship('ComponentInventory', backref='customer')

class ComponentInventory(db.Model):
    inventory_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    component_id = db.Column(db.Integer, db.ForeignKey('aircraft_component.component_id'))
    component = db.relationship('AircraftComponent', backref='inventories')
    quantity = db.Column(db.Integer)
    location = db.Column(db.String(255))
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.supplier_id'))
    expiration_date = db.Column(db.Date)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.customer_id'))


# Routes for User Registration and Profile
@app.route('/')
def home():
    return render_template('sign_up.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Process registration form data and add a new player to the database
        username = request.form.get('username')
        email = request.form.get('email')
        phnumber = request.form.get('phnumber')
        age = request.form.get('Age')
        dob = request.form.get('dob')

        new_player = User(
            mail_id=email,
            dob=dob,
            age=age,
            mobile=phnumber,
            naame=username
        )

        db.session.add(new_player)
        db.session.commit()

        return redirect(url_for('sign_up.html'))

    return render_template('sign_up.html')

if __name__ == '__main__':
    #db.create_all()  # Create database tables before running the app
    app.run(debug=True)
