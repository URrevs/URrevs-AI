from copy import copy
from pickle import dump, load
import pandas as pd
from pyparsing import Or
from save_load_data import *

userDic = {}


def enum(**enums):
    return type('Enum', (), enums)


Tracker = enum(FULL_SCREEN_REVIEW=0.2, LIKE_OR_DISLIKE_REVIEW=0.3,
               SEE_MORE_REVIEW=0.1, COMMENT_REVIEW=0.4, DONT_LIKE=-1,
               UPVOTE_QUESTION=0.25, DOWNVOTE_QUESTION=-0.25, ANSWER_QUESTION=0.33,
               FULL_SCREEN_QUESTION=0.25, ASK_QUESTION=0.17)

Identifier = enum(PRODUCT_REVIEW=0, PRODUCT_QUESTION=1,
                  COMPANY_REVIEW=2, COMPANY_QUESTION=3)


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
       
        userDic[tracker['id']] = 1
        if len(tracker['review'])==24:
            tracker['review'] = addIdentifierToID(tracker['review'], identifier)   
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
previewTrackers1=   load(open('prevs.pkl', 'rb'))
previewTrackers2= load(open('prevs.pkl', 'rb'))

col = {'user_id': [],
       'item_id': [],
       'rating': []}

# Create DataFrame
df = pd.DataFrame(col)

df = loadDatFarame('user2review.pkl')
""" df = addTrackers(df, previewTrackers, Tracker.COMMENT_REVIEW, Identifier.PRODUCT_REVIEW)
df = addTrackers(df, previewTrackers1, Tracker.FULL_SCREEN_REVIEW, Identifier.COMPANY_REVIEW)
df = addTrackers(df, previewTrackers2, Tracker.ASK_QUESTION, Identifier.COMPANY_QUESTION)
saveDatFarame('user2review.pkl',df) """
#print(len(df['item_id'][0]))
print(previewTrackers)