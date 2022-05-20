from multiprocessing.connection import wait
from random import choice
from time import sleep
from turtle import delay
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import status
from django import forms
from recommenderApi import settings
from recommender.reviewsRecommender import ReviewContentRecommender
from django.views.decorators.csrf import csrf_exempt
import json
from .models import *
from pickle import load
from .fill_db import *

class Form(forms.Form):
    num = forms.IntegerField(label='Num of Recommendations', min_value=1, max_value=10)

def train():
    print('train')
    sleep(10)
    print('finish')

def index(request):
    try:
        print('start')
        return JsonResponse({'message': 'hello, world !!'})
    except:
        pass
    finally:
        train()
#-----------------------------------------------------------------------------------------------------
def get_reviews(request, userId):
    if request.method == 'GET':
        if request.META.get('HTTP_X_API_KEY') == settings.API_KEY_SECRET:
            reqBody = request.GET
            round = reqBody.get('round')
            if round is None:
                error = {
                    'success': False,
                    'status':'Missed Round Number'
                }
                return JsonResponse(error, status=status.HTTP_400_BAD_REQUEST)
            else:
                response = {
                    'phoneRevs': [

                    ],
                    'companyRevs': [

                    ],
                    'phoneQuestions': [

                    ],
                    'companyQuestions': [

                    ]
                }
                return JsonResponse(response, status=status.HTTP_200_OK)
        else:
            error = {
                'success': False,
                'status': 'invalid API Key'
            }
            return JsonResponse(error, status=status.HTTP_401_UNAUTHORIZED)
    else:
        error = {
            'success': False,
            'status': 'process failed'
        }
        return JsonResponse(response, status=status.HTTP_400_BAD_REQUEST)
#-----------------------------------------------------------------------------------------------------
def html_recommend(request, userId):
    if request.method == 'POST':
        form = Form(request.POST)
        if form.is_valid():
            # user = request.POST['user']
            num = form.cleaned_data['num']
        rec = ReviewContentRecommender()
        df, check = rec.load_data(file_name='recommender/static/data/reviews.xlsx', sheet_name='product reviews')
        users = df['user'].dropna().values.tolist()
        reviews = df.index.values.tolist()
        mostInteractedReview = choice(reviews)
        lst, spaces = rec.recommend(referenceId=mostInteractedReview, path='recommender/static/data/', n_recommendations=num)
        return render(request, 'recommender/index.html', {
            'form': Form(),
            'users': users,
            'id': userId,
            'mostInteractedReview': mostInteractedReview,
            'recommendations': lst[1:]
        })
    rec = ReviewContentRecommender()
    df, check = rec.load_data(file_name='recommender/static/data/reviews.xlsx', sheet_name='product reviews')
    users = df['user'].dropna().values.tolist()
    return render(request, 'recommender/index.html', {
        'form': Form(),
        'id': userId,
        'users': users
    })
#-----------------------------------------------------------------------------------------------------
@csrf_exempt
def get_review_grade(request):
    if request.method == 'POST':
        if request.META.get('HTTP_X_API_KEY') == settings.API_KEY_SECRET:
            reqBody = json.loads(request.body.decode('utf-8'))
            try:
                phoneRevPros   = reqBody['phoneRevPros']
                phoneRevCons   = reqBody['phoneRevCons']
                companyRevPros = reqBody['companyRevPros']
                companyRevCons = reqBody['companyRevCons']
                # Calculate grade for review
                response = {
                    'grade': 30
                }
                return JsonResponse(response, status=status.HTTP_200_OK)
            except:
                # Request body is not valid
                error = {
                    'success': False,
                    'status': 'bad request'
                }
                return JsonResponse(error, status=status.HTTP_400_BAD_REQUEST)
        else:
            error = {
                'success': False,
                'status': 'invalid API Key'
            }
            return JsonResponse(error, status=status.HTTP_401_UNAUTHORIZED)
    else:
        # Request method is not valid
        error = {
            'success': False,
            'status': 'process failed'
        }
        return JsonResponse(error, status=status.HTTP_400_BAD_REQUEST)
#-----------------------------------------------------------------------------------------------------
similiar_phones = [
    '6256a7575f87fa90093a4bd2', 
    '6256a75b5f87fa90093a4bd6', 
    '6256a76d5f87fa90093a4bdb', 
    '6256a7715f87fa90093a4be2', 
    '6256a7835f87fa90093a4be8', 
    '6256a7875f87fa90093a4bec', 
    '6256a7925f87fa90093a4bf0', 
    '6256a7ab5f87fa90093a4bf4', 
    '6256a7b65f87fa90093a4bf8', 
    '6256a7ba5f87fa90093a4bfc', 
    '6256a7d45f87fa90093a4c01',
    '6256a7d85f87fa90093a4c06', 
    '6256a7dc5f87fa90093a4c0b', 
    '6256a7e05f87fa90093a4c0f', 
    '6256a7e35f87fa90093a4c13', 
    '6256a7f25f87fa90093a4c17', 
    '6256a7f65f87fa90093a4c1b', 
    '6256a7fa5f87fa90093a4c1f', 
    '6256a7fe5f87fa90093a4c23', 
    '6256a80c5f87fa90093a4c27'
]

def get_similiar_phones(request, phoneId):
    if request.method == 'GET':
        if request.META.get('HTTP_X_API_KEY') == settings.API_KEY_SECRET:
            response = {
                'similiar_phones': similiar_phones
            }
            return JsonResponse(response, status=status.HTTP_200_OK)
        else:
            error = {
                'success': False,
                'status': 'invalid API Key'
            }
            return JsonResponse(error, status=status.HTTP_401_UNAUTHORIZED)
    else:
        error = {
			'success': False,
			'status': 'process failed'
        }
        return JsonResponse(error, status=status.HTTP_400_BAD_REQUEST)
