from traceback import print_tb
from flask import render_template, request, redirect, session
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.user import User
from flask_app.models.recipe import Recipe
from flask_app import app
from flask_bcrypt import Bcrypt
from flask import flash

bcrypt = Bcrypt(app)


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/register', methods=['POST'])
def register():
    if not User.validate_registration(request.form):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": pw_hash
        }
    user_id = User.save(data)
    print(user_id)
    session['user_id'] = user_id
    session['first_name'] = data['first_name']
    session['last_name'] = data['last_name']
    return redirect('/dashboard')

@app.route('/login', methods=['POST'])
def login():
    data = { 
        "email" : request.form["email"] 
        }
    user = User.get_by_email(data)
    if not user:
        flash(u"Invalid Email/Password", 'login error')
        return redirect("/")
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash(u"Invalid Email/Password", 'login error')
        return redirect('/')
    session['user_id'] = user.id
    session['first_name'] = user.first_name
    session['last_name'] = user.last_name
    return redirect('/dashboard')

@app.route('/log-out')
def clear():
    session.clear()
    return redirect('/')

@app.route('/dashboard')
def show():
    id = session['user_id']
    all_recipes = Recipe.get_all(id)
    return render_template("dashboard.html", all_recipes=all_recipes)


@app.route('/new-recipe')
def new_recipe():
    if session.get("user_id") == None:
        return redirect('/')
    return render_template("add_recipe.html")

@app.route('/add_recipe', methods=['POST'])
def add_recipe():
    if not Recipe.validate_recipe(request.form):
        return redirect('/new-recipe')
    data = {
        "name": request.form['name'],
        "description": request.form['description'],
        "ingredients": request.form['ingredients'],
        "directions": request.form['directions'],
        "date_made": request.form['date_made'],
        "under_thirty": request.form['under_thirty'],
        "user_id": session['user_id']
        }
    Recipe.save(data)
    return redirect('/dashboard')

@app.route('/edit/<int:id>')
def show_recipe(id):
    if session.get("user_id") == None:
        return redirect('/')
    recipe = Recipe.get_one(id)
    return render_template("edit_recipe.html", recipe=recipe)

@app.route('/edit_recipe/<int:id>', methods=['POST'])
def edit_recipe(id):
    if not Recipe.validate_recipe(request.form):
        return redirect(f'/edit/{id}')
    data = {
        "id": id,
        "name": request.form['name'],
        "description": request.form['description'],
        "ingredients": request.form['ingredients'],
        "directions": request.form['directions'],
        "date_made": request.form['date_made'],
        "under_thirty": request.form['under_thirty'],
        "user_id": session['user_id']
    }
    Recipe.edit(data)
    return redirect(f'/recipe/{id}')

@app.route('/recipe/<int:id>')
def view_recipe(id):
    if session.get("user_id") == None:
        return redirect('/')
    recipe = Recipe.get_one(id)
    print(recipe.date_made)
    return render_template("recipe.html", recipe=recipe)

@app.route('/delete/<int:id>')
def delete_recipe(id):
    Recipe.delete(id)
    return redirect('/dashboard')
