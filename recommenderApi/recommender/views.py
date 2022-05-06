from random import choice
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import status
from django import forms
from recommenderApi import settings
from recommender.reviewsRecommender import ReviewContentRecommender

class Form(forms.Form):
    num = forms.IntegerField(label='Num of Recommendations', min_value=1, max_value=10)

# Create your views here.
def index(request):
    if request.method == 'GET':
        if request.META.get('HTTP_X_API_KEY') == settings.API_KEY_SECRET:
            response = {
                'message': 'Hello, world!!'
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