from recommender.models import Mobile
from recommenderApi.imports import MongoClient, certifi, dt, ObjectId
from recommenderApi.settings import MONGODB_LINK, MONGODB_NAME, ROUND_NUM_OF_REVIEWS
from recommender.sqliteDB.data import SQLite_Database

class MongoConnection:
    def __init__(self, mongodb_link: str = MONGODB_LINK, mongodb_name: str = MONGODB_NAME):
        self.db = self.connect_to_mongo(mongodb_link, mongodb_name)
        return None
    
    def connect_to_mongo(self, mongodb_link: str = MONGODB_LINK, mongodb_name: str = MONGODB_NAME):
        client = MongoClient(mongodb_link, tlsCAFile=certifi.where())
        self.db = client[mongodb_name]
        return self.db
    
    def check_new_user_mongo(self, userId: str):
        try:
            userId = ObjectId(userId)
            users_col = self.db['users']
            user = users_col.find_one({'_id': userId}, {'_id': 1, 'name': 1})
            SQLite_Database().create_new_user(id=str(user['_id']), name=user['name'])
            return True, user
        except:
            return False, []

    def get_users_mongo(self, date: dt):
        users_col = self.db['users']
        users = users_col.find({'createdAt': {'$gte': date}}, {'_id': 1, 'name': 1})
        return users

    def get_product_reviews_mongo(self, date: dt):
        prevs_col = self.db['prevs']
        projection = {
            '_id': 1, 'user': 1, 'phone': 1, 'pros': 1, 'cons': 1, 'createdAt': 1, 'generalRating': 1,
            'uiRating': 1, 'manQuality': 1, 'valFMon': 1, 'camera': 1, 'callQuality': 1, 'batteryRating': 1
        }
        prevs = prevs_col.find({'createdAt': {'$gte': date}}, projection)
        return prevs

    def get_company_reviews_mongo(self, date: dt):
        crevs_col = self.db['crevs']
        projection = {
            '_id': 1, 'user': 1, 'company': 1, 'pros': 1, 'cons': 1, 'createdAt': 1, 'generalRating': 1
        }
        crevs = crevs_col.find({'createdAt': {'$gte': date}}, projection)
        return crevs

    def get_companies_mongo(self):
        companies_col = self.db['companies']
        companies = companies_col.find({}, {'_id': 1, 'nameLower': 1})
        return companies

    def get_phones_mongo(self, date: dt):
        phones_col = self.db['nphones']
        projection = {
            '_id': 1, 'name': 1, 'company': 1, 'price': 1, 'releaseDate': 1, 'length': 1, 'width': 1,
            'height': 1, 'network': 1, 'weight': 1, 'sim': 1, 'screenType': 1, 'screenSize': 1,
            'screen2bodyRatio': 1, 'resolutionLength': 1, 'resolutionWidth': 1, 'resolutionDensity': 1,
            'screenProtection': 1, 'os': 1, 'chipset': 1, 'cpu': 1, 'gpu': 1, 'intMem': 1, 'mainCam': 1,
            'selfieCam': 1, 'hasLoudspeaker': 1, 'hasStereo': 1, 'has3p5mm': 1, 'wlan': 1, 'hasNfc': 1,  
            'bluetoothVersion': 1, 'radio': 1, 'usbType': 1, 'usbVersion': 1, 'hasGyro': 1, 'hasProximity': 1,
            'fingerprintDetails': 1, 'batteryCapacity': 1, 'hasPastCharging': 1, 'chargingPower': 1,
            'createdAt': 1, 'updatedAt': 1
        }
        phones = phones_col.find({'createdAt': {'$gte': date}}, projection)
        return phones

    def get_product_reviews_likes_mongo(self, date: dt):
        prevs_likes_col = self.db['prevslikes']
        likes = prevs_likes_col.find({'updatedAt': {'$gte': date}, 'unliked': False}, {'_id': 0, 'user': 1, 'review': 1})
        # check if this like is new or not
        # add identifier to the like
        likes_lst: list = []
        for like in likes:
            likes_lst.append({'id': str(like['user']), 'review': f"0{like['review']}"})
        return likes_lst
    
    def get_company_reviews_likes_mongo(self, date: dt):
        crevs_likes_col = self.db['crevslikes']
        likes = crevs_likes_col.find({'createdAt': {'$gte': date}, 'unliked': False}, {'_id': 0, 'user': 1, 'review': 1})
        # check if this like is new or not
        # add identifier to the like
        likes_lst: list = []
        for like in likes:
            likes_lst.append({'id': str(like['user']), 'review': f"1{like['review']}"})
        return likes_lst

    def get_product_reviews_unlikes_mongo(self, date: dt):
        prevs_unlikes_col = self.db['prevsunlikes']
        unlikes = prevs_unlikes_col.find({'createdAt': {'$gte': date}}, {'_id': 0, 'user': 1, 'review': 1})
        # check if this unlike is new or not
        # add identifier to the unlike
        unlikes_lst: list = []
        for unlike in unlikes:
            unlikes_lst.append({'id': str(unlike['user']), 'review': f"0{unlike['review']}"})
        return unlikes_lst

    def get_company_reviews_unlikes_mongo(self, date: dt):
        crevs_unlikes_col = self.db['crevsunlikes']
        unlikes = crevs_unlikes_col.find({'createdAt': {'$gte': date}}, {'_id': 0, 'user': 1, 'review': 1})
        # check if this unlike is new or not
        # add identifier to the unlike
        unlikes_lst: list = []
        for unlike in unlikes:
            unlikes_lst.append({'id': str(unlike['user']), 'review': f"1{unlike['review']}"})
        return unlikes_lst
        # return unlikes

    def get_product_reviews_comments_mongo(self, date: dt):
        prevs_comments_col = self.db['prevscomments']
        comments = prevs_comments_col.find({'createdAt': {'$gte': date}}, {'_id': 0, 'user': 1, 'review': 1})
        # add identifier to the comment
        comments_lst: list = []
        for comment in comments:
            comments_lst.append({'id': str(comment['user']), 'review': f"0{comment['review']}"})
        return comments_lst
        # return comments

    def get_company_reviews_comments_mongo(self, date: dt):
        crevs_comments_col = self.db['crevscomments']
        comments = crevs_comments_col.find({'createdAt': {'$gte': date}}, {'_id': 0, 'user': 1, 'review': 1})
        # add identifier to the comment
        comments_lst: list = []
        for comment in comments:
            comments_lst.append({'id': str(comment['user']), 'review': f"1{comment['review']}"})
        return comments_lst
        # return comments

    def get_product_reviews_seemores_mongo(self, date: dt):
        prevs_seemores_col = self.db['prevsseemores']
        seemores = prevs_seemores_col.find({'updatedAt': {'$gte': date}}, {'_id': 0, 'user': 1, 'review': 1})
        # add identifier to the seemore
        seemores_lst: list = []
        for seemore in seemores:
            seemores_lst.append({'id': str(seemore['user']), 'review': f"0{seemore['review']}"})
        return seemores_lst
        # return seemores

    def get_company_reviews_seemores_mongo(self, date: dt):
        crevs_seemores_col = self.db['crevsseemores']
        seemores = crevs_seemores_col.find({'updatedAt': {'$gte': date}}, {'_id': 0, 'user': 1, 'review': 1})
        # add identifier to the seemore
        seemores_lst: list = []
        for seemore in seemores:
            seemores_lst.append({'id': str(seemore['user']), 'review': f"1{seemore['review']}"})
        return seemores_lst
        # return seemores

    def get_product_reviews_fullscreens_mongo(self, date: dt):
        prevs_fullscreens_col = self.db['prevsfullscreens']
        fullscreens = prevs_fullscreens_col.find({'updatedAt': {'$gte': date}}, {'_id': 0, 'user': 1, 'review': 1})
        # add identifier to the fullscreen
        fullscreens_lst: list = []
        for fullscreen in fullscreens:
            fullscreens_lst.append({'id': str(fullscreen['user']), 'review': f"0{fullscreen['review']}"})
        return fullscreens_lst
        # return fullscreens

    def get_company_reviews_fullscreens_mongo(self, date: dt):
        crevs_fullscreens_col = self.db['crevsfullscreens']
        fullscreens = crevs_fullscreens_col.find({'updatedAt': {'$gte': date}}, {'_id': 0, 'user': 1, 'review': 1})
        # add identifier to the fullscreen
        fullscreens_lst: list = []
        for fullscreen in fullscreens:
            fullscreens_lst.append({'id': str(fullscreen['user']), 'review': f"1{fullscreen['review']}"})
        return fullscreens_lst
        # return fullscreens

    def get_product_reviews_hates_mongo(self, date: dt):
        prevs_hates_col = self.db['prevshates']
        hates = prevs_hates_col.find({'updatedAt': {'$gte': date}}, {'_id': 0, 'user': 1, 'review': 1})
        # add identifier to the hate
        hates_lst: list = []
        for hate in hates:
            hates_lst.append({'id': str(hate['user']), 'review': f"0{hate['review']}"})
        return hates_lst
        # return hates

    def get_company_reviews_hates_mongo(self, date: dt):
        crevs_hates_col = self.db['crevshates']
        hates = crevs_hates_col.find({'updatedAt': {'$gte': date}}, {'_id': 0, 'user': 1, 'review': 1})
        # add identifier to the hate
        hates_lst: list = []
        for hate in hates:
            hates_lst.append({'id': str(hate['user']), 'review': f"1{hate['review']}"})
        return hates_lst
        # return hates

    def update_all_fixed_data_mongo(self, date:dt):
        sqlite = SQLite_Database()
        users = self.get_users_mongo(date)
        for user in users:
            sqlite.create_new_user_ifNotExist(user)
        companies = self.get_companies_mongo()
        for company in companies:
            sqlite.create_new_company_ifNotExist(company)
        mobiles = self.get_phones_mongo(date)
        for mobile in mobiles:
            sqlite.create_new_mobile_ifNotExist(mobile)
        reviews = self.get_product_reviews_mongo(date)
        for review in reviews:
            sqlite.create_new_Preview_ifNotExist(review)
        reviews = self.get_company_reviews_mongo(date)
        for review in reviews:
            sqlite.create_new_Creview_ifNotExist(review)
        print('finish adding all users, companies and mobiles')

    def get_all_items_trackers_mongo(self, date: dt):
        trackers = {
            'product': {
                'LIKE': self.get_product_reviews_likes_mongo(date),
                'UNLIKE': self.get_product_reviews_unlikes_mongo(date),
                'COMMENT': self.get_product_reviews_comments_mongo(date),
                'SEE_MORE': self.get_product_reviews_seemores_mongo(date),
                'FULL_SCREEN': self.get_product_reviews_fullscreens_mongo(date),
                'DONT_LIKE': self.get_product_reviews_hates_mongo(date)
            },
            'company': {
                'LIKE': self.get_company_reviews_likes_mongo(date),
                'UNLIKE': self.get_company_reviews_unlikes_mongo(date),
                'COMMENT': self.get_company_reviews_comments_mongo(date),
                'SEE_MORE': self.get_company_reviews_seemores_mongo(date),
                'FULL_SCREEN': self.get_company_reviews_fullscreens_mongo(date),
                'DONT_LIKE': self.get_company_reviews_hates_mongo(date)
            }
        }
        return trackers

    def get_phone_profile_visit_mongo(self, date: dt):
        profile_visits_col = self.db['phoneprofilevisits']
        visits = profile_visits_col.find({'updatedAt': {'$gte': date}}, {'user': 1, 'phone': 1})
        visits_lst: list = []
        for visit in visits:
            visits_lst.append({'id': str(visit['user']), 'phone': str(visit['phone'])})
        return visits_lst

    def get_phone_comparison_mongo(self, date: dt):
        comparison_col = self.db['phonecomparisons']
        comparisons = comparison_col.find({'updatedAt': {'$gte': date}})
        comparisons_lst: list = []
        for comparison in comparisons:
            comparisons_lst.append({'id': str(comparison['user']), 'phone1': str(comparison['phone1']), 'phone2': str(comparison['phone2'])})
        return comparisons_lst

    def get_all_products_trackers_mongo(self, date: dt):
        trackers = {
            'mobile': {
                'PROFILE': self.get_phone_profile_visit_mongo(date),
                'COMPARE': self.get_phone_comparison_mongo(date),
                # Add Question Tracker
            }
        }
        return trackers

