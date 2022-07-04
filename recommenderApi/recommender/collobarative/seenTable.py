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

    def check_if_review_shown_before(self, userid, reviews, spaces):
        """
        reviews is a list of reviews
        """
        revs = []
        spcs = []
        if not self.df.empty:
            for i in range(len(reviews)):
                if self.df[(self.df['user_id'] == userid) & (self.df['item_id'] == reviews[i])].empty:
                    revs.append(reviews[i][1:])
                    spcs.append(spaces[i])
                    self.addToSeenTable(userid, [reviews[i]])
            # print(revs)
            return revs, spcs
        else:
            for review in reviews: self.addToSeenTable(userid, [review])
            # print(reviews)
            return reviews, spaces

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