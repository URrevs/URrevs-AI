from .fill_db import create_user
from recommenderApi.imports import MongoClient, certifi, ObjectId
from recommenderApi.settings import MONGODB_LINK

def check_new_user(userId: str):
    try:
        userId = ObjectId(userId)
        cluster = MongoClient(MONGODB_LINK, tlsCAFile=certifi.where())
        
        db = cluster['urrevs']
        users_col = db['users']

        user = users_col.find_one({'_id': userId})
        create_user(id=str(user['_id']), name=user['name'])
        return True, user
    except:
        return False, []
