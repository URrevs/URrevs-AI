from django.http import JsonResponse
from rest_framework import status
from recommenderApi import settings

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
            round  = reqBody.get('round')
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

