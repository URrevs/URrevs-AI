from recommender.collobarative.reviewTracker import Trackers
from recommender.collobarative.seenTable import SeenTable
from recommender.mongoDB.getData import MongoConnection
from recommender.mongoDB.sendData import send_date
from recommender.sqliteDB.data import SQLite_Database
from recommenderApi.imports import np, pd, dt, dump, load, Review_Tracker, Mobile_Tracker, Question_Tracker
from recommender.collobarative.recommend import MatrixFactorization
from recommender.collobarative.questions import questions_to_dic
from recommender.gamification.grading import Grading
from recommenderApi.settings import ROUND_NUM_OF_REVIEWS, REMOVE_FROM_SEEN_TABLE_AFTER_DAYS, EVERY_ITERATION_EPOCHS_AMOUNT_INCREASE
from recommenderApi.settings import MIN_ITEM, MAX_PREVIEW, MAX_CREVIEW, MAX_PQUESTION, MAX_CQUESTION
from recommender.models import *
from recommender.collobarative.anonymous import calc_anonymous_data 
from recommender.reviews.reviewsRecommender import ReviewContentRecommender
from recommender.recommend import recommend

def get_max_n_liked_companies(mobiles: list):
    companies = []
    sql = SQLite_Database()
    for mobile in mobiles:
        try: companies.append(sql.get_company_from_mobile(mobile))
        except: pass
    return companies

def train(first: bool = False):
    try:
        try: vars = load(open('recommenderApi/vars.pkl', 'rb'))
        except: vars = {}
        if first:
            print('------------------------------------ Start training ----------------------------------------')
            print('Training on items data')
            # Training on items data
            items_epochs = 600
            items_model = MatrixFactorization(n_epochs=items_epochs)
            train_rmse = items_model.train(path='recommender/collobarative/itemsTrackers.pkl',
                test_size=0.2, reg = 0.005, gamma=0.5)
            test_rmse = items_model.test()
            # if train_rmse != 0 or test_rmse != 0:
            print('train_rmse: ', train_rmse, '  -  test_rmse: ', test_rmse)
            vars['items_epochs'] = items_epochs
            items_model.save_model()
            
            # Training on mobiles data
            mobiles_epochs = 30
            mobiles_model = MatrixFactorization(n_epochs=mobiles_epochs, columns=['user_id', 'product_id', 'rating', 'rating_pred'])
            train_rmse = mobiles_model.train(path='recommender/collobarative/mobileTrackers.pkl', test_size=0.2)
            test_rmse = mobiles_model.test()
            # if train_rmse != 0 or test_rmse != 0:
            print('train_rmse: ', train_rmse, '  -  test_rmse: ', test_rmse)
            vars['mobiles_epochs'] = mobiles_epochs
            mobiles_model.save_model(model_path='recommender/collobarative/MF_mobiles_model.pkl')
                    
        else:
            print('------------------------------------ Start training items --------------------------------------')
            print('Training on items data')
            # Training on items data
            try: items_epochs = vars['items_epochs']
            except: items_epochs = 600
            while True:
                items_model = MatrixFactorization(n_epochs=items_epochs)
                train_rmse = items_model.online_train(path='recommender/collobarative/itemsTrackers.pkl',
                    model_path='recommender/collobarative/MF_items_model.pkl', test_size=0.2)
                test_rmse = items_model.test()
                print('train_rmse: ', train_rmse, '  -  test_rmse: ', test_rmse)
                # if train_rmse < 0.1 and test_rmse < 0.1:
                if train_rmse < 0.3:
                    vars['items_epochs'] = items_epochs
                    items_model.save_model(model_path='recommender/collobarative/MF_items_model.pkl')
                    break
                else:
                    items_epochs += EVERY_ITERATION_EPOCHS_AMOUNT_INCREASE
            print('----------------------------------- Start training mobiles -----------------------------------------')
            print('Training on mobiles data')
            # Training on mobiles data
            try: mobiles_epochs = vars['mobiles_epochs']
            except: mobiles_epochs = 30
            while True:
                mobiles_model = MatrixFactorization(n_epochs=mobiles_epochs, columns=['user_id', 'product_id', 'rating', 'rating_pred'])
                train_rmse = mobiles_model.online_train(path='recommender/collobarative/mobileTrackers.pkl',
                    model_path='recommender/collobarative/MF_mobiles_model.pkl', test_size=0.2)
                test_rmse = mobiles_model.test()
                print('train_rmse: ', train_rmse, '  -  test_rmse: ', test_rmse)
                # if train_rmse < 0.1 and test_rmse < 0.1:
                if train_rmse < 0.3:    
                    mobiles_model.save_model(model_path='recommender/collobarative/MF_mobiles_model.pkl')
                    vars['mobiles_epochs'] = mobiles_epochs
                    break
                else:
                    items_epochs += EVERY_ITERATION_EPOCHS_AMOUNT_INCREASE
            print('------------------------------------------------------')
        dump(vars, open('recommenderApi/vars.pkl', 'wb'))
    except Exception as e:
        print(e)
        pass

def update_ratios(diffs: list, old: list) -> list:
    '''
        function to calculate the ratios based on the interactions and the old state

        parameters: interaction list and the old state list
        output: the new list of ratios
    '''
    assert (sum(old) == 20)
    new = old.copy()
    diffs_min = diffs.copy()
    max = [MAX_PREVIEW, MAX_CREVIEW, MAX_PQUESTION, MAX_CQUESTION]
    counter = 4
    while counter > 1:
        while True:
            max_idx = np.argmax(diffs)
            diffs[max_idx] = -1
            counter -= 1
            if new[max_idx] < max[max_idx] or counter == 0:
                break
        while True:
            min_idx = np.argmin(diffs_min)
            diffs_min[min_idx] = np.inf
            counter -= 1
            if new[min_idx] > MIN_ITEM or counter == 0:
                break
        if max[max_idx] > old[max_idx] and old[min_idx] > MIN_ITEM and min_idx != max_idx:
            new[max_idx] = old[max_idx] + 1
            new[min_idx] = old[min_idx] - 1
    if sum(new) != ROUND_NUM_OF_REVIEWS: return old
    return new

def update_counts(sqlite: SQLite_Database, itemType, itemId: str, val: list):
    if itemType == '0': # product reviews
        sqlite.update_Prev_interaction(itemId, val)
    elif itemType == '1': # company reviews
        sqlite.update_Crev_interaction(itemId, val)
    elif itemType == '2': # product questions
        val[0] = MongoConnection().get_product_questions_num_votes_mongo(id=itemId)
        sqlite.update_Pques_interaction(itemId, val)
    elif itemType == '3': # company questions
        val[0] = MongoConnection().get_company_questions_num_votes_mongo(id=itemId)
        sqlite.update_Cques_interaction(itemId, val)

def get_all_mobiles_have_reviews():
    sqlite = SQLite_Database()
    return sqlite.get_all_mobiles_have_reviews()

def generate_questions():
    sql = SQLite_Database()
    try:
        pques = sql.get_Pquestion()
        dump(questions_to_dic(pques, 2), open('recommender/collobarative/pques.pkl', 'wb'))
        cques = sql.get_Cquestion()
        dump(questions_to_dic(cques, 3), open('recommender/collobarative/cques.pkl', 'wb'))
    except Exception as e:
        print('Generating Questions: ', e)

def update_values(date: dt, first: bool = False):
    try:
        print('----------------------------- Start Updating Values ------------------------------------')
        mongo = MongoConnection()
        product_questions = mongo.update_all_fixed_data_mongo(date=date, first=first)
        print('finish all fixed mongo data')
        generate_questions()
        print('updated all fixed data')
        review = ReviewContentRecommender()
        review.preprocessing()
        review.preprocessing(recommend_type='company', path='recommender/reviews/crevs.pkl')
        print('Reviews content model finish')
        items_trackers = mongo.get_all_items_trackers_mongo(date=date)
        # print(items_trackers)
        print('got all items trackers')
        items_trackers_file = Trackers(loadfile=True)
        # items_trackers_file.resetTrackersFile()
        for item in items_trackers.keys():
            # review or question
            for item_type in items_trackers[item]:
                # product or company
                for tracker_type in items_trackers[item][item_type].keys():
                    if item == 'reviews':
                        items_trackers_file.addReviewsTrackers(items_trackers[item][item_type][tracker_type],\
                                Review_Tracker[tracker_type], item_type=='company')
                    elif item == 'questions':
                        items_trackers_file.addQuestionsTrackers(items_trackers[item][item_type][tracker_type],\
                                Question_Tracker[tracker_type], int(item_type=='company')+2)
        print('added items trackers')
        items_trackers_file.down_old_items_grade()
        print('downgraded old items')
        items_trackers_file.fill_most_liked_items()
        print('filled most liked items for all users')
        items_trackers_file.saveTrackers()
        print('items trackers saved')
        mobile_trackers_file = Trackers('recommender/collobarative/mobileTrackers.pkl', loadfile=True)
        # mobile_trackers_file.resetTrackersFile(col='product_id')
        mobile_trackers = mongo.get_all_products_trackers_mongo(date=date)
        print('got all mobiles trackers')
        time = dt.now()
        for item_type in mobile_trackers.keys():
            for tracker_type in mobile_trackers[item_type].keys():
                mobile_trackers_file.addMobilesTrackers(mobile_trackers[item_type][tracker_type], Mobile_Tracker[tracker_type])
        print('added mobile trackers')
        mobile_trackers_file.down_old_items_grade()
        print('downgraded old mobile')
        mobile_trackers_file.saveTrackers()
        print('mobile trackers saved')
        SeenTable(loadfile=True).removeExpiredDateFromSeenTable(REMOVE_FROM_SEEN_TABLE_AFTER_DAYS * 86400)
        print('removed expired date from seen table')
        sqlite = SQLite_Database()
        for user in items_trackers_file.usersDic.keys():
            u = sqlite.get_user(id = user)
            if u != None:
                [PR, CR, PQ, CQ] = update_ratios(items_trackers_file.usersDic[user], [u.PR, u.CR, u.PQ, u.CQ])
                sqlite.update_user_ratios(userId=user, PR=PR, CR=CR, PQ=PQ, CQ=CQ)
        print('updated user ratios')
        for item in items_trackers_file.interactions.keys():
            update_counts(sqlite=sqlite, itemType=item[0], itemId=item[1:], val=items_trackers_file.interactions[item])
        print('updated counts')
        get_all_mobiles_have_reviews()
        calc_anonymous_data()
        print('calculated anonymous data')
        if not first:
            try:
                recommendations = {}
                MF_Model = MatrixFactorization()
                users1 = items_trackers_file.getAllUsers()
                for user in users1:
                    recommendations[user] = MF_Model.recommend_items(user)
                dump(recommendations, open('recommender/collobarative/MF_items.pkl', 'wb'))
                print('generating MF Items recommendation done successfully')
            except Exception as e:
                print('generating MF items: ', e)
            try:
                mobiles = {}
                sql = SQLite_Database()
                MF_Model = MatrixFactorization()
                users2 = mobile_trackers_file.getAllUsers()
                for user in users2:
                    phones = MF_Model.recommend_mobiles(user, n_recommendations=5)
                    companies = get_max_n_liked_companies(phones)
                    prevs = []; crevs = []; pques = []; cques = []
                    prevs.extend(sql.get_Previews_by_mobile(phones))
                    pques.extend(sql.get_Pquestions_by_mobiles(phones))
                    cques.extend(sql.get_Cquestions_by_company(companies))
                    crevs.extend(sql.get_Creviews_by_companies(companies))
                    mobiles[user] = {
                        'phones': phones,
                        'companies': companies,
                        'lists': (prevs, crevs, pques, cques)
                    }
                dump(mobiles, open('recommender/collobarative/MF_mobiles.pkl', 'wb'))
                print('generating MF Mobiles recommendation done successfully')
            except Exception as e:
                print('generating MF mobiles: ', e)
        users = {}
        dump(users, open('recommender/users.pkl', 'wb'))
        dump(users, open('recommender/collobarative/gen_MF_ques.pkl', 'wb'))
        dump(users, open('recommender/collobarative/gen_MF_mobile_revs.pkl', 'wb'))
        dump(users, open('recommender/collobarative/gen_MF_revs.pkl', 'wb'))
        dump(users, open('recommender/collobarative/gen_CR_revs.pkl', 'wb'))
        print('old recommendation daily history erased')
        # print('generate first recommendation for every user')
        # if not first:
        #     try:
        #         users = {}
        #         dump(users, open('recommender/collobarative/gen_round_1.pkl', 'wb'))
        #         sql = SQLite_Database()
        #         users3 = items_trackers_file.getAllUsers()
        #         for userId in users3:
        #             user = sql.get_user(id=userId)
        #             # print(userId, user.name)
        #             users[userId] = recommend(userId=userId, round=1, PR=user.PR, CR=user.CR, PQ=user.PQ, CQ=user.CQ)
        #         dump(users, open('recommender/collobarative/gen_round_1.pkl', 'wb'))
        #     except Exception as e: print(e)
        # print('finished generating the first recommendations for all users')
        send_date(time)
        print('sent date')
    except Exception as e:
        print("Updating Values", e)
        pass
    
def train_and_update(date: dt, first: bool = False):
    if first:
        dump({}, open('recommenderApi/vars.pkl', 'wb'))
        Trackers().resetTrackersFile()
        Trackers('recommender/collobarative/mobileTrackers.pkl').resetTrackersFile(col='product_id')
        SeenTable().resetSeenTable()
    update_values(date, first)
    try:
        grading = Grading()
        grading.update_tf_idf()
        print('finish updating tf-idf vectorizers for gimification')
    except Exception as e:
        print('grading: ', e)
        print('failed in grading')
    train(first=first)

def check_engagement():
    df: pd.DataFrame = load(open('recommender/collobarative/itemsTrackers.pkl', 'rb'))['item_id']
    print(df.value_counts().index.values)
    return len(df.value_counts().values) >= 10, df.value_counts().index.values

# def calc_anonymous_data():
#     sql = SQLite_Database()
#     items = []
#     cques = sql.get_answered_Cquestions(answer=True, limit=50)
#     pques = sql.get_answered_Pquestions(answer=True, limit=100-len(cques))
#     rest = 100 - len(pques) - len(cques)
#     if rest % 2 == 0: prevs = sql.get_Prevs(limit=50+rest//2)
#     else: prevs = sql.get_Prevs(limit=51+rest//2)
#     crevs = sql.get_Crevs(limit=50+rest//2)
#     items.extend(cques); items.extend(pques); items.extend(crevs); items.extend(prevs)
#     items.sort(key=lambda x: (-x[1], -x[2], -x[3], -x[4]))
#     counter = 0; iter = 0
#     pques = []; cques = []; prevs = []; crevs = []; total = []; final = []
#     for item in items:
#         total.append(item[0][1:])
#         if item[0][0] == '0': prevs.append(item[0][1:])
#         if item[0][0] == '1': crevs.append(item[0][1:])
#         if item[0][0] == '2': pques.append(item[0][1:])
#         if item[0][0] == '3': cques.append(item[0][1:])
#         counter += 1
#         if counter == ROUND_NUM_OF_REVIEWS: 
#             counter = 0
#             final.append([prevs, crevs, pques, cques, total])
#             pques = []; cques = []; prevs = []; crevs = []; total = []
#             iter += 1
#     dump(final, open('recommender/collobarative/anonymous_data.pkl', 'wb'))
#     return final
