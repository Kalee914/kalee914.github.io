#############################################################
# CS340 : CRUD Module
# KaLee Li 
# Prof.Kellogg
#############################################################

#!/usr/bin/env python
# coding: utf-8

# In[2]:


from pymongo import MongoClient
from bson.objectid import ObjectId

class AnimalShelter(object):
    """ CRUD operations for Animal collection in MongoDB """
    
    def __init__(self, username, password):
        
        # Connection Variables
        HOST = 'localhost'
        PORT = 27017
        DB = 'AAC'
        ANIMALS = 'animals'
        
        AUTH_DB = 'AAC'
        
        # Initialize Connection 
        self.client = MongoClient(f'mongodb://{HOST}:{PORT}')
        self.database = self.client[DB]
        
        self.username = username
        # matching user name in the users collection
        user_credentials = self.database['users'].find_one({'username': username})
        
        if user_credentials:
            password = user_credentials['password']
            # Authenticate using the retrieved credentials
            self.client = MongoClient(f'mongodb://{self.username}:{password}@{HOST}:{PORT}/{DB}?authSource={AUTH_DB}')
            self.database = self.client[DB]
        else:
            raise Exception("User not found in the users collection.")   
            
        # collection
        self.animals_collection = self.database[ANIMALS]


    # Create method to implement the C in CRUD
    
    def create(self, data):
        if data is not None:
            successfulInsert = self.animals_collection.insert(data)  
            if successfulInsert is not None:
                return True
            return False            
        else:
            raise Exception("Nothing to save because the data parameter is empty")

    # Read method to implement the R in CRUD
    
    def read(self, *args): # *args to pass a number of arguments
        
        query = {} #empty dictionary to combine search criteria 
        for arg in args:
            query.update(arg) 
        
        results = list(self.animals_collection.find(query))
        return results
            
    # Update Method to implement the R in CRUD 
    
    def update(self, *args, **kwargs):
        
        findExistData = {}  # Empty dictionary to combine search criteria
        setUpdate = {}

        for search in args:
            findExistData.update(search)

        for newData in kwargs.items():
            setUpdate.update({newData[0]: newData[1]})

        if findExistData is not None:
            updated_result = self.animals_collection.update_many(findExistData, {"$set": setUpdate})
            modified_count = updated_result.raw_result.get('nModified', 0)
            print(f"Number of modified documents: {modified_count}")
            return updated_result.raw_result 
        else:
            raise Exception("Nothing to update because the search criteria is empty")
            
    # Delete Method to implement the D in CRUD
    
    def delete(self, removeData):
        if removeData is not None:
            deleteData = self.animals_collection.delete_many(removeData)
            deleted_count = deleteData.raw_result.get('n', 0)  
            print(f"Number of deleted documents: {deleted_count}")
            return deleteData.raw_result
        else:
            raise Exception("Nothing to delete because the search criteria is empty")
