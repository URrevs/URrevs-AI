from datetime import datetime as dt
from recommender.collobarative.save_load_data import *

def dateAsNumber(date: dt, alert: bool = False) -> float:
    reference: dt = dt(2000, 1, 1)
    try:
        return (date - reference).total_seconds()
    except:
        if alert: print(f'"{date}" is not valid input')
        return 0

class SeenTable:
    def __init__(self, filepath = 'recommender/collobarative/seenTable.pkl', loadfile = False):
        self.filepath = filepath
        self.df = None
        if loadfile:
            self.df = loadDataFrame(filepath)

    def addToSeenTable(self, userId, itemIds):
        date=dateAsNumber(dt.now())
        for itemId in itemIds:
            newRow = {
                'user_id': [userId],
                'item_id': [itemId],
                'date': [date]
            }
            self.df=addNewRowToDatarame(self.df, newRow)
        saveDataFrame(self.filepath, self.df)
    
    def addToSeenTableMod(self, userId, itemIds):
        date=dateAsNumber(dt.now())
        for itemId in itemIds:
            newRow = {
                'user_id': [userId],
                'item_id': [itemId],
                'date': [date]
            }
            self.df=addNewRowToDatarame(self.df, newRow)
        saveDataFrame(self.filepath, self.df)

    def check_item_not_exist(self, userid, itemId):
        return self.df[(self.df['user_id'] == userid) & (self.df['item_id'] == itemId)].empty

    def check_if_review_shown_before(self, userid, reviews, spaces, num=0):
        """
        reviews is a list of reviews
        """
        revs = []; spcs = []
        revs2 = []; spcs2 = []
        if num == 0: num = len(reviews)
        i = 0
        for i in range(len(reviews)):
            if not self.df.empty:
                if i < num:
                    if self.df[(self.df['user_id'] == userid) & (self.df['item_id'] == reviews[i])].empty:
                        if len(reviews[i]) == 25: revs.append(reviews[i][1:])
                        elif len(reviews[i]) == 24: revs.append(reviews[i])
                        spcs.append(spaces[i])
                        self.addToSeenTable(userid, [reviews[i]])
                else: 
                    if len(reviews[i]) == 25: revs2.append(reviews[i][1:])
                    elif len(reviews[i]) == 24: revs2.append(reviews[i])
                    spcs2.append(spaces[i])
            else:
                for i in range(len(reviews)):
                    if i < num:
                        if len(reviews[i]) == 25: revs.append(reviews[i][1:])
                        elif len(reviews[i]) == 24: revs.append(reviews[i])
                        spcs.append(spaces[i])
                        self.addToSeenTable(userid, [reviews[i]])
                    else: 
                        if len(reviews[i]) == 25: revs2.append(reviews[i][1:])
                        elif len(reviews[i]) == 24: revs2.append(reviews[i])
                        spcs2.append(spaces[i])
        if num == 0: return revs, spcs
        else: return revs, spcs, revs2, spcs2

    def removeExpiredDateFromSeenTable(self, amount=432000):
        """ amount unit is in seconds ->> 432000 corsponding to 5 days """
        date = dateAsNumber(dt.now())
        self.df.drop(self.df[date-self.df['date'] >= amount].index, inplace = True)
        saveDataFrame(self.filepath, self.df)

    def resetSeenTable(self):
        col = {
            'user_id': [],
            'item_id': [],
            'date': []
        }
        saveDataFrame(self.filepath, pd.DataFrame(col))
        return None

    def showSeenTable(self, tablePath='recommender/collobarative/seenTable.pkl'):
        df = load(open(tablePath, 'rb'))
        print('seentable: ', df)
        return None

# print('SeenTable created successfully', df)
""" print(dateAsNumber(dt.now())-706074198.937577) """
""" removeExpiredDateFromSeenTable(tablePath='seenTable.pkl',amount=750) """