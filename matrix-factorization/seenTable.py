from datetime import datetime as dt
from save_load_data import *

seenTablePath='../seenTable.pkl'

def dateAsNumber(date: dt) -> float:

  reference: dt = dt(2000, 1, 1)
  try:
      return (date - reference).total_seconds()
  except:
      if self.alert:
          print(f'"{date}" is not valid input')
      return 0

def addToSeenTable(df,userId,itemIds):
    date=dateAsNumber(dt.now())
    for itemId in itemIds:
        newRow = {'user_id': [userId],
                  'item_id': [itemId],
                  'date': [date]}
        df=addNewRowToDatarame(df,newRow)
    saveDatFarame(seenTablePath,df)

def removeExpiredDateFromSeenTable(tablePath=seenTablePath,amount=432000):
    """ amount unit is in seconds ->> 432000 corsponding to 5 days """
    df=loadDatFarame(tablePath)
    date=dateAsNumber(dt.now())
    """ print(date- df['date']) """
    df.drop(df[date- df['date']  >= amount].index, inplace = True)
    saveDatFarame(tablePath,df)

col = {'user_id': [],
       'item_id': [],
       'date': []}

# Create DataFrame
df = pd.DataFrame(col)

""" saveDatFarame('seenTable.pkl',df) """
""" print(dateAsNumber(dt.now())-706074198.937577) """
""" removeExpiredDateFromSeenTable(tablePath='seenTable.pkl',amount=750) """