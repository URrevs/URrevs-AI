from pickle import dump, load
import pandas as pd


def addIdentifierToID(id, identifier):
    return str(identifier) + id

def removeIndentifierFromID(id):
    return str(id[1:])

def getRate(df:pd.DataFrame,userId,itemId):
  return df.loc[ (df['user_id']==userId) &(df['item_id']==itemId),'rating']

def setRate(df:pd.DataFrame,userId,rate):
  df.loc[ df['user_id']==userId,'rating']=rate

def addNewRowToDatarame(df:pd.DataFrame,row):
  df2 = pd.DataFrame(row)
  df = pd.concat([df, df2], ignore_index=True, axis=0)
  return df

def rowIsExist(df:pd.DataFrame,userId,ItemId):
  res= df.loc[ (df['user_id']  == userId) &(df['item_id']  == ItemId)].any().all()
  return res

previewTrackers = load(open('prevs.pkl', 'rb'))

for tracker in previewTrackers:
    tracker['review'] = addIdentifierToID(tracker['review'], 0)

col = {'user_id': [],
       'item_id': [],
       'rating': []}

# Create DataFrame
df = pd.DataFrame(col)
newRow = {'user_id': [previewTrackers[0]['id']],
                      'item_id': [previewTrackers[0]['review']],
                       'rating': [0.5]}
  