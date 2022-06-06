from flask import flash

from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user


class Name:
    def __init__(self, data):
        self.id = data["id"]
        self.name = data["name"]
        self.meaning = data["meaning"]
        self.origin = data["origin"]
        self.pronounciation = data["pronounciation"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        
        if "user" in data: # if user exists as a key, then data contains user object
            self.user = data["user"]
            
        else: # otherwise, it contains user_id only 
            self.user = user.User.get_by_id({"id": data["user_id"]})
            
        
    # create
    @classmethod
    def create(cls, data):
        query = "INSERT INTO names (user_id, name, meaning, origin, pronounciation, created_at, updated_at) VALUES (%(user_id)s, %(name)s, %(meaning)s, %(origin)s, %(pronounciation)s, NOW(), NOW());"

# returns the ID of the newly created name
        return connectToMySQL("name_schema").query_db(query, data)
    # read many
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM names;"
        results = connectToMySQL("name_schema").query_db(query)
        
        names = []
        for row in results:
            names.append(cls(row))
            
        return names
    
    # read one
    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM names WHERE id = %(id)s;"
        results = connectToMySQL("name_schema").query_db(query, data)
        
        if len(results) < 1:
            return False
        
        
        return cls(results[0])

    # update
    @classmethod
    def update(cls, data):
        query = "UPDATE names SET name = %(name)s, meaning = %(meaning)s, origin = %(origin)s, pronounciation = %(pronounciation)s, updated_at = NOW() WHERE id = %(id)s;"
    
        return connectToMySQL("name_schema").query_db(query, data)
    
    #delete
    @classmethod
    def delete(cls, data):
        query = "DELETE FROM names WHERE id = %(id)s;"
        
        connectToMySQL("name_schema").query_db(query, data)

        
    @staticmethod
    def validate(post_data):
        is_valid = True
        
        if len(post_data["name"]) < 2:
            flash("Name must be at least 2 characters.")
            is_valid = False
            
        if len(post_data["meaning"]) < 2:
            flash("meaning must be at least 2 characters.")
            is_valid = False
            
        if len(post_data["origin"]) < 2:
            flash("origin must be at least 8 characters.")
            is_valid = False
            
        if len(post_data["pronounciation"]) < 2:
            flash("pronounciation must be at least 8 characters.")
            is_valid = False
        
        return is_valid
    
        
        