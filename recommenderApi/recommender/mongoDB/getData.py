from recommender.models import Mobile
from recommenderApi.imports import MongoClient, certifi, dt, ObjectId
from recommenderApi.settings import MONGODB_LINK, MONGODB_NAME, ROUND_NUM_OF_REVIEWS
from recommender.sqliteDB.data import SQLite_Database
from recommender.mobiles1.getPhones import Similar_Phones

class MongoConnection:
    def __init__(self, mongodb_link: str = MONGODB_LINK, mongodb_name: str = MONGODB_NAME):
        self.db = self.connect_to_mongo(mongodb_link, mongodb_name)
        # print('connected to mongo')
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
        self.db = self.connect_to_mongo()
        users_col = self.db['users']
        users = users_col.find({'createdAt': {'$gte': date}}, {'_id': 1, 'name': 1})
        return users

    def get_product_reviews_mongo(self, date: dt):
        self.db = self.connect_to_mongo()
        prevs_col = self.db['prevs']
        projection = {
            '_id': 1, 'user': 1, 'phone': 1, 'pros': 1, 'cons': 1, 'createdAt': 1, 'generalRating': 1,
            'uiRating': 1, 'manQuality': 1, 'valFMon': 1, 'camera': 1, 'callQuality': 1, 'batteryRating': 1
        }
        prevs = prevs_col.find({'createdAt': {'$gte': date}}, projection)
        return prevs

    def get_company_reviews_mongo(self, date: dt):
        self.db = self.connect_to_mongo()
        crevs_col = self.db['crevs']
        projection = {
            '_id': 1, 'user': 1, 'company': 1, 'pros': 1, 'cons': 1, 'createdAt': 1, 'generalRating': 1
        }
        crevs = crevs_col.find({'createdAt': {'$gte': date}}, projection)
        return crevs

    def get_companies_mongo(self):
        self.db = self.connect_to_mongo()
        companies_col = self.db['companies']
        companies = companies_col.find({}, {'_id': 1, 'nameLower': 1})
        return companies

    def get_phones_mongo(self, date: dt):
        self.db = self.connect_to_mongo()
        phones_col = self.db['nphones']
        projection = {
            '_id': 1, 'name': 1, 'company': 1, 'price': 1, 'releaseDate': 1, 'length': 1, 'width': 1,
            'height': 1, 'network': 1, 'weight': 1, 'sim': 1, 'screenType': 1, 'screenSize': 1,
            'screen2bodyRatio': 1, 'resolutionLength': 1, 'resolutionWidth': 1, 'resolutionDensity': 1,
            'screenProtection': 1, 'os': 1, 'chipset': 1, 'cpu': 1, 'gpu': 1, 'intMem': 1, 'mainCam': 1,
            'selfieCam': 1, 'hasLoudspeaker': 1, 'hasStereo': 1, 'has3p5mm': 1, 'wlan': 1, 'hasNfc': 1,  
            'bluetoothVersion': 1, 'radio': 1, 'usbType': 1, 'usbVersion': 1, 'hasGyro': 1, 'hasProximity': 1,
            'fingerprintDetails': 1, 'batteryCapacity': 1, 'hasFastCharging': 1, 'chargingPower': 1,
            'createdAt': 1, 'updatedAt': 1
        }
        phones = phones_col.find({'createdAt': {'$gte': date}}, projection)
        return phones

    def get_product_reviews_likes_mongo(self, date: dt):
        self.db = self.connect_to_mongo()
        prevs_likes_col = self.db['prevslikes']
        likes = prevs_likes_col.find({'updatedAt': {'$gte': date}, 'unliked': False}, {'_id': 0, 'user': 1, 'review': 1})
        # add identifier to the like
        likes_lst: list = []
        for like in likes:
            likes_lst.append({'id': str(like['user']), 'review': f"0{like['review']}"})
        return likes_lst
    
    def get_company_reviews_likes_mongo(self, date: dt):
        self.db = self.connect_to_mongo()
        crevs_likes_col = self.db['crevslikes']
        likes = crevs_likes_col.find({'updatedAt': {'$gte': date}, 'unliked': False}, {'_id': 0, 'user': 1, 'review': 1})
        # add identifier to the like
        likes_lst: list = []
        for like in likes:
            likes_lst.append({'id': str(like['user']), 'review': f"1{like['review']}"})
        return likes_lst

    def get_product_reviews_unlikes_mongo(self, date: dt):
        self.db = self.connect_to_mongo()
        prevs_unlikes_col = self.db['prevsunlikes']
        unlikes = prevs_unlikes_col.find({'createdAt': {'$gte': date}}, {'_id': 0, 'user': 1, 'review': 1})
        # add identifier to the unlike
        unlikes_lst: list = []
        for unlike in unlikes:
            unlikes_lst.append({'id': str(unlike['user']), 'review': f"0{unlike['review']}"})
        return unlikes_lst

    def get_company_reviews_unlikes_mongo(self, date: dt):
        self.db = self.connect_to_mongo()
        crevs_unlikes_col = self.db['crevsunlikes']
        unlikes = crevs_unlikes_col.find({'createdAt': {'$gte': date}}, {'_id': 0, 'user': 1, 'review': 1})
        # add identifier to the unlike
        unlikes_lst: list = []
        for unlike in unlikes:
            unlikes_lst.append({'id': str(unlike['user']), 'review': f"1{unlike['review']}"})
        return unlikes_lst
    
    def get_product_reviews_comments_mongo(self, date: dt):
        self.db = self.connect_to_mongo()
        prevs_comments_col = self.db['prevscomments']
        comments = prevs_comments_col.find({'createdAt': {'$gte': date}}, {'_id': 0, 'user': 1, 'review': 1})
        # add identifier to the comment
        comments_lst: list = []
        for comment in comments:
            comments_lst.append({'id': str(comment['user']), 'review': f"0{comment['review']}"})
        return comments_lst
    
    def get_company_reviews_comments_mongo(self, date: dt):
        self.db = self.connect_to_mongo()
        crevs_comments_col = self.db['crevscomments']
        comments = crevs_comments_col.find({'createdAt': {'$gte': date}}, {'_id': 0, 'user': 1, 'review': 1})
        # add identifier to the comment
        comments_lst: list = []
        for comment in comments:
            comments_lst.append({'id': str(comment['user']), 'review': f"1{comment['review']}"})
        return comments_lst
    
    def get_product_reviews_seemores_mongo(self, date: dt):
        self.db = self.connect_to_mongo()
        prevs_seemores_col = self.db['prevsseemores']
        seemores = prevs_seemores_col.find({'updatedAt': {'$gte': date}}, {'_id': 0, 'user': 1, 'review': 1})
        # add identifier to the seemore
        seemores_lst: list = []
        for seemore in seemores:
            seemores_lst.append({'id': str(seemore['user']), 'review': f"0{seemore['review']}"})
        return seemores_lst
    
    def get_company_reviews_seemores_mongo(self, date: dt):
        self.db = self.connect_to_mongo()
        crevs_seemores_col = self.db['crevsseemores']
        seemores = crevs_seemores_col.find({'updatedAt': {'$gte': date}}, {'_id': 0, 'user': 1, 'review': 1})
        # add identifier to the seemore
        seemores_lst: list = []
        for seemore in seemores:
            seemores_lst.append({'id': str(seemore['user']), 'review': f"1{seemore['review']}"})
        return seemores_lst
    
    def get_product_reviews_fullscreens_mongo(self, date: dt):
        self.db = self.connect_to_mongo()
        prevs_fullscreens_col = self.db['prevsfullscreens']
        fullscreens = prevs_fullscreens_col.find({'updatedAt': {'$gte': date}}, {'_id': 0, 'user': 1, 'review': 1})
        # add identifier to the fullscreen
        fullscreens_lst: list = []
        for fullscreen in fullscreens:
            fullscreens_lst.append({'id': str(fullscreen['user']), 'review': f"0{fullscreen['review']}"})
        return fullscreens_lst
    
    def get_company_reviews_fullscreens_mongo(self, date: dt):
        self.db = self.connect_to_mongo()
        crevs_fullscreens_col = self.db['crevsfullscreens']
        fullscreens = crevs_fullscreens_col.find({'updatedAt': {'$gte': date}}, {'_id': 0, 'user': 1, 'review': 1})
        # add identifier to the fullscreen
        fullscreens_lst: list = []
        for fullscreen in fullscreens:
            fullscreens_lst.append({'id': str(fullscreen['user']), 'review': f"1{fullscreen['review']}"})
        return fullscreens_lst
    
    def get_product_reviews_hates_mongo(self, date: dt):
        self.db = self.connect_to_mongo()
        prevs_hates_col = self.db['prevshates']
        hates = prevs_hates_col.find({'updatedAt': {'$gte': date}}, {'_id': 0, 'user': 1, 'review': 1})
        # add identifier to the hate
        hates_lst: list = []
        for hate in hates:
            hates_lst.append({'id': str(hate['user']), 'review': f"0{hate['review']}"})
        return hates_lst
    
    def get_company_reviews_hates_mongo(self, date: dt):
        self.db = self.connect_to_mongo()
        crevs_hates_col = self.db['crevshates']
        hates = crevs_hates_col.find({'updatedAt': {'$gte': date}}, {'_id': 0, 'user': 1, 'review': 1})
        # add identifier to the hate
        hates_lst: list = []
        for hate in hates:
            hates_lst.append({'id': str(hate['user']), 'review': f"1{hate['review']}"})
        return hates_lst
    
    # ------------------------------------------------------------------------------------------------------

    def get_product_questions_mongo(self, date: dt):
        self.db = self.connect_to_mongo()
        pques_col = self.db['pques']
        projection = {
            '_id': 1, 'user': 1, 'phone': 1, 'content': 1, 'createdAt': 1, 'acceptedAns': 1
        }
        pques = pques_col.find({'createdAt': {'$gte': date}}, projection)
        return pques

    def get_product_questions_num_votes_mongo(self, id: str):
        self.db = self.connect_to_mongo()
        pques_col = self.db['pques']
        pques = pques_col.find_one({'_id': ObjectId(id)}, {'_id': 0, 'upvotes': 1})
        if pques == None: return 0
        return pques['upvotes']


    def get_company_questions_mongo(self, date: dt):
        self.db = self.connect_to_mongo()
        cques_col = self.db['cques']
        projection = {
            '_id': 1, 'user': 1, 'company': 1, 'content': 1, 'createdAt': 1, 'acceptedAns': 1
        }
        cques = cques_col.find({'createdAt': {'$gte': date}}, projection)
        return cques

    def get_company_questions_num_votes_mongo(self, id: str):
        self.db = self.connect_to_mongo()
        cques_col = self.db['cques']
        cques = cques_col.find_one({'_id': ObjectId(id)}, {'_id': 0, 'upvotes': 1})
        if cques == None: return 0
        return cques['upvotes']

    def get_product_questions_upvotes_mongo(self, date: dt):
        self.db = self.connect_to_mongo()
        pques_upvotes_col = self.db['pqueslikes']
        upvotes = pques_upvotes_col.find({'updatedAt': {'$gte': date}, 'unliked': False}, {'_id': 0, 'user': 1, 'question': 1})
        # add identifier to the like
        upvotes_lst: list = []
        for upvote in upvotes:
            upvotes_lst.append({'id': str(upvote['user']), 'question': f"2{upvote['question']}"})
        return upvotes_lst
    
    def get_company_questions_upvotes_mongo(self, date: dt):
        self.db = self.connect_to_mongo()
        cques_upvotes_col = self.db['cqueslikes']
        upvotes = cques_upvotes_col.find({'updatedAt': {'$gte': date}, 'unliked': False}, {'_id': 0, 'user': 1, 'question': 1})
        # add identifier to the like
        upvotes_lst: list = []
        for upvote in upvotes:
            upvotes_lst.append({'id': str(upvote['user']), 'question': f"3{upvote['question']}"})
        return upvotes_lst
    
    def get_product_questions_downvotes_mongo(self, date: dt):
        self.db = self.connect_to_mongo()
        pques_downvotes_col = self.db['pquesunlikes']
        downvotes = pques_downvotes_col.find({'createdAt': {'$gte': date}}, {'_id': 0, 'user': 1, 'question': 1})
        # add identifier to the unlike
        downvotes_lst: list = []
        for downvote in downvotes:
            downvotes_lst.append({'id': str(downvote['user']), 'question': f"2{downvote['question']}"})
        return downvotes_lst

    def get_company_questions_downvotes_mongo(self, date: dt):
        self.db = self.connect_to_mongo()
        cques_downvotes_col = self.db['cquesunlikes']
        downvotes = cques_downvotes_col.find({'createdAt': {'$gte': date}}, {'_id': 0, 'user': 1, 'question': 1})
        # add identifier to the unlike
        downvotes_lst: list = []
        for downvote in downvotes:
            downvotes_lst.append({'id': str(downvote['user']), 'question': f"3{downvote['question']}"})
        return downvotes_lst

    def get_product_questions_answers_mongo(self, date: dt):
        self.db = self.connect_to_mongo()
        pques_answers_col = self.db['pquesanswers']
        answers = pques_answers_col.find({'createdAt': {'$gte': date}}, {'_id': 0, 'user': 1, 'question': 1})
        # add identifier to the comment
        answers_lst: list = []
        for answer in answers:
            answers_lst.append({'id': str(answer['user']), 'question': f"2{answer['question']}"})
        return answers_lst

    def get_company_questions_answers_mongo(self, date: dt):
        self.db = self.connect_to_mongo()
        cques_answers_col = self.db['cquesanswers']
        answers = cques_answers_col.find({'createdAt': {'$gte': date}}, {'_id': 0, 'user': 1, 'question': 1})
        # add identifier to the comment
        answers_lst: list = []
        for answer in answers:
            answers_lst.append({'id': str(answer['user']), 'question': f"3{answer['question']}"})
        return answers_lst

    def get_product_questions_fullscreens_mongo(self, date: dt):
        self.db = self.connect_to_mongo()
        pques_fullscreens_col = self.db['pquesfullscreens']
        fullscreens = pques_fullscreens_col.find({'updatedAt': {'$gte': date}}, {'_id': 0, 'user': 1, 'question': 1})
        # add identifier to the fullscreen
        fullscreens_lst: list = []
        for fullscreen in fullscreens:
            fullscreens_lst.append({'id': str(fullscreen['user']), 'question': f"2{fullscreen['question']}"})
        return fullscreens_lst

    def get_company_questions_fullscreens_mongo(self, date: dt):
        self.db = self.connect_to_mongo()
        cques_fullscreens_col = self.db['cquesfullscreens']
        fullscreens = cques_fullscreens_col.find({'updatedAt': {'$gte': date}}, {'_id': 0, 'user': 1, 'question': 1})
        # add identifier to the fullscreen
        fullscreens_lst: list = []
        for fullscreen in fullscreens:
            fullscreens_lst.append({'id': str(fullscreen['user']), 'question': f"3{fullscreen['question']}"})
        return fullscreens_lst

    def get_product_questions_added_acceptedanswer_mongo(self, date: dt):
        self.db = self.connect_to_mongo()
        pques_accepteds_col = self.db['pquesaccepteds']
        accepteds = pques_accepteds_col.find({'createdAt': {'$gte': date}}, {'_id': 0, 'question': 1})
        return accepteds

    def get_company_questions_added_acceptedanswer_mongo(self, date: dt):
        self.db = self.connect_to_mongo()
        cques_accepteds_col = self.db['cquesaccepteds']
        accepteds = cques_accepteds_col.find({'createdAt': {'$gte': date}}, {'_id': 0, 'question': 1})
        return accepteds

    def get_product_questions_removed_acceptedanswer_mongo(self, date: dt):
        self.db = self.connect_to_mongo()
        pques_accepteds_col = self.db['pquesacceptedremoveds']
        accepteds = pques_accepteds_col.find({'createdAt': {'$gte': date}}, {'_id': 0, 'question': 1})
        return accepteds

    def get_company_questions_removed_acceptedanswer_mongo(self, date: dt):
        self.db = self.connect_to_mongo()
        cques_accepteds_col = self.db['cquesacceptedremoveds']
        accepteds = cques_accepteds_col.find({'createdAt': {'$gte': date}}, {'_id': 0, 'question': 1})
        return accepteds

    def get_product_questions_aboutmyphones_visits_mongo(self, date: dt):
        self.db = self.connect_to_mongo()
        sql = SQLite_Database()
        ques_visits_col = self.db['questionsaboutmyphonesvisits']
        visits = ques_visits_col.find({'updatedAt': {'$gte': date}}, {'_id': 1})
        visits_lst: list = []
        for visit in visits:
            visits_lst.extend(sql.get_owned_mobiles_questions_mongo(str(visit['_id'])))
        return visits_lst

    def get_product_questions_hates_mongo(self, date: dt):
        self.db = self.connect_to_mongo()
        pques_hates_col = self.db['pqueshates']
        hates = pques_hates_col.find({'updatedAt': {'$gte': date}}, {'_id': 0, 'user': 1, 'question': 1})
        # add identifier to the hate
        hates_lst: list = []
        for hate in hates:
            hates_lst.append({'id': str(hate['user']), 'question': f"2{hate['question']}"})
        return hates_lst

    def get_company_questions_hates_mongo(self, date: dt):
        self.db = self.connect_to_mongo()
        cques_hates_col = self.db['cqueshates']
        hates = cques_hates_col.find({'updatedAt': {'$gte': date}}, {'_id': 0, 'user': 1, 'question': 1})
        # add identifier to the hate
        hates_lst: list = []
        for hate in hates:
            hates_lst.append({'id': str(hate['user']), 'question': f"3{hate['question']}"})
        return hates_lst

    def get_last_training_time(self):
        col = self.db['constants']
        time = col.find_one({'name': 'AILastQuery'}, {'_id': 0, 'date': 1})
        return time['date']

    def update_all_fixed_data_mongo(self, date:dt, first:bool):
        sqlite = SQLite_Database()
        users = self.get_users_mongo(date)
        print('get all users mongo')
        for user in users:
            sqlite.create_new_user_ifNotExist(user)
        print('add them to sqlite db')
        print('get all companies mongo')
        companies = self.get_companies_mongo()
        for company in companies:
            sqlite.create_new_company_ifNotExist(company)
        print('add them to sqlite db')
        print('get all phones mongo')
        mobiles = self.get_phones_mongo(date)
        lst_phones = []
        for mobile in mobiles:
            sqlite.create_new_mobile_ifNotExist(mobile)
            lst_phones.append(mobile)
        print('add them to sqlite db')
        try:
            similar = Similar_Phones(mongo=self)
            df = similar.make_comparison_table(lst_phones)
            print('df is generated successfully')
            if df.shape[0] != 0: similar.min_max_scale(df, repeat = not first)
            print('finish adding similar phones')
        except Exception as e:
            print('similar phones: ', e)
            print('failed to add similar phones')
        print('get all pques mongo')
        product_questions = self.get_product_questions_mongo(date)
        for question in product_questions:
            sqlite.create_new_Pquestion_ifNotExist(question)
        print('add them to sqlite db')
        print('get all pques accepted answer')
        questions = self.get_product_questions_added_acceptedanswer_mongo(date)
        for question in questions:
            sqlite.set_Pques_accepted_answer(question['question'])
        questions = self.get_product_questions_removed_acceptedanswer_mongo(date)
        for question in questions:
            sqlite.set_Pques_accepted_answer(question['question'], accepted_answer=False)
        print('finish updating all pques accepted answer')
        print('get all cques mongo')
        questions = self.get_company_questions_mongo(date)
        for question in questions:
            sqlite.create_new_Cquestion_ifNotExist(question)
        print('add them to sqlite db')
        print('get all cques accepted answer')
        questions = self.get_company_questions_added_acceptedanswer_mongo(date)
        for question in questions:
            sqlite.set_Cques_accepted_answer(question['question'])
        questions = self.get_company_questions_removed_acceptedanswer_mongo(date)
        for question in questions:
            sqlite.set_Cques_accepted_answer(question['question'], accepted_answer=False)
        print('get all prevs mongo')
        reviews = self.get_product_reviews_mongo(date)
        for review in reviews:
            sqlite.create_new_Preview_ifNotExist(review)
        print('add them to sqlite db')
        print('get all crevs mongo')
        reviews = self.get_company_reviews_mongo(date)
        for review in reviews:
            sqlite.create_new_Creview_ifNotExist(review)
        print('add them to sqlite db')
        print('finish updating all pques accepted answer')
        print('finish adding all users, companies, mobiles, reviews and questions')
        return product_questions

    def get_all_items_trackers_mongo(self, date: dt):
        trackers = {
            'reviews': {
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
            },
            'questions': {
                'product': {
                    'UPVOTE': self.get_product_questions_upvotes_mongo(date),
                    'DOWNVOTE': self.get_product_questions_downvotes_mongo(date),
                    'ANSWER': self.get_product_questions_answers_mongo(date),
                    'FULL_SCREEN': self.get_product_questions_fullscreens_mongo(date),
                    'ABOUT_MY_PRODUCTS_PAGE': self.get_product_questions_aboutmyphones_visits_mongo(date),
                    'DONT_LIKE': self.get_product_questions_hates_mongo(date)
                },
                'company': {
                    'UPVOTE': self.get_company_questions_upvotes_mongo(date),
                    'DOWNVOTE': self.get_company_questions_downvotes_mongo(date),
                    'ANSWER': self.get_company_questions_answers_mongo(date),
                    'FULL_SCREEN': self.get_company_questions_fullscreens_mongo(date),
                    'DONT_LIKE': self.get_company_questions_hates_mongo(date)
                }
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
            comparisons_lst.append({'id': str(comparison['user']), 'phone': str(comparison['srcPhone'])})
            comparisons_lst.append({'id': str(comparison['user']), 'phone': str(comparison['dstPhone'])})
        return comparisons_lst

    def get_all_products_trackers_mongo(self, date: dt, questions: list = []):
        trackers = {
            'mobile': {
                'PROFILE': self.get_phone_profile_visit_mongo(date),
                'COMPARE': self.get_phone_comparison_mongo(date),
                'QUESTION': questions
            }
        }
        return trackers

