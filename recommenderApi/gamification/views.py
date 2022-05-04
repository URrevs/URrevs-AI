from django.http import JsonResponse
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from recommenderApi import settings
import json

# Create your views here.
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
