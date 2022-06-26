# from random import choice
# from time import sleep
from django.http import JsonResponse
# from django.shortcuts import render
from rest_framework import status
# from django import forms
from recommenderApi.imports import *
from recommenderApi.settings import *
# from recommender.reviewsRecommender import ReviewContentRecommender
from django.views.decorators.csrf import csrf_exempt
import json
from .models import *
from .fill_db import *
from recommender.gamification.grading import Grading, FileData
from recommender.mongoDB.getData import *
from recommender.mongoDB.sendData import *
from recommender.asyn_tasks.tasks import start_async
from recommender.sqliteDB.data import *
from recommender.collobarative.recommend import *
# from recommender.collobarative.train import *
from recommender.recommend import *
# from recommender.mobiles.getPhones import get_phones

# Create your views here.
def index(request):
    # recommender = MatrixFactorization(n_epochs = 30, alert = True)
    # recommender.online_train()
    # print(recommender.test())
    # print(loadDatFarame('recommender/collobarative/seenTable.pkl'))
    # print(recommender.recommend('u5'))
    # likes = MongoConnection().get_product_reviews_likes_mongo(dt(2020, 1,1))
    # for like in likes:
    #     print(like)
    # print(likes)
    # try:
    #     users = MongoConnection().get_users_mongo(dt(2020, 1,1))
    #     for user in users:
    #         print(user)
    # except:
    #     print('error')
    # print(get_phones())
    # update_values(dt(2020, 1,1))
    # train_and_update(dt(2020, 1,1), first=False)
    # Trackers(loadfile=True).showTrackers()
    # Trackers('recommender/collobarative/mobileTrackers.pkl', loadfile=True).showTrackers()
    # train(first = True)
    # SeenTable(loadfile=True).resetSeenTable()
    # print('seentable============================')
    # SeenTable(loadfile=True).showSeenTable()
    # model = MatrixFactorization(n_epochs = 30, alert = True)
    # model.load_model()
    # print(model.recommend_items('628a60526811b1d11dbba4e1'))

    # print(check_interactions_existance('628a60526811b1d11dbba4e1'))
    # print(get_max_n_liked_mobiles('628a60526811b1d11dbba4e1', n = 5))
    # mobiles = PReview.objects.values_list('productId', flat=True).distinct()
    # print(mobiles)
    # print(get_most_liked_reviews('628a60526811b1d11dbba4e1'))
    # Trackers(loadfile=True).resetTrackersFile()
    # print('trackers=============================')
    # Trackers(loadfile=True).showTrackers()
    # users = {}
    # dump(users, open('recommender/users.pkl', 'wb'))
    # print(recommend('628a60526811b1d11dbba4e1', 3, 8,4,6,2))

    # model = ReviewContentRecommender()
    # model.preprocessing('company', 'recommender/reviews/crevs.pkl')
    # res, des = model.recommend(referenceId='627406a68cc1cefd58624016', recommend_type='product', 
    # n_recommendations=3, items=['628e30166a09c359b2d913bc', '628e2ace6a09c359b2d911c2', '628d0c28909f0465573ff0f6'])
    # print(res.values, des)

    # model = MatrixFactorization(n_epochs = 30, alert = True)
    # model.train()
    # SeenTable().resetSeenTable()          
    # # print(model.test())
    # r = model.recommend('628a60526811b1d11dbba4e1', n_recommendations=10, item_type=1)
    # print(r)
    # calc_anonymous_data()
    # print('start async task')
    # send_emails.delay(22)
    # print('after async task')
    return JsonResponse({'message': 'Deployed Successfully'})
#-----------------------------------------------------------------------------------------------------
def reset_files(request) -> JsonResponse:
    '''
        reset all files for training
    '''
    if request.method == 'GET':
        if request.META.get('HTTP_X_API_KEY') == API_KEY_SECRET:
            try:
                Trackers().resetTrackersFile()
                Trackers('recommender/collobarative/mobileTrackers.pkl').resetTrackersFile(col='product_id')
                SeenTable().resetSeenTable()
                response = {
                    'message': 'All files reseted'
                } 
                return JsonResponse(response, status=status.HTTP_200_OK)
            except Exception as e:
                error = {
                    'success': False,
                    'status': 'process failed',
                    'error': str(e)
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
def start_training(request) -> JsonResponse:
    '''
    train the recommender system
    '''
    if request.method == 'GET':
        if request.META.get('HTTP_X_API_KEY') == API_KEY_SECRET:
            reqBody = request.GET
            # try:
            try:
                first = bool(reqBody.get('first') == '1')
            except:
                first = False
            # Sync training run here
            if first: date = dt(2018, 1, 1)
            else:
                try:
                    var = load(open('recommenderApi/vars.pkl', 'rb'))
                    date = var['date']
                except:
                    date =  MongoConnection().get_last_training_time()
            print('start async task')
            print(date)
            start_async.delay(date, first)
            # train_and_update(date, first=first)
            response = {
                'message': 'Training started'
            }
            return JsonResponse(response, status=status.HTTP_200_OK)
            # except Exception as e:
            #     error = {
            #         'success': False,
            #         'status': 'process failed',
            #         'error': str(e)
            #     }
            #     return JsonResponse(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
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
def get_recommendations(request, userId: str) -> JsonResponse:
    '''
        Get the reviews of a user

        parameters: the user id
        output: the reviews of the user
    '''
    if request.method == 'GET':
        if request.META.get('HTTP_X_API_KEY') == API_KEY_SECRET:
            reqBody = request.GET
            try:
                round = int(reqBody.get('round'))
                try:
                    user1 = get_user(userId)
                    if user1 == None:
                        check, user = MongoConnection().check_new_user_mongo(userId)
                        if not check:
                            error = {
                                'success': False,
                                'status': "user doesn't exist"
                            }
                            return JsonResponse(error, status=status.HTTP_404_NOT_FOUND)
                    if user1 != None:
                        # print(user1, round)
                        productReviews, companyReviews, productQuestions, companyQuestions, total = recommend(
                            userId=userId, 
                            round=round, 
                            PR=user1.PR, 
                            CR=user1.CR,
                            PQ=user1.PQ, 
                            CQ=user1.CQ
                        )
                    else:
                        productReviews, companyReviews, productQuestions, companyQuestions, total = recommend(
                            userId=userId, 
                            round=round, 
                            PR=2*ROUND_NUM_OF_REVIEWS//5, 
                            CR=ROUND_NUM_OF_REVIEWS//5,
                            PQ=3*ROUND_NUM_OF_REVIEWS//10, 
                            CQ=ROUND_NUM_OF_REVIEWS//10
                        )
                    response = {
                        'phoneRevs': productReviews,
                        'companyRevs': companyReviews,
                        'phoneQuestions': productQuestions,
                        'companyQuestions': companyQuestions,
                        'total': total
                    }
                    return JsonResponse(response, status=status.HTTP_200_OK)
                except Exception as e:
                    error = {
                        'success': False,
                        'status': 'process failed',
                        'error': str(e)
                    }
                    return JsonResponse(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            except Exception as e:
                error = {
                    'success': False,
                    'status':'Missed valid round number',
                        'error': str(e)
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
def get_anonymous_recommendations(request) -> JsonResponse:
    '''
        Get the reviews for anonymous user

        parameters: the user id
        output: the reviews of the user
    '''
    if request.method == 'GET':
        if request.META.get('HTTP_X_API_KEY') == API_KEY_SECRET:
            reqBody = request.GET
            try:
                round = int(reqBody.get('round'))
                try:
                    product, company, total = anonymous_recommend(round)
                    response = {
                        'phoneRevs': product,
                        'companyRevs': company,
                        'phoneQuestions': [],
                        'companyQuestions': [],
                        'total': total
                    }
                    return JsonResponse(response, status=status.HTTP_200_OK)
                except Exception as e:
                    error = {
                        'success': False,
                        'status': 'process failed',
                        'error': str(e)
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
        if request.META.get('HTTP_X_API_KEY') == API_KEY_SECRET:
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
        if request.META.get('HTTP_X_API_KEY') == API_KEY_SECRET:
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
