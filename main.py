# Imports
from flask import Flask, render_template, url_for, request, flash, redirect, jsonify
from flask_wtf import FlaskForm
from flask_login import LoginManager, login_required, login_user, logout_user, current_user, UserMixin
from flask_sqlalchemy import SQLAlchemy
from wtforms import StringField, EmailField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length
from werkzeug import security as s

f_m_s = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(f_m_s)

csrf_token = "fiuh42fuo3htijfm2"
f_m_s.config['SECRET_KEY'] = csrf_token

# Initiating sql database
f_m_s.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///fms_db.db"
db = SQLAlchemy(f_m_s)  # Database instance

@login_manager.user_loader
def load_user(id):
    return Admin.query.get(int(id))


# Database Tables setup.

## User and Admin
class Admin(db.Model, UserMixin):
    """Table for admin."""
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False)


class User(db.Model):
    """Table for Users."""
    __tablename__ = 'user'
    aadhar_no = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(80), nullable=False)
    lname = db.Column(db.String(80), nullable=False)

    bill_no = db.Column(db.Integer, db.ForeignKey("bill.bill_no"))

class Bill(db.Model):
    """Table to store bill details."""
    __tablename__ = 'bill'
    bill_no = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    purchase_total = db.Column(db.Float(), nullable=False)

    aadhar_no = db.Column(db.Integer, db.ForeignKey("user.aadhar_no"))




## Tables for Fertilizer

class Fertilizer_type(db.Model):
    """Table for Fertilizer types."""
    __tablename__ = 'fertilizer_subtype'
    id = db.Column(db.Integer, primary_key=True)
    type_ = db.Column(db.String(80), nullable=False)
    
class Fertilizer_brand(db.Model):
    """Table for Fertilizer brands."""
    __tablename__ = 'fertilizer_brand'
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(80), nullable=False)

class Fertilizer(db.Model):
    """Table for Fertilizers."""
    __tablename__ = 'fertilizer'
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float(), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    
    brand_name = db.Column(db.Integer, db.ForeignKey('fertilizer_brand.id'))
    type_ = db.Column(db.Integer, db.ForeignKey('fertilizer_subtype.id'))

## Tables for Pesticides:
class Pesticide_type(db.Model):
    """Table for pesticide types."""
    __tablename__ = 'pesticide_type'
    id = db.Column(db.Integer,  primary_key=True)
    type_ = db.Column(db.String(80), nullable=False)

class Pesticide_brand(db.Model):
    """Table for pesticide brands."""
    __tablename__ = 'pesticide_brand'
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(80), nullable=False)

class Pesticide(db.Model):
    """Table for pesticides."""
    __tablename__ = 'pesticide'
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float(), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    brand_name = db.Column(db.Integer, db.ForeignKey('pesticide_brand.id'))
    type_ = db.Column(db.Integer, db.ForeignKey('pesticide_type.id'))

# Generating database
with f_m_s.app_context():
    db.create_all()


# Get all admins and users
with f_m_s.app_context():
    admins = Admin.query.all()


# All utility Functions:
def get_brand_id(brand, type):
    """This function returns the brand ID"""
    if type == "Fertilizer" :
        db_brands = Fertilizer_brand.query.all()
        for b in db_brands:
            if b.brand == brand:
                return b.id
    else:
        db_brands = Pesticide_brand.query.all()
        for b in db_brands:
            if b.brand == brand:
                return b.id


def get_sub_type_id(sub_type, type):
    """This function returns the sub_type id"""
    if type == "Fertilizer":
        db_sub_type = Fertilizer_type.query.all()
        for s_t in db_sub_type:
            if s_t.type_ == sub_type:
                return s_t.id 
    else:  
        db_sub_type = Pesticide_type.query.all()
        for s_t in db_sub_type:
            if s_t.type_ == sub_type:
                return s_t.id    


def get_all_brands():
    with f_m_s.app_context():
        brands_list = [b.brand for b in Fertilizer_brand.query.all()] + [ b.brand for b in Pesticide_brand.query.all()]
    print(brands_list)
    return brands_list


def get_all_subtype():
    with f_m_s.app_context():
        sub_type_list = [f_t.type_ for f_t in Fertilizer_type.query.all()] + [p_t.type_ for p_t in Pesticide_type.query.all()]
    print(sub_type_list)
    return sub_type_list


def add_fertilizer_brand():
    new_brand_1 = Fertilizer_brand(brand="Coromandal International Ltd")
    db.session.add(new_brand_1)
    new_brand_2 = Fertilizer_brand(brand="National Fertilizers Ltd")
    db.session.add(new_brand_2)
    new_brand_3 = Fertilizer_brand(brand="Chambal Fertilizers & Chemicals Ltd")
    db.session.add(new_brand_3)
    new_brand_4 = Fertilizer_brand(brand="Rashtriya Chemicals & Fertilizers Ltd")
    db.session.add(new_brand_4)
    new_brand_5 = Fertilizer_brand(brand="Zuari Agro Chemicals Ltd")
    db.session.add(new_brand_5)

    db.session.commit()


def add_pesticide_brand():
    new_brand_1 = Pesticide_brand(brand="UPL Ltd")
    db.session.add(new_brand_1)
    new_brand_2 = Pesticide_brand(brand="BASF India Ltd")
    db.session.add(new_brand_2)
    new_brand_3 = Pesticide_brand(brand="P I Industries Ltd")
    db.session.add(new_brand_3)
    new_brand_4 = Pesticide_brand(brand="Bayer CropScience Ltd")
    db.session.add(new_brand_4)
    new_brand_5 = Pesticide_brand(brand="Sumitomo Chemical India Ltd")
    db.session.add(new_brand_5)

    db.session.commit()


def add_fertilizer_subtype():
    new_subtype_1 = Fertilizer_type(type_ = "Nitrogen")
    new_subtype_2 = Fertilizer_type(type_ = "Phosphorus")
    new_subtype_3 = Fertilizer_type(type_ = "Potassium")

    db.session.add(new_subtype_1)
    db.session.add(new_subtype_2)
    db.session.add(new_subtype_3)

    db.session.commit()


def add_pesticide_subtype():
    new_subtype_1 = Pesticide_type(type_ = "Insecticide")
    new_subtype_2 = Pesticide_type(type_ = "Fungicide")
    new_subtype_3 = Pesticide_type(type_ = "Herbicide")
    new_subtype_4 = Pesticide_type(type_ = "Rodenticide")

    db.session.add(new_subtype_1)
    db.session.add(new_subtype_2)
    db.session.add(new_subtype_3)
    db.session.add(new_subtype_4)

    db.session.commit()


def add_admin():
    """This function adds admin to the database implicitly."""
    new_admin = Admin(user_name="parth.wani@mitaoe.ac.in", password=hash_password("qwerty"))
    db.session.add(new_admin)
    db.session.commit()


def add_fertilizers():
    for i in range(1, 6):
        for j in range(1, 4):
            new_product = Fertilizer(price=round(60 + (2*(i+(1/j))), 2), quantity=20, type_=j, brand_name=i)
            db.session.add(new_product)
            db.session.commit()
    

def add_pesticides():
    for i in range(1, 6):
        for j in range(1, 5):
            new_product = Pesticide(price=round(50 + (2*(i+(1/j))), 2), quantity=20, type_=j, brand_name=i)
            db.session.add(new_product)
            db.session.commit()


def check_if_already_exists(s_type, brand_id, sub_type_id):
    if s_type == "Fertilizer":
        lis = Fertilizer.query.filter_by(brand_name = brand_id, type_ = sub_type_id).all()
    else:
        lis = Pesticide.query.filter_by(brand_name = brand_id, type_ =sub_type_id).all()

    return lis


# Function to hash and check passwords.
def hash_password(password):
    """This function hashes the user password. Converts password to SHA256 hash string with salt of length 8."""
    hashed_password = s.generate_password_hash(password=password, method='pbkdf2:sha256', salt_length=8)
    return hashed_password


def check_hash(user_hash, password):
    """This function checks if the password entered by the user is correct by comparing hashes."""
    check = s.check_password_hash(user_hash, password)
    return check


# Forms:
class signup_user(FlaskForm):
    email = EmailField("Email-ID: ", validators=[DataRequired()])
    password = PasswordField("Create Password: ", validators=[DataRequired()])

class admin_login(FlaskForm):
    email = EmailField("Email-ID: ", validators=[DataRequired()])
    password = PasswordField("Password: ", validators=[DataRequired()])
    signin = SubmitField("Sign In")

class signin_user(FlaskForm):
    email = EmailField("Email-ID: ", validators=[DataRequired()])
    password = PasswordField("Password: ", validators=[DataRequired()])

class product_bill(FlaskForm):
    product_type = SelectField("Product Type: ", validators=[DataRequired()], choices=['Fertilizer', 'Pesticide'])
    brand = SelectField("Brand: ", validators=[DataRequired()], choices=[b for b in get_all_brands()])
    sub_type = SelectField("Sub Type: ", validators=[DataRequired()], choices=[s for s in get_all_subtype()])
    quantity = StringField("Quantity: ", validators=[DataRequired()])
    price = StringField("Price: ", validators=[DataRequired()])
    add = SubmitField("Add", validators=[DataRequired()])


class add_to_db(FlaskForm):
    product_type = SelectField("Product Type: ", validators=[DataRequired()], choices=['Fertilizer', 'Pesticide'])
    brand = SelectField("Brand: ", validators=[DataRequired()], choices=[b for b in get_all_brands()])
    sub_type = SelectField("Sub Type: ", validators=[DataRequired()], choices=[s for s in get_all_subtype()])
    quantity = StringField("Quantity (in kg): ", validators=[DataRequired()])
    add = SubmitField("Add", validators=[DataRequired()])



# Routes:
@f_m_s.route("/")
def home():
    return render_template('index.html', user_logged_in=current_user.is_authenticated)


@f_m_s.route("/asignin",  methods=['GET', 'POST'])
def admin_signin():
    # add_admin ()
    val = True
    form = admin_login()
    admins = Admin.query.all()
    if form.validate_on_submit():
        for admin in admins:
            print(form.email.data, form.password.data)
            if admin.user_name == form.email.data and check_hash(user_hash=admin.password, password=form.password.data):
                val = True
                login_user(admin)
                return redirect(url_for('admin_dashboard', admin_logged_in=current_user.is_authenticated))
            else:
                val = False
        if val == False:
            flash('Invalid Email-ID or password')
    else:
        print("Not validated")
    return render_template("admin_signin.html", form = form)


@f_m_s.route("/admindashboard")
@login_required
def admin_dashboard():
    # add_fertilizer_brand()
    # add_pesticide_brand()
    # add_fertilizer_subtype()
    # add_pesticide_subtype()
    # add_fertilizers()
    # add_pesticides()
    return render_template("admin_dashboard.html", user_logged_in = current_user.is_authenticated)


@f_m_s.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))


@f_m_s.route("/billing-system")
@login_required
def billing_system():
    form = product_bill()
    return render_template('billing_system.html', form=form, user_logged_in=current_user.is_authenticated)

@f_m_s.route("/inventory")
@login_required
def inventory():
    return render_template('inventory.html', user_logged_in=current_user.is_authenticated)

@f_m_s.route("/<type>")
def get_subtype_brand(type):
    sub_type_list = []
    brand_list = []
    
    if type == "fertilizer" or type == "Fertilizer":
        sub_type = Fertilizer_type.query.all()
        brand = Fertilizer_brand.query.all()
    else:
        sub_type = Pesticide_type.query.all()
        brand = Pesticide_brand.query.all()

    print(brand_list)
    for st in sub_type:
        sub_type_list.append(st.type_)
    for br in brand:
        brand_list.append(br.brand)

    add_to_db.brand.choices = brand_list
    add_to_db.sub_type.choices = sub_type_list
    # add_to_db(brand = [b for b in brand_list], sub_type = [t for t in sub_type_list])

    return jsonify({'sub_type': sub_type_list},{'brand': brand_list})


# Database operations
@f_m_s.route("/add-db", methods=['GET', 'POST'])
@login_required
def add_to_db_():
    form = add_to_db()
    if form.validate_on_submit():
        print("validated")
        if form.product_type.data == "Fertilizer":
            br_id = get_brand_id(form.brand.data, "Fertilizer")
            s_id = get_sub_type_id(form.sub_type.data, "Fertilizer")

            check_if_already_exists("Fertilizer", br_id, s_id)[0].quantity += int(form.quantity.data)

        else:
            br_id = get_brand_id(form.brand.data, "Pesticide")
            s_id = get_sub_type_id(form.sub_type.data, "Pesticide")

            check_if_already_exists("Pesticide", br_id, s_id)[0].quantity += int(form.quantity.data)

        db.session.commit()
        flash("Product Added")
        return redirect(url_for('add_to_db_', form=form, user_logged_in= current_user.is_authenticated))
    else:
        print("Not validated")
        print(form.errors)
    return render_template('add_to_db.html', form=form, user_logged_in= current_user.is_authenticated)

@f_m_s.route("/<type>/<brand>/<subtype>", methods=["GET", "POST"])
def get_data(type, brand, subtype):
    print(type, brand, subtype)

    if type =="Fertilizer" or type == "fertilizer":

        br_id = get_brand_id(brand, "Fertilizer")
        s_id = get_sub_type_id(subtype, "Fertilizer")

        search_res = Fertilizer.query.filter_by(brand_name = br_id, type_ = s_id).all()
    else:
        br_id = get_brand_id(brand, "Pesticide")
        s_id = get_sub_type_id(subtype, "Pesticide")
        search_res = Pesticide.query.filter_by(brand_name = br_id, type_ = s_id).all()

    
    return jsonify({'quantity': search_res[0].quantity, 'price': search_res[0].price})

@f_m_s.route("/get_price/<type>/<brand>/<subtype>/<quantity>", methods=["GET", "POST"])
def get_price(type, brand, subtype, quantity):

    if type =="Fertilizer" or type == "fertilizer":

        br_id = get_brand_id(brand, "Fertilizer")
        s_id = get_sub_type_id(subtype, "Fertilizer")

        search_res = Fertilizer.query.filter_by(brand_name = br_id, type_ = s_id).all()

        f = Fertilizer.query.filter_by(brand_name = br_id, type_ = s_id).first()
        f.quantity -= float(quantity)
        db.session.commit()

    else:
        br_id = get_brand_id(brand, "Pesticide")
        s_id = get_sub_type_id(subtype, "Pesticide")

        search_res = Pesticide.query.filter_by(brand_name = br_id, type_ = s_id).all()

        f = Pesticide.query.filter_by(brand_name = br_id, type_ = s_id).first()
        f.quantity -= float(quantity)
        db.session.commit()
    
    if  float(search_res[0].quantity) - float(quantity) < 20:
            return []
    
    return jsonify({'price': search_res[0].price})

@f_m_s.route('/add-back/<quantity>/<subtype>/<brand>/<type>', methods=['GET', 'POST'])
def add_back(quantity, subtype, brand, type):
    print(quantity, type, brand, subtype)
    if type =="Fertilizer" or type == "fertilizer":

        br_id = get_brand_id(brand, "Fertilizer")
        s_id = get_sub_type_id(subtype, "Fertilizer")

        f = Fertilizer.query.filter_by(brand_name = br_id, type_ = s_id).first()
        f.quantity += float(quantity)
        db.session.commit()
    else:

        br_id = get_brand_id(brand, "Pesticide")
        s_id = get_sub_type_id(subtype, "Pesticide")

        f = Pesticide.query.filter_by(brand_name = br_id, type_ = s_id).first()
        f.quantity += float(quantity)
        db.session.commit()

    return jsonify({"ret_val":f.quantity})


@f_m_s.route("/search-db")
@login_required
def search_in_db():

    return render_template('search_in_db.html', user_logged_in=current_user.is_authenticated)



if __name__ == '__main__':
    with f_m_s.app_context():
        f_m_s.run(debug=True)




