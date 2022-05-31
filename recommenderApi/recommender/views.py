from random import choice
from time import sleep
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import status
from django import forms
from recommenderApi import settings
from recommender.reviewsRecommender import ReviewContentRecommender
from django.views.decorators.csrf import csrf_exempt
import json
from .models import *
from .fill_db import *
from recommender.gamification.grading import Grading, FileData
from recommender.mongoDB.getData import *
from recommender.asyn_tasks.tasks import send_emails

# Create your views here.
def index(request):
    print('start async task')
    send_emails()
    return JsonResponse({'message': 'Hello, World!'})
# def index(request):
#     conn = MongoConnection()
#     phones = conn.get_product_reviews_likes_mongo(dt(2020, 1,1))
#     for phone in phones:
#         print(phone)
#     return JsonResponse({'success': True, 'status': 'ok'})
#-----------------------------------------------------------------------------------------------------
def start_training(request) -> JsonResponse:
    '''
    train the recommender system
    '''
    if request.method == 'GET':
        if request.META.get('HTTP_X_API_KEY') == settings.API_KEY_SECRET:
            try:
                # Async training run here
                response = {
                    'message': 'Training started'
                } 
                return JsonResponse(response, status=status.HTTP_200_OK)
            except:
                error = {
                    'success': False,
                    'status': 'process failed'
                }
                return JsonResponse(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
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
#-----------------------------------------------------------------------------------------------------
def get_reviews(request, userId: str) -> JsonResponse:
    '''
        Get the reviews of a user

        parameters: the user id
        output: the reviews of the user
    '''
    if request.method == 'GET':
        if request.META.get('HTTP_X_API_KEY') == settings.API_KEY_SECRET:
            reqBody = request.GET
            try:
                round = int(reqBody.get('round'))
                user = get_user(userId)
                if user == None:
                    check, user = check_new_user(userId)
                    if not check:
                        error = {
                            'success': False,
                            'status': "user doesn't exist"
                        }
                        return JsonResponse(error, status=status.HTTP_404_NOT_FOUND)
                try:
                    # here get the reviews for the user 'userId' at the round 'round'
                    # 1 - get the 4 ratios
                    # 2 - get the questions
                    # 3 - get the reviews
                    
                    response = {
                        'phoneRevs': [
                            user.PR
                        ],
                        'companyRevs': [
                            user.CR
                        ],
                        'phoneQuestions': [
                            user.PQ
                        ],
                        'companyQuestions': [
                            user.CQ
                        ]
                    }
                    return JsonResponse(response, status=status.HTTP_200_OK)
                except:
                    error = {
                        'success': False,
                        'status': 'process failed'
                    }
                    return JsonResponse(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            except:
                error = {
                    'success': False,
                    'status':'Missed valid round number'
                }
                return JsonResponse(error, status=status.HTTP_400_BAD_REQUEST)
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
@csrf_exempt
def get_review_grade(request):
    if request.method == 'POST':
        if request.META.get('HTTP_X_API_KEY') == settings.API_KEY_SECRET:
            reqBody = json.loads(request.body.decode('utf-8'))
            try:
                reviews: list = [
                    [reqBody['phoneRevPros']],
                    [reqBody['phoneRevCons']],
                    [reqBody['companyRevPros']],
                    [reqBody['companyRevCons']]
                ]
                # Calculate grade for review
                try:
                    grade = Grading()
                    response = {
                        'grade': grade.calc_TF_IDF(reviews)
                    }
                    return JsonResponse(response, status=status.HTTP_200_OK)
                except:
                    error = {
                        'success': False,
                        'status': 'process failed'
                    }
                    return JsonResponse(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
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
