
from flask import render_template,redirect,url_for,flash,request
from grocerylist import app, db, bcrypt
from grocerylist.forms import RegistrationForm,LoginForm,AddItemForm,UpdateAccountForm
from grocerylist.models import User, Items
from flask_login import login_user,logout_user,login_required,current_user

@app.route("/")
@app.route("/home", methods=['POST', 'GET'])
def home():
    items = Items.query.all()  
    return render_template('home.html', title='home', items=items)


@app.route("/about")
def about():
    return render_template('about.html',title='about',email="yug.somdagar11@gmail.com")

@app.route("/register",methods=['POST','GET'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username = form.username.data, email = form.email.data, password = hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created..','success')
        return redirect(url_for('login'))
    return render_template('register.html',title='register',form = form)

@app.route("/login",methods=['POST','GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user,remember= form.remember.data)
            next_page = request.args.get('next')
            flash('You have been logged in','success')
            return redirect(next_page) if next_page else redirect(url_for('home'))  
        else:
            flash('Login Unsuccessful' , 'danger')
    return render_template('login.html',title='login',form = form)

@app.route("/logout",methods=['POST','GET'])
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/account", methods=['POST', 'GET'])
def account():
    form = UpdateAccountForm()

    if form.validate_on_submit():
        if form.email.data:  # Check if email is not empty
            current_user.email = form.email.data
        else:
            flash('Email cannot be empty!', 'danger')
            return redirect(url_for('account'))

        if form.username.data:  # Check if username is not empty
            current_user.name = form.username.data
        else:
            flash('Username cannot be empty!', 'danger')
            return redirect(url_for('account'))

        db.session.commit()
        flash('Your account has been updated', 'success')
        return redirect(url_for('account'))
    
    return render_template('account.html', form=form)



@app.route("/new_item/new",methods=['POST','GET'])
@login_required
def new_item():
    form = AddItemForm()
    if form.validate_on_submit():
        item = Items(name = form.name.data, quantity = form.quantity.data, category = form.category.data)
        db.session.add(item)
        db.session.commit()
        flash('Item addedd ','success')
        return redirect(url_for('home'))
    return render_template('new_item.html',title='new item',legend = 'Add new item',form = form)

@app.route("/new_item/<int:item_id>")
def item(item_id):
    item = Items.query.get_or_404(item_id)
    return render_template("item.html",item = item, name = item.name, quantity = item.quantity, category = item.category)


@app.route("/item/<int:item_id>/edit",methods=['POST','GET'])
@login_required
def edit_item(item_id):
    item = Items.query.get_or_404(item_id)
    form = AddItemForm()
    if form.validate_on_submit():
        item.name = form.name.data
        item.quantity = form.quantity.data
        item.category = form.category.data
        db.session.commit()
        flash('Item edited!','success')
        return redirect(url_for('item',item_id = item.id))
    elif request.method == 'GET':
        form.name.data = item.name
        form.quantity.data = item.quantity
        form.category.data = item.category

    return render_template("new_item.html",title = 'Edit item',legend = 'Edit Item',form = form)

@app.route("/item/<int:item_id>/delete", methods=['POST'])
@login_required
def delete_item(item_id):
    item = Items.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    flash('Item deleted!', 'success')
    return redirect(url_for('home'))






