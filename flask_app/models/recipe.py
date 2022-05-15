from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import app
from datetime import datetime

db ="recipes"

class Recipe:
    def __init__( self , data ):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.under_thirty = data['under_thirty']
        self.ingredients = data['ingredients']
        self.directions = data['directions']
        self.date_made = data['date_made'].strftime("%Y-%m-%d")
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
    @staticmethod
    def validate_recipe(form_data):
        is_valid = True
        if len(form_data['name']) < 3:
            flash(u"Name must be at least 3 characters.", 'recipe error')
            is_valid = False
        if len(form_data['description']) < 3:
            flash(u"Description must be at least 3 characters.", 'recipe error')
            is_valid = False
        if len(form_data['ingredients']) < 3:
            flash(u"ingredients must be at least 3 characters.", 'recipe error')
            is_valid = False
        if len(form_data['directions']) < 3:
            flash(u"Directions must be at least 3 characters.", 'recipe error')
            is_valid = False
        if not form_data['name']:
            flash(u"Name is required", 'recipe error')
            is_valid = False
        if not form_data['description']:
            flash(u"Description is required", 'recipe error')
            is_valid = False
        if not form_data['ingredients']:
            flash(u"ingredients are required", 'recipe error')
            is_valid = False
        if not form_data['directions']:
            flash(u"Directions are required", 'recipe error')
            is_valid = False
        return is_valid

    @classmethod
    def save(cls, data):
        query = "INSERT INTO recipes (name, description, under_thirty, ingredients, directions, date_made, user_id) VALUES (%(name)s, %(description)s, %(under_thirty)s, %(ingredients)s, %(directions)s, %(date_made)s, %(user_id)s);"
        return connectToMySQL(db).query_db(query, data)  

    @classmethod
    def delete(cls, id):
        query  = f"DELETE FROM recipes WHERE id = {id};"
        return connectToMySQL(db).query_db(query)
    
    @classmethod
    def edit(cls, data):
        query  = f"UPDATE recipes SET name =%(name)s, description = %(description)s, under_thirty = %(under_thirty)s, ingredients = %(ingredients)s, directions = %(directions)s, date_made = %(date_made)s WHERE id = %(id)s;"
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def get_one(cls, id):
        query  = "SELECT * FROM recipes WHERE id = %(id)s;"
        result = connectToMySQL(db).query_db(query, {'id':id})
        print(result)
        return cls(result[0])

    @classmethod
    def get_all(cls, id):
        query  = f"SELECT * FROM recipes;"
        results = connectToMySQL(db).query_db(query)
        recipes = []
        for recipe in results:
            recipes.append(cls(recipe))
        return recipes