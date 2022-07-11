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

    def check_if_review_shown_before(self, userid, reviews, spaces='', num='', known=[]):
        """
        reviews is a list of reviews
        """
        revs = []; revs2 = []
        check = True
        if spaces == '': check = False
        if check: spcs = []; spcs2 = []        
        if num == '': num = len(reviews)
        counter = 0
        if not self.df.empty:
            for i in range(len(reviews)):
                length = len(reviews[i])
                if length == 25: rev = reviews[i][1:]
                elif length == 23: rev = f'6{reviews[i]}'
                else: rev = reviews[i]
                if rev not in known:
                    if counter < num:
                        if self.df[(self.df['user_id'] == userid) & (self.df['item_id'] == reviews[i])].empty:
                            revs.append(rev)
                            if check: spcs.append(spaces[i])
                            self.addToSeenTable(userid, [reviews[i]])
                            counter += 1
                    else:
                        revs2.append(rev)
                        if check: spcs2.append(spaces[i])
        else:
            for i in range(len(reviews)):
                length = len(reviews[i])
                if length == 25: rev = reviews[i][1:]
                elif length == 23: rev = f'6{reviews[i]}'
                else: rev = reviews[i]
                if rev not in known:
                    if counter < num:
                        revs.append(rev)
                        if check: spcs.append(spaces[i])
                        self.addToSeenTable(userid, [reviews[i]])
                        counter += 1
                    else:
                        revs2.append(rev)
                        if check: spcs2.append(spaces[i])
        if not check: return revs
        if num == '': return revs, spcs
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