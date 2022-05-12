from pickle import dump, load
import pandas as pd
from pyparsing import Or


def enum(**enums):
    return type('Enum', (), enums)


Tracker = enum(FULL_SCREEN=0.2, LIKE_OR_DISLIKE=0.3,
               SEE_MORE=0.1, COMMENT=0.4, DONT_LIKE=-1)

Identifier = enum(PRODUCT=0, COMPANY=1)

def loadDatFarame(fileName):
  df = load(open(fileName, 'rb'))
  return df

def saveDatFarame(fileName,df):
  dump(df, open(fileName, 'wb'))

def addIdentifierToID(id, identifier):
    return str(identifier) + id


def removeIndentifierFromID(id):
    return str(id[1:])


def getRate(df: pd.DataFrame, userId, itemId):
    return df.loc[(df['user_id'] == userId) & (df['item_id'] == itemId), 'rating']


def getRateByUser(df: pd.DataFrame, userId):
    return df.loc[df['user_id'] == userId, 'rating']


def setRate(df: pd.DataFrame, userId, itemId, rate):
    df.loc[(df['user_id'] == userId) & (
        df['item_id'] == itemId), 'rating'] = rate


def updateRateByUser(df: pd.DataFrame, userId, rate):
    df.loc[(df['user_id'] == userId), 'rating'] += rate


def addNewRowToDatarame(df: pd.DataFrame, row):
    df2 = pd.DataFrame(row)
    df = pd.concat([df, df2], ignore_index=True, axis=0)
    return df


def rowIsExist(df: pd.DataFrame, userId, ItemId):
    return ((df['user_id'] == userId) & (
        df['item_id'] == ItemId)).any()


def calculateUniqness():
    return df.groupby(['user_id', 'item_id']).ngroups


def addTrackers(df: pd.DataFrame, trackers: list, trackerType: Tracker, identifier: Identifier):
    for tracker in trackers:
        if tracker['review'][0] != str(Identifier.PRODUCT) and tracker['review'][0] != str(Identifier.COMPANY):
            tracker['review'] = addIdentifierToID(
                tracker['review'], identifier)
        if ~rowIsExist(df, tracker['id'], tracker['review']):
            newRow = {'user_id': [tracker['id']],
                      'item_id': [tracker['review']],
                      'rating': [0]}
            df = addNewRowToDatarame(df, newRow)
        rate = getRate(df, tracker['id'], tracker['review'])
        rate = rate+trackerType
        if rate.values > 1:
            rate = 1
        elif rate.values < 0:
            rate = 0
        setRate(df, tracker['id'], tracker['review'], rate)
    return df


previewTrackers = load(open('prevs.pkl', 'rb'))



col = {'user_id': [],
       'item_id': [],
       'rating': []}

# Create DataFrame
df = pd.DataFrame(col)

df=loadDatFarame('user2review.pkl')
print(df)