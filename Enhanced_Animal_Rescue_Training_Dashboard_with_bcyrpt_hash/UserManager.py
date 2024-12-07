#!/usr/bin/env python
# coding: utf-8

# In[ ]:
import bcrypt
from pymongo import MongoClient
from bson.objectid import ObjectId
from AnimalShelters import AnimalShelter

class UserManager:
    # Handles user registration and validation for MongoDB

    def __init__(self):
        
        # Connection Variables
        HOST = 'localhost'
        PORT = 27017
        DB = 'AAC'
        USERS = 'users'        
        AUTH_DB = 'AAC'
        
        # Initialize Connection 
        
        self.client = MongoClient(f'mongodb://{HOST}:{PORT}/{DB}')
        self.database = self.client[DB]
        
        # collection
        self.users_collection= self.database[USERS]

    def register_user(self, username, password):
        # Register a new user if username does not already exist
        if not username or not password:
            raise ValueError("Username and password cannot be empty.")
        
        # Check if user already exists
        if self.users_collection.find_one({"username": username}):
            return "Username already exists"
        # Hash the password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        # Insert new user to users collection
        registered = self.users_collection.insert_one({"username": username, "password": hashed_password})
        
        if registered.inserted_id:
            try: # to create MongoDB credential
                result = self.client['AAC'].command(
                    "createUser", 
                    username, 
                    pwd=password, 
                    roles=[{"role": "readWrite", "db": "AAC"}]
                )
                print("CreateUser result: {}".format(result)) 
                return "User {} registered and created successfully".format(username)
            except Exception as e:
                print("Error creating user: {}".format(str(e)))
                return "Failed to create user in MongoDB: {}".format(str(e))
        
        else: 
            return "Failed to register user"
    
    def validate_user(self, username, password):
        # Validate an existing user's credentials
        user = self.users_collection.find_one({"username": username})
        
        if user and bcrypt.checkpw(password.encode('utf-8'), user["password"]):
            # Return an instance of AnimalShelter on successful validation
            return AnimalShelter(username, password)
        else:
            return "Invalid username or password"

