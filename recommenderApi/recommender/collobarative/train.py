from recommender.collobarative.reviewTracker import Trackers
from recommender.collobarative.seenTable import SeenTable
from recommender.mongoDB.getData import MongoConnection
from recommender.mongoDB.sendData import send_date
from recommender.sqliteDB.data import SQLite_Database
from recommenderApi.imports import np, pd, dt, dump, load, Review_Tracker, Mobile_Tracker
from recommender.collobarative.recommend import MatrixFactorization
from recommenderApi.settings import ROUND_NUM_OF_REVIEWS, REMOVE_FROM_SEEN_TABLE_AFTER_DAYS, EVERY_ITERATION_EPOCHS_AMOUNT_INCREASE
from recommenderApi.settings import MIN_ITEM, MAX_PREVIEW, MAX_CREVIEW, MAX_PQUESTION, MAX_CQUESTION
from recommender.models import *
from recommender.reviews.reviewsRecommender import ReviewContentRecommender

def train(first: bool = False):
    try:
        vars = load(open('recommenderApi/vars.pkl', 'rb'))
        if first:
            print('------------------------------------ Start training ----------------------------------------')
            print('Training on items data')
            # Training on items data
            items_epochs = 600
            items_model = MatrixFactorization(n_epochs=items_epochs)
            train_rmse = items_model.train(path='recommender/collobarative/itemsTrackers.pkl',
                test_size=0.2, reg = 0.005, gamma=0.5)
            test_rmse = items_model.test()
            if train_rmse != 0 or test_rmse != 0:
                print('train_rmse: ', train_rmse, '  -  test_rmse: ', test_rmse)
                vars['items_epochs'] = items_epochs
                items_model.save_model()
            
            # Training on mobiles data
            mobiles_epochs = 30
            mobiles_model = MatrixFactorization(n_epochs=mobiles_epochs, columns=['user_id', 'product_id', 'rating', 'rating_pred'])
            train_rmse = mobiles_model.train(path='recommender/collobarative/mobileTrackers.pkl', test_size=0.2)
            test_rmse = mobiles_model.test()
            if train_rmse != 0 or test_rmse != 0:
                print('train_rmse: ', train_rmse, '  -  test_rmse: ', test_rmse)
                vars['mobiles_epochs'] = mobiles_epochs
                mobiles_model.save_model(model_path='recommender/collobarative/MF_mobiles_model.pkl')
                    
        else:
            print('------------------------------------ Start training items --------------------------------------')
            print('Training on items data')
            # Training on items data
            items_epochs = vars['items_epochs']
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
            mobiles_epochs = vars['mobiles_epochs']
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
    if itemType == '1': # company
        sqlite.update_Crev_interaction(itemId, val)
    else: # product
        sqlite.update_Prev_interaction(itemId, val)

def get_all_mobiles_have_reviews():
    sqlite = SQLite_Database()
    return sqlite.get_all_mobiles_have_reviews()

def update_values(date: dt):
    try:
        print('----------------------------- Start Updating Values ------------------------------------')
        mongo = MongoConnection()
        mongo.update_all_fixed_data_mongo(date=date)
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
        for item_type in items_trackers.keys():
            for tracker_type in items_trackers[item_type].keys():
                items_trackers_file.addItemsTrackers(items_trackers[item_type][tracker_type], Review_Tracker[tracker_type], item_type=='company')
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
        users = {}
        dump(users, open('recommender/users.pkl', 'wb'))
        print('recommendation daily history erased')
        send_date(time)
        print('sent date')
    except Exception as e:
        print("Updating Values", e)
        pass
    
def train_and_update(date: dt, first: bool = False):
    # if first:
    #     date = dt(2022, 5, 1)
    if first:
        Trackers().resetTrackersFile()
        Trackers('recommender/collobarative/mobileTrackers.pkl').resetTrackersFile(col='product_id')
        SeenTable().resetSeenTable()
    update_values(date)
    train(first=first)

def check_engagement():
    df: pd.DataFrame = load(open('recommender/collobarative/itemsTrackers.pkl', 'rb'))['item_id']
    return len(df.value_counts().values) >= 10, df.value_counts().index.values

def calc_anonymous_data():
    check, df = check_engagement()
    reviews = []
    count = 0
    if check:
        count = (min([len(df), 200]) // ROUND_NUM_OF_REVIEWS) * ROUND_NUM_OF_REVIEWS
        sqlite = SQLite_Database()
        for id in df:
            if id[0] == '0':
                prev = sqlite.get_Preview(id = id[1:])
                # After adding all prevs to db remove this condition
                if prev != None:
                    reviews.append([id, prev.likesCounter, prev.commentsCounter])
            else:
                crev = sqlite.get_Creview(id=id[1:])
                # After adding all crevs to db remove this condition
                if crev != None:
                    reviews.append([id, crev.likesCounter, crev.commentsCounter])
        reviews.sort(key=lambda x: (-x[1], -x[2]))
        reviews = [reviews[i][0] for i in range(count)]
    reviews1 = []
    prevs = PReview.objects.all().order_by('-time')[:100 - count/2]
    crevs = CReview.objects.all().order_by('-time')[:100 - count/2]
    reviews1 = ([[f'0{review.id}', len(review.pros.split())+len(review.cons.split()), review.time] for review in prevs]\
        + [[f'1{review.id}', len(review.pros.split())+len(review.cons.split()), review.time] for review in crevs])
    reviews1.sort(key=lambda x: (-x[2], -x[1]))
    reviews = reviews + [review[0] for review in reviews1]
    dump(reviews, open('recommender/collobarative/anonymous_data.pkl', 'wb'))
    return reviews
