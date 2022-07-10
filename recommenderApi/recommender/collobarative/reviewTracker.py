from recommender.sqliteDB.data import SQLite_Database
from recommenderApi.imports import pd, dump, load, Review_Tracker, Mobile_Tracker, Question_Tracker, dt
from recommender.collobarative.save_load_data import *
from recommenderApi.settings import *
from recommender.collobarative.recommend import MatrixFactorization
from recommender.mongoDB.getData import MongoConnection

class Trackers:
    def __init__(self, filepath = 'recommender/collobarative/itemsTrackers.pkl', loadfile = False):
        self.filepath = filepath
        self.allTrackerslst = []
        self.interactions = {}
        self.usersDic = {}
        self.df = None
        if loadfile:
            try: self.df: pd.DataFrame = loadDataFrame(filepath)
            except:
                # here recalculate the file again
                mongo = MongoConnection()
                if filepath == 'recommender/collobarative/itemsTrackers.pkl':
                    # collect all trackers again
                    items_trackers = mongo.get_all_items_trackers_mongo(date=dt(2022, 1, 1))
                    # recalculate the trackers
                    for item in items_trackers.keys():
                        for item_type in items_trackers[item]:
                            for tracker_type in items_trackers[item][item_type].keys():
                                if item == 'reviews':
                                    self.addReviewsTrackers(items_trackers[item_type][tracker_type],\
                                        Review_Tracker[tracker_type], item_type=='company')
                                elif item == 'questions':
                                    self.addQuestionsTrackers(items_trackers[item_type][tracker_type],\
                                        Review_Tracker[tracker_type], int(item_type=='company')+2)
                else:
                    # collect all trackers again
                    mobile_trackers = mongo.get_all_products_trackers_mongo(date=dt(2022, 1, 1))
                    # recalculate the trackers
                    for item_type in mobile_trackers.keys():
                        for tracker_type in mobile_trackers[item_type].keys():
                            self.addMobilesTrackers(mobile_trackers[item_type][tracker_type], Mobile_Tracker[tracker_type])
                # save the file
                self.saveTrackers()

    def addIdentifierToID(self, id, identifier):
        return f'{identifier}{id}'

    def removeIndentifierFromID(self, id):
        return str(id[1:])

    def getAllUsers(self):
        return self.df['user_id'].unique()

    def getRate(self, userId, itemId, col='item_id'):
        return self.df.loc[(self.df['user_id'] == userId) & (self.df[col] == itemId), 'rating']

    def getMostLikedReview(self, userId, item_type = 'product'):
        if item_type == 'product': item_type = '0'
        else: item_type = '1'
        return self.df.iloc[self.df.loc[(self.df['user_id'] == userId) & (self.df['item_id'].str.startswith(item_type)), 'rating'].idxmax()]['item_id']

    def getHatesReviews(self, userId):
        lst = self.df.loc[(self.df['user_id'] == userId) & (self.df['rating'] < -0.5), 'item_id'].values
        for item in lst:
            if len(item) == 25: item = item[1:]
        return lst

    def getMaxNLikedMobile(self, userId, n):
        mobiles_lst = load(open(f'recommenderApi/vars.pkl', 'rb'))['mobiles']
        lst = []
        userDF = self.df.loc[(self.df['user_id'] == userId) & (self.df['rating'] > 0.7) & (self.df['product_id'].isin(mobiles_lst))]
        for mobile in userDF.sort_values(by='rating', ascending=False)['product_id'].values:
            if mobile in mobiles_lst:
                lst.append(mobile); n -= 1
                if n == 0: break
        return lst

    def getRateByUser(self, userId):
        return self.df.loc[self.df['user_id'] == userId, 'rating']

    def setRate(self, userId, itemId, rate, col = 'item_id'):
        self.df.loc[(self.df['user_id'] == userId) & (self.df[col] == itemId), 'rating'] = rate
    
    def updateRateByUser(self, userId, rate):
        self.df.loc[(self.df['user_id'] == userId), 'rating'] += rate

    def downgradeRateByUser(self, userId):
        self.df.loc[(self.df['user_id'] == userId) & ((self.df['rating'] > MIN_LEVEL_OLD_TRACKERS_REACH) |
            (self.df['rating'] == MIN_LEVEL_OLD_TRACKERS_REACH+REVIEW_DONT_LIKE)), 'rating'] -= DAILY_DECREASE_FOR_OLD_TRACKERS

    def addNewRowToDataFrame(self, row):
        df2 = pd.DataFrame(row)
        self.df = pd.concat([self.df, df2], ignore_index=True, axis=0)
        return self.df

    def checkUserExist(self, userId):
        return ((self.df['user_id'] == userId) & (self.df['rating'] != -1)).any()

    def rowIsExist(self, userId, ItemId, col='item_id'):
        return ((self.df['user_id'] == userId) & (self.df[col] == ItemId)).any()

    def calculateUniqness(self, col='item_id'):
        return self.df.groupby(['user_id', col]).ngroups

    def updateLikes(self, itemId: str, val: int):
        if itemId in self.interactions.keys(): self.interactions[itemId][0] += val
        else: self.interactions[itemId] = [val, 0, 0]
    
    def updateComments(self, itemId: str):
        if itemId in self.interactions.keys(): self.interactions[itemId][1] += 1
        else: self.interactions[itemId] = [0, 1, 0]
    
    def updateHates(self, itemId: str):
        if itemId in self.interactions.keys(): self.interactions[itemId][2] += 1
        else: self.interactions[itemId] = [0, 0, 1]

    def addReviewsTrackers(self, trackers: list, trackerType: Review_Tracker, itemType: bool):
        # list to prevent duplicates in trackers
        trackerlst = []
        sqlite = SQLite_Database()
        for tracker in trackers:
            # check if (user, item) row is not in the trackers list
            if f"{tracker['id']}{tracker['review']}" not in trackerlst:
                if trackerType == REVIEW_LIKE: # 0.3
                    if (not itemType and sqlite.check_Prev_like(user=tracker['id'], review=tracker['review'][1:]))\
                    or (itemType and sqlite.check_Crev_like(user=tracker['id'], review=tracker['review'][1:])):
                        continue
                    else:
                        if itemType: sqlite.add_Crev_like(user=tracker['id'], review=tracker['review'][1:])
                        else: sqlite.add_Prev_like(user=tracker['id'], review=tracker['review'][1:])
                        self.updateLikes(tracker['review'], 1)
                elif trackerType == REVIEW_UNLIKE: # -0.3
                    if (not itemType and sqlite.check_Prev_like(user=tracker['id'], review=tracker['review'][1:]))\
                    or (itemType and sqlite.check_Crev_like(user=tracker['id'], review=tracker['review'][1:])):
                        if itemType: sqlite.remove_Crev_like(user=tracker['id'], review=tracker['review'][1:])
                        else: sqlite.remove_Prev_like(user=tracker['id'], review=tracker['review'][1:])
                        self.updateLikes(tracker['review'], -1)
                    else:
                        continue
                elif trackerType == REVIEW_COMMENT: self.updateComments(tracker['review']) # 0.4
                elif trackerType == REVIEW_DONT_LIKE: self.updateHates(tracker['review'])  # -1
                # check if (user, item) row is in the dataframe
                if not self.rowIsExist(tracker['id'], tracker['review']):
                    # add new row (user, item) to dataframe
                    newRow = {
                        'user_id': [tracker['id']],
                        'item_id': [tracker['review']],
                        'rating': [0]
                    }
                    self.df = self.addNewRowToDataFrame(newRow)
                # get the rate on (user, item) row in the dataframe
                rate = self.getRate(tracker['id'], tracker['review']).values[0]
                # if the tracker is hate then append the value 
                # else if tracker is unlike decrease the value to minimum 0
                if trackerType == REVIEW_DONT_LIKE: rate = trackerType 
                elif trackerType == REVIEW_UNLIKE: 
                    if rate != -1:
                        rate -= min(rate, abs(trackerType))
                        if rate < MIN_LEVEL_OLD_TRACKERS_REACH: rate = MIN_LEVEL_OLD_TRACKERS_REACH
                else:
                    if rate == -1: rate = -0.5 
                    rate = (rate + trackerType)
                # save the rate between 0 and 1
                if rate > 1: rate = 1
                # add the row to the trackers list to prevent duplicates
                trackerlst.append([f"{tracker['id']}{tracker['review']}"])
                # if the row (user, item) isn't in list of all trackers so this row first time to appear
                if f"{tracker['id']}{tracker['review']}" not in self.allTrackerslst:
                    # increase rate by 0.1 to elemenate the effect of downgrading on the new items
                    rate += DAILY_DECREASE_FOR_OLD_TRACKERS # 0.1
                    self.allTrackerslst.append([f"{tracker['id']}{tracker['review']}"])
                    
                    # form the daily activity for every user
                    if tracker['id'] not in self.usersDic.keys():
                        self.usersDic[tracker['id']] = [0, 0, 0, 0]
                    # if user DOESN'T LIKE the item decrement it
                    if trackerType == REVIEW_DONT_LIKE: self.usersDic[tracker['id']][itemType] -= 1
                    # if user LIKES the item increment it
                    else: self.usersDic[tracker['id']][itemType] += 1
                
                # update the rate on (user, item) row in the dataframe
                self.setRate(tracker['id'], tracker['review'], rate)
        return None
    
    def addQuestionsTrackers(self, trackers: list, trackerType: Question_Tracker, itemType: int):
        # list to prevent duplicates in trackers
        trackerlst = []
        sqlite = SQLite_Database()
        for tracker in trackers:
            # check if (user, item) row is not in the trackers list
            if f"{tracker['id']}{tracker['question']}" not in trackerlst:
                if trackerType == QUESTION_UPVOTE: # 0.3
                    if ((itemType == 2) and sqlite.check_Pques_upvote(user=tracker['id'], question=tracker['question'][1:]))\
                    or ((itemType == 3) and sqlite.check_Cques_upvote(user=tracker['id'], question=tracker['question'][1:])):
                        continue
                    else:
                        if itemType == 3: sqlite.add_Cques_upvote(user=tracker['id'], question=tracker['question'][1:])
                        elif itemType == 2: sqlite.add_Pques_upvote(user=tracker['id'], question=tracker['question'][1:])
                        self.updateLikes(tracker['question'], 1)
                elif trackerType == QUESTION_DOWNVOTE: # -0.3
                    if ((itemType == 2) and sqlite.check_Pques_upvote(user=tracker['id'], question=tracker['question'][1:]))\
                    or ((itemType == 3) and sqlite.check_Cques_upvote(user=tracker['id'], question=tracker['question'][1:])):
                        if itemType == 3: sqlite.remove_Cques_upvote(user=tracker['id'], question=tracker['question'][1:])
                        elif itemType == 2: sqlite.remove_Pques_upvote(user=tracker['id'], question=tracker['question'][1:])
                        self.updateLikes(tracker['question'], -1)
                    else:
                        continue
                elif trackerType == QUESTION_ANSWER: self.updateComments(tracker['question']) # 0.4
                elif trackerType == QUESTION_DONT_LIKE: self.updateHates(tracker['question'])  # -1
                # check if (user, item) row is in the dataframe
                if not self.rowIsExist(tracker['id'], tracker['question']):
                    # add new row (user, item) to dataframe
                    newRow = {
                        'user_id': [tracker['id']],
                        'item_id': [tracker['question']],
                        'rating': [0]
                    }
                    self.df = self.addNewRowToDataFrame(newRow)
                # get the rate on (user, item) row in the dataframe
                rate = self.getRate(tracker['id'], tracker['question']).values[0]
                # if the tracker is hate then append the value
                # else if tracker is unlike decrease the value to minimum 0
                if trackerType == QUESTION_DONT_LIKE: rate = trackerType 
                elif trackerType == QUESTION_DOWNVOTE: 
                    if rate != -1:
                        rate -= min(rate, abs(trackerType))
                        if rate < MIN_LEVEL_OLD_TRACKERS_REACH: rate = MIN_LEVEL_OLD_TRACKERS_REACH
                else:
                    if rate == -1: rate = -0.5
                    rate = (rate + trackerType)
                # save the rate between 0 and 1
                if rate > 1: rate = 1
                # add the row to the trackers list to prevent duplicates
                trackerlst.append([f"{tracker['id']}{tracker['question']}"])
                # if the row (user, item) isn't in list of all trackers so this row first time to appear
                if f"{tracker['id']}{tracker['question']}" not in self.allTrackerslst:
                    # increase rate by 0.1 to elemenate the effect of downgrading on the new items
                    rate += DAILY_DECREASE_FOR_OLD_TRACKERS # 0.1
                    self.allTrackerslst.append([f"{tracker['id']}{tracker['question']}"])

                    # form the daily activity for every user
                    if tracker['id'] not in self.usersDic.keys():
                        self.usersDic[tracker['id']] = [0, 0, 0, 0]
                    # if user DOESN'T LIKE the item decrement it
                    if trackerType == QUESTION_DONT_LIKE: self.usersDic[tracker['id']][itemType] -= 1
                    # if user LIKES the item increment it
                    else:
                        increment = 1
                        # if user enters page (about my product) icrease the Product questions the double 
                        # to increase probability of increasing num of product questions shown in the next day
                        if trackerType == QUESTION_MY_PRODUCTS_PAGE: increment = 2 
                        self.usersDic[tracker['id']][itemType] += increment
                # update the rate on (user, item) row in the dataframe
                self.setRate(tracker['id'], tracker['question'], rate)
        return None
    

    def addMobilesTrackers(self, trackers: list, trackerType: Mobile_Tracker):
        # list to prevent duplicates in trackers
        trackerlst = []
        for tracker in trackers:
            # check if (user, item) row is not in the trackers list
            if f"{tracker['id']}{tracker['phone']}" not in trackerlst:
                # check if (user, item) row is in the dataframe
                if not self.rowIsExist(tracker['id'], tracker['phone'], col='product_id'):
                    # add new row (user, item) to dataframe
                    newRow = {
                        'user_id': [tracker['id']],
                        'product_id': [tracker['phone']],
                        'rating': [0]
                    }
                    self.df = self.addNewRowToDataFrame(newRow)
                # get the rate on (user, item) row in the dataframe
                rate = self.getRate(tracker['id'], tracker['phone'], col='product_id').values[0]
                # append the value to old rate
                rate += trackerType
                # save the rate between 0 and 1
                if rate > 1: rate = 1
                elif rate < 0 and rate != -1: rate = MIN_LEVEL_OLD_TRACKERS_REACH # 0.1
                # add the row to the trackers list to prevent duplicates
                trackerlst.append([f"{tracker['id']}{tracker['phone']}"])
                # if the row (user, item) isn't in list of all trackers so this row first time to appear
                if f"{tracker['id']}{tracker['phone']}" not in self.allTrackerslst:
                    # increase rate by 0.1 to elemenate the effect of downgrading on the new items
                    rate += DAILY_DECREASE_FOR_OLD_TRACKERS # 0.1
                    self.allTrackerslst.append([f"{tracker['id']}{tracker['phone']}"])
                
                # update the rate on (user, item) row in the dataframe
                self.setRate(tracker['id'], tracker['phone'], rate, col='product_id')
        return None

    def down_old_items_grade(self):
        for user in self.usersDic.keys():
            self.downgradeRateByUser(user)
        return None

    def fill_most_liked_items(self):
        sql = SQLite_Database()
        for user in self.usersDic.keys():
            # print(user, self.getMostLikedReview(user)[1:])
            # get the most liked items for the user
            try: sql.update_add_Most_liked_Prev(user, self.getMostLikedReview(user)[1:])
            except: pass
            try: sql.update_add_Most_liked_Crev(user, self.getMostLikedReview(user, item_type='company')[1:])
            except: pass
        return None

    def saveTrackers(self):
        dump(self.df, open(self.filepath, 'wb'))
        return None
    
    def loadTrackers(self):
        self.df = load(open(self.filepath, 'rb'))

    def showTrackers(self):
        print(self.df)
        return None
    
    def resetTrackersFile(self, col='item_id'):
        column = {
            'user_id': [],
            col: [],
            'rating': []
        }
        self.df = pd.DataFrame(column)
        self.saveTrackers()

