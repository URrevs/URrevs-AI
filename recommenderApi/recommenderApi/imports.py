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
from recommenderApi.settings import *

def enum(**enums):
    return type('Enum', (), enums)

Identifier = enum(PRODUCT=0, COMPANY=1)
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
    'DONT_LIKE': QUESTION_DONT_LIKE
    }
Mobile_Tracker = {
    'PROFILE': MOBILE_PROFILE, 
    'COMPARE': MOBILE_COMPARE, 
    'QUESTION': MOBILE_QUESTION
    }
