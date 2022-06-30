from recommender.sqliteDB.data import SQLite_Database
from recommenderApi.imports import pd, dump, load, Review_Tracker, Mobile_Tracker
from recommender.collobarative.save_load_data import *
from recommenderApi.settings import *
from recommender.collobarative.recommend import MatrixFactorization

class Trackers:
    def __init__(self, filepath = 'recommender/collobarative/itemsTrackers.pkl', loadfile = False):
        self.filepath = filepath
        self.allTrackerslst = []
        self.interactions = {}
        self.usersDic = {}
        self.df = None
        if loadfile:
            self.df: pd.DataFrame = loadDataFrame(filepath)

    def addIdentifierToID(self, id, identifier):
        return f'{identifier}{id}'

    def removeIndentifierFromID(self, id):
        return str(id[1:])

    def getRate(self, userId, itemId, col='item_id'):
        return self.df.loc[(self.df['user_id'] == userId) & (self.df[col] == itemId), 'rating']

    def getMostLikedReview(self, userId, item_type):
        if item_type == 'product': item_type = '0'
        else: item_type = '1'
        return self.df.iloc[self.df.loc[(self.df['user_id'] == userId) & (self.df['item_id'].str.startswith(item_type)), 'rating'].idxmax()]['item_id']


    def getMaxNLikedMobile(self, userId, n):
        # model = MatrixFactorization(columns=['user_id', 'product_id', 'rating', 'rating_pred'])
        # mobiles = set(model.recommend_mobiles(userId, n_recommendations=n, pred=False).flatten())
        mobiles_lst = load(open(f'recommenderApi/vars.pkl', 'rb'))['mobiles']
        lst = []
        # for mobile in mobiles: 
        #     if mobile in mobiles_lst:
        #         lst.append(mobile); n -= 1
        #         if n == 0: return lst
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

    def addItemsTrackers(self, trackers: list, trackerType: Review_Tracker, itemType: bool):
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

