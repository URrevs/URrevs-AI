# from random import choice
# from time import sleep
from django.http import JsonResponse
# from django.shortcuts import render
from recommender.collobarative.questions import *
from rest_framework import status
# from django import forms
from recommenderApi.imports import *
from recommender.collobarative.train import update_values
from recommenderApi.settings import *
# from recommender.reviewsRecommender import ReviewContentRecommender
from django.views.decorators.csrf import csrf_exempt
from recommender.collobarative.train import train_and_update
import json
from .models import *
from .fill_db import *
from recommender.gamification.grading import Grading
from recommender.mongoDB.getData import *
from recommender.mongoDB.sendData import *
from recommender.asyn_tasks.tasks import start_async, start_async2
from recommender.sqliteDB.data import *
from recommender.collobarative.recommend import *
# from recommender.collobarative.train import *
from recommender.recommend import *
from recommender.mobiles1.getPhones import Similar_Phones
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

    # update_values(dt(2022, 7, 1))
    
    # train_and_update(dt(2020, 1,1), first=False)
    # Trackers(loadfile=True).showTrackers()
    # for user in Trackers(loadfile=True).getAllUsers():
    #     print(user)
    # Trackers('recommender/collobarative/mobileTrackers.pkl', loadfile=True).showTrackers()
    # print(Trackers(loadfile=True).getHatesReviews('62bcf0887098c747b5c99613'))
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
    # start_async2.delay()
    # users = MongoConnection().get_users_mongo(dt(2020, 1,1))
    # for user in users:
    #     print(user)
    #     break
    #     sqlite.create_new_Preview_ifNotExist(review)
    # sql = SQLite_Database()
    # sql.update_add_Most_liked_Prev('626b28707fe7587a42e3dfeb', '627406a18cc1cefd58623f9e')
    # like = sql.get_Most_liked_Prev('626b28707fe7587a42e3dfeb')
    # print(like)

    # update_values(dt(2022, 7, 1))
    # ques = getAllQuetion(filterType=2)
    # print('all ques loaded')
    # print(filterQuetions(user='626b28707fe7587a42e3dfeb', questions=ques.keys(), sort=[], filterType=2, 
    #         sort_exist=False))

    
    # MongoConnection().get_product_questions_mongo(dt(2022, 7, 1))
    # SQLite_Database().add_Prev_like('62c22279d7965c45d2c698eb', '62c264e5ad43f157e4ef19b6')
    # SQLite_Database().create_Preview(id='fferre', user='62c22279d7965c45d2c698eb', phone='6256a76d5f87fa90093a4bdb',
    #         rate=1, rate1=1, rate2=1, rate3=1, rate4=1, rate5=1, rate6=1, date=12332435, pros='', cons='')
    # visits = [{'id': '62c22279d7965c45d2c698eb'}, {'id': '62c22279d7965c45d2c698eb'}]
    # visits_lst: list = []
    # sql = SQLite_Database()
    # for visit in visits:
    #     visits_lst.extend(sql.get_owned_mobiles_questions(str(visit['id'])))
    # print(visits_lst)
    # SQLite_Database().get_owned_mobiles_questions('62c22279d7965c45d2c698eb')
    # Similar_Phones().generate_n_similars('6256a7e35f87fa90093a4c13')
    # Similar_Phones().min_max_scale(repeat = False)
    # Similar_Phones().min_max_scale(repeat = True)
    # Similar_Phones().add_new_mobiles()
    # train_and_update(dt(2022, 6, 30), first=0)
    # Grading().calc_TF_IDF()
    return JsonResponse({'message': 'Deployed Successfully'})
#-----------------------------------------------------------------------------------------------------
def reset_files(request) -> JsonResponse:
    '''
        reset all files for training
    '''
    if request.method == 'GET':
        if request.META.get('HTTP_X_API_KEY') == API_KEY_SECRET:
            try:
                # Trackers().resetTrackersFile()
                # Trackers('recommender/collobarative/mobileTrackers.pkl').resetTrackersFile(col='product_id')
                SeenTable().resetSeenTable()
                response = {
                    'message': 'All files reseted'
                } 
                return JsonResponse(response, status=status.HTTP_200_OK)
            except Exception as e:
                print(e)
                error = {
                    'success': False,
                    'status': 'process failed',
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
            try:
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
                
                subprocess.call([START_REDIS], shell=True)
                print('Start redis')
                subprocess.call([START_CELERY], shell=True)
                print('Start celery succeeded')
                print('start async task')
                start_async.delay(date, first)
                # train_and_update(date, first=first)
                response = {
                    'message': 'Training started'
                }
                return JsonResponse(response, status=status.HTTP_200_OK)
            except Exception as e:
                print(e)
                error = {
                    'success': False,
                    'status': 'process failed',
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
def stop_training(request) -> JsonResponse:
    '''
    train the recommender system
    '''
    if request.method == 'GET':
        if request.META.get('HTTP_X_API_KEY') == API_KEY_SECRET:
            try:
                subprocess.call([STOP_CELERY], shell=True)
                print('Stopping celery succeeded')
                subprocess.call([STOP_REDIS], shell=True)
                print('Stopping redis succeeded')
                response = {
                    'message': 'Training stoped'
                }
                return JsonResponse(response, status=status.HTTP_200_OK)
            except Exception as e:
                print('Failed to stop training services', e)
                error = {
                    'success': False,
                    'status': 'process failed',
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
                    print(e)
                    error = {
                        'success': False,
                        'status': 'process failed',
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
                    prevs, crevs, pques, cques, total = anonymous_recommend(round)
                    response = {
                        'phoneRevs': prevs,
                        'companyRevs': crevs,
                        'phoneQuestions': pques,
                        'companyQuestions': cques,
                        'total': total
                    }
                    return JsonResponse(response, status=status.HTTP_200_OK)
                except Exception as e:
                    print(e)
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
                except Exception as e:
                    print(e)
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
def get_similiar_phones(request, phoneId):
    if request.method == 'GET':
        if request.META.get('HTTP_X_API_KEY') == API_KEY_SECRET:
            if SQLite_Database().get_mobile(phoneId) == None:
                error = {
                    'success': False,
                    'status': 'invalid phone id'
                }
                return JsonResponse(error, status=status.HTTP_400_BAD_REQUEST)
            try: 
                recs = Similar_Phones().generate_n_similars(phoneId)
                response = {
                    'similiar_phones': recs
                }
                return JsonResponse(response, status=status.HTTP_200_OK)
            except Exception as e:
                print(e)
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
