from recommenderApi.imports import MongoClient, certifi, dt
from recommenderApi.settings import MONGODB_LINK, MONGODB_NAME

class MongoConnection:
    def __init__(self, mongodb_link: str = MONGODB_LINK, mongodb_name: str = MONGODB_NAME):
        self.db = self.connect_to_mongo(mongodb_link, mongodb_name)
        return None
    
    def connect_to_mongo(self, mongodb_link: str = MONGODB_LINK, mongodb_name: str = MONGODB_NAME):
        client = MongoClient(mongodb_link, tlsCAFile=certifi.where())
        self.db = client[mongodb_name]
        return self.db

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
        likes = prevs_likes_col.find({'createdAt': {'$gte': date}, 'unliked': False}, {'user': 1, 'review': 1})
        return likes

    def get_company_reviews_likes_mongo(self, date: dt):
        crevs_likes_col = self.db['crevslikes']
        likes = crevs_likes_col.find({'createdAt': {'$gte': date}, 'unliked': False}, {'user': 1, 'review': 1})
        return likes

    def get_product_reviews_unlikes_mongo(self, date: dt):
        prevs_unlikes_col = self.db['prevsunlikes']
        unlikes = prevs_unlikes_col.find({'createdAt': {'$gte': date}}, {'user': 1, 'review': 1})
        return unlikes

    def get_company_reviews_unlikes_mongo(self, date: dt):
        crevs_unlikes_col = self.db['crevsunlikes']
        unlikes = crevs_unlikes_col.find({'createdAt': {'$gte': date}}, {'user': 1, 'review': 1})
        return unlikes

    def get_product_reviews_comments_mongo(self, date: dt):
        prevs_comments_col = self.db['prevscomments']
        comments = prevs_comments_col.find({'createdAt': {'$gte': date}}, {'user': 1, 'review': 1})
        return comments

    def get_company_reviews_comments_mongo(self, date: dt):
        crevs_comments_col = self.db['crevscomments']
        comments = crevs_comments_col.find({'createdAt': {'$gte': date}}, {'user': 1, 'review': 1})
        return comments

    def get_product_reviews_seemores_mongo(self, date: dt):
        prevs_seemores_col = self.db['prevsseemores']
        seemores = prevs_seemores_col.find({'updatedAt': {'$gte': date}}, {'user': 1, 'review': 1})
        return seemores

    def get_company_reviews_seemores_mongo(self, date: dt):
        crevs_seemores_col = self.db['crevsseemores']
        seemores = crevs_seemores_col.find({'updatedAt': {'$gte': date}}, {'user': 1, 'review': 1})
        return seemores

    def get_product_reviews_fullscreens_mongo(self, date: dt):
        prevs_fullscreens_col = self.db['prevsfullscreens']
        fullscreens = prevs_fullscreens_col.find({'updatedAt': {'$gte': date}}, {'user': 1, 'review': 1})
        return fullscreens

    def get_company_reviews_fullscreens_mongo(self, date: dt):
        crevs_fullscreens_col = self.db['crevsfullscreens']
        fullscreens = crevs_fullscreens_col.find({'updatedAt': {'$gte': date}}, {'user': 1, 'review': 1})
        return fullscreens

    def get_product_reviews_hates_mongo(self, date: dt):
        prevs_hates_col = self.db['prevshates']
        hates = prevs_hates_col.find({'updatedAt': {'$gte': date}}, {'user': 1, 'review': 1})
        return hates

    def get_company_reviews_hates_mongo(self, date: dt):
        crevs_hates_col = self.db['crevshates']
        hates = crevs_hates_col.find({'updatedAt': {'$gte': date}}, {'user': 1, 'review': 1})
        return hates

    def get_phone_profile_visit_mongo(self, date: dt):
        profile_visits_col = self.db['phoneprofilevisits']
        visits = profile_visits_col.find({'updatedAt': {'$gte': date}}, {'user': 1, 'phone': 1})
        return visits

    def get_phone_comparison_mongo(self, date: dt):
        comparison_col = self.db['phonecomparisons']
        comparisons = comparison_col.find({'updatedAt': {'$gte': date}})
        return comparisons



