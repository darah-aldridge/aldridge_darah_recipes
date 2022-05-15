import email
import imp, re
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
from flask_app import app
from flask_app.models.recipe import Recipe

from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)


db ="recipes"
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r"^[A-Za-z]+$") 

class User:
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']  
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.recipe_list = []
    @staticmethod
    def validate_registration(form_data):
        is_valid = True
        if not EMAIL_REGEX.match(form_data['email']): 
            flash(u"Invalid email address!", 'register error')
            is_valid = False
        if len(form_data['first_name']) < 2:
            flash(u"First name must be at least 2 characters.", 'register error')
            is_valid = False
        if not form_data['first_name']:
            flash(u"You must include a first name.", 'register error')
            is_valid = False
        if not NAME_REGEX.match(form_data['first_name']):
            flash(u"You can only use letters for your first name.", 'register error')
            is_valid = False
        if len(form_data['last_name']) < 2:
            flash(u"Last name must be at least 2 characters.", 'register error')
            is_valid = False
        if not form_data['last_name']:
            flash(u"You must include a last name.", 'register error')
            is_valid = False
        if not NAME_REGEX.match(form_data['last_name']):
            flash(u"You can only use letters for your last name.", 'register error')
            is_valid = False
        if not form_data['email']:
            flash(u"You must include an email.", 'register error')
            is_valid = False
        if not form_data['password']:
            flash(u"You must include an password.", 'register error')
            is_valid = False
        if User.get_by_email({'email': form_data['email']}):
            flash(u"Email address is already in use!", 'register error')
            is_valid=False
        if form_data['password'] != form_data['confirm_password']:
            flash(u"Passwords don't match!", 'register error')
            is_valid=False
        if len(form_data['password']) < 8:
            flash(u"Password must be at least 8 characters.", 'register error')
            is_valid = False
        return is_valid

    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        return connectToMySQL(db).query_db( query, data )  

    @classmethod
    def check(cls, email, password):
        print(email, password)
        query  = "SELECT * FROM users WHERE password = %(password)s && email = %(email)s;"
        results = connectToMySQL(db).query_db(query)
        if results:
            return cls(results[0])
        else:
            return False
    
    @classmethod
    def login(cls, data):
        print(data)
        query  = "SELECT * FROM users WHERE password = %(password)s && email = %(email)s;"
        results = connectToMySQL(db).query_db(query)
        if results:
            return cls(results[0])
        else:
            return False
        
    @classmethod
    def get_by_email(cls, email):
        query  = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(db).query_db(query, email)
        # print(results)
        if len(results) < 1:
            return False
        if results:
            return cls(results[0])
        else:
            return False
    
    @classmethod
    def get_one_user_with_recipes(cls):
        # query = f"SELECT * FROM recipes LEFT JOIN users ON users.id = recipes.user_id WHERE recipes.user_id = {user_id};"
        query = f"SELECT * FROM recipes LEFT JOIN users ON users.id = recipes.user_id;"
        results = connectToMySQL(db).query_db(query)
        userWithrecipes = False
        for row in results:
            data = {
                "id": row['id'],
                "name": row['name'],
                "description": row['description'],
                "under_thirty": row['under_thirty'],
                "ingredients": row['ingredients'],
                "directions": row['directions'],
                "date_made": row['date_made'],
                "user_id": row['user_id'],
            }
            userWithrecipes.recipe_list.append(Recipe(data))
        return userWithrecipes