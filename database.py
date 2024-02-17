from pymongo import MongoClient
from dotenv import load_dotenv
import os
from bson import ObjectId


load_dotenv()

mongodb_password = os.getenv("MONGODB_PASSWORD")

class MongoDBHandler:
    def __init__(self):
        self.client = MongoClient(f'mongodb+srv://durmatekin22:{mongodb_password}@cluster0.ysg4er0.mongodb.net/')
        self.database=self.client['library']
        self.collection=self.database['books']
        
        
    def add_book_database(self,book_data):
        self.collection.insert_one(book_data)
        
    def get_all_books_data(self):
        # print(list(self.collection.find()))
        data=list(self.collection.find())
        print(data)
        return data
        
    def data_length(self):
        data=list(self.collection.find())
        return int(len(data))
    
    def remove_data_index(self,index):
        all_books = self.get_all_books_data()
        if 0<=index<len(all_books):
            #belgeyi sil
            removed_book=all_books.pop(index)
            self.collection.delete_one({'_id':removed_book['_id']})
            print(f"Belge silindi : {removed_book}")
        else:
            print("Geçersiz İndex Numarası Gönderildi")
             
    def all_remove_books(self):
        self.collection.delete_many({})
