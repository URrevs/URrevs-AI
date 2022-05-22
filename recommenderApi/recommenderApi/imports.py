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