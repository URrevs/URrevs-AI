import pandas as pd
import numpy as np
from datetime import datetime as dt
from typing import Tuple
from sklearn.preprocessing import OneHotEncoder, LabelEncoder, MinMaxScaler
from pickle import dump, load
from sklearn.neighbors import NearestNeighbors
import os
from nltk import word_tokenize
from nltk.corpus import stopwords
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from pymongo import MongoClient
import certifi
from bson import ObjectId
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
import random
import sys
from pyparsing import Or
import requests
import json
import subprocess
from recommenderApi.settings import *

def enum(**enums):
    return type('Enum', (), enums)

Tracker = enum(FULL_SCREEN_REVIEW=REVIEW_FULL_SCREEN, LIKE_REVIEW=REVIEW_LIKE, DISLIKE_REVIEW=REVIEW_UNLIKE,
               SEE_MORE_REVIEW=REVIEW_SEE_MORE, COMMENT_REVIEW=REVIEW_COMMENT, DONT_LIKE_REVIEW=REVIEW_DONT_LIKE,
               UPVOTE_QUESTION=QUESTION_UPVOTE, DOWNVOTE_QUESTION=QUESTION_DOWNVOTE, ANSWER_QUESTION=QUESTION_ANSWER,
               FULL_SCREEN_QUESTION=QUESTION_FULL_SCREEN, ASK_QUESTION=QUESTION_MY_PRODUCTS_PAGE,
               DONT_LIKE_QUESTION=QUESTION_DONT_LIKE)

Identifier = enum(PRODUCT_REVIEW=0, PRODUCT_QUESTION=1,
                  COMPANY_REVIEW=2, COMPANY_QUESTION=3)

Review_Tracker = {
    'FULL_SCREEN': REVIEW_FULL_SCREEN, 
    'LIKE': REVIEW_LIKE, 
    'UNLIKE': REVIEW_UNLIKE, 
    'SEE_MORE': REVIEW_SEE_MORE, 
    'COMMENT': REVIEW_COMMENT, 
    'DONT_LIKE': REVIEW_DONT_LIKE
    }
Question_Tracker = {
    'FULL_SCREEN': QUESTION_FULL_SCREEN, 
    'UPVOTE': QUESTION_UPVOTE, 
    'DOWNVOTE': QUESTION_DOWNVOTE, 
    'ANSWER': QUESTION_ANSWER,
    'ABOUT_MY_PRODUCTS_PAGE': QUESTION_MY_PRODUCTS_PAGE,
    'DONT_LIKE': QUESTION_DONT_LIKE
    }
Mobile_Tracker = {
    'PROFILE': MOBILE_PROFILE, 
    'COMPARE': MOBILE_COMPARE, 
    'QUESTION': MOBILE_QUESTION
    }
