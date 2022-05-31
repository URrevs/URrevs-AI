from cmath import inf
from venv import create
from numpy import argmax, argmin
from recommender.models import User, PReview, CReview, Company, Mobile
from datetime import datetime as dt
from pymongo import MongoClient
import certifi

def update_ratios(diffs: list, old: list) -> list:
    '''
        function to calculate the ratios based on the interactions and the old state

        parameters: interaction list and the old state list
        output: the new list of ratios
    '''
    new = old.copy()
    diffs_min = diffs.copy()
    max = [7, 5, 3, 3]
    counter = 4
    while counter > 1:
        while True:
            max_idx = argmax(diffs)
            diffs[max_idx] = -1
            counter -= 1
            if new[max_idx] < max[max_idx] or counter == 0:
                break
        while True:
            min_idx = argmin(diffs_min)
            diffs_min[min_idx] = inf
            counter -= 1
            if new[min_idx] > 1 or counter == 0:
                break
        if max[max_idx] > old[max_idx] and old[min_idx] > 1 and old[min_idx] != old[max_idx]:
            new[max_idx] = old[max_idx] + 1
            new[min_idx] = old[min_idx] - 1
    return new

# print(getRatios([6, 3, 6, 1], [5, 1, 3, 1]))

def get_user(id: str = ''):
    if id == '':
        users = User.objects.all()
    else:
        try:
            users = User.objects.get(pk= id)
        except User.DoesNotExist:
            return None
    return users

def create_user(id: str, name: str):
    try:
        user = User(id=id, name=name)
        user.save()
        return user
    except Exception as e:
        print(e)
        return None

# def getReviews(id: str = '') -> list:
#     if id == '':
#         reviews = Review.objects.all()
#     else:
#         try:
#             reviews = Review.objects.get(pk= id)
#         except Review.DoesNotExist:
#             return []
#     return reviews

def create_company(id: str = '', name: str = ''):
    try:
        company = Company(id=id, name=name)
        company.save()
        return company
    except Exception as e:
        print(e)
        return None

def DB_get_users(date: dt):
    CONNECTION_STRING = 'mongodb+srv://urrevsai:urrevsrocks@urrevs-ai.xmex9.mongodb.net/urrevs?retryWrites=true&w=majority'
    cluster = MongoClient(CONNECTION_STRING, tlsCAFile=certifi.where())

    db = cluster['urrevs']
    users_col = db['users']

    cursor = users_col.find({'createdAt': {'$gte': date}}, {'_id': 1, 'name': 1})
    return cursor

def create_mobile(id: str = '', name: str = '', company: str = '', price: int = 0):
    try:
        company = Company.objects.get(id=company)
        mobile = Mobile(id=id, name=name, company=company, price=price)
        mobile.save()
        return mobile
    except Exception as e:
        print(e)
        return None

def create_Preview(id: str, user: str, phone: str, rate: int, rate1, rate2, rate3, rate4, rate5, rate6,
                date: dt, pros: str, cons: str):
    try:
        user = User.objects.get(id=user)
        phone = Mobile.objects.get(id=phone)
        review = PReview(id=id, userId=user, productId=phone, rating=rate, time=date, pros=pros, cons=cons,
                rating1=rate1, rating2=rate2, rating3=rate3, rating4=rate4, rating5=rate5, rating6=rate6)
        review.save()
        return review
    except Exception as e:
        print(e)
        return None


def create_Creview(id: str, user: str, company: str, rate: int, date: dt, pros: str, cons: str):
    try:
        user = User.objects.get(id=user)
        company = Company.objects.get(id=company)
        review = CReview(id=id, userId=user, companyId=company, rating=rate, time=date, pros=pros, cons=cons)
        review.save()
        return review
    except Exception as e:
        print(e)
        return None
