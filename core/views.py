from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.utils.timezone import now
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.models import Token  

from .serializers import RegisterSerializer, CharacterSerializer, UserCharaterSerializer
from .utils import verify_telegram_auth  
from . import models



class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile_view(request):
    user = request.user
    return Response({
        'username': user.username,
        'email': user.email,
        'id': user.id,
    })
    
    
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
    
@csrf_exempt
@api_view(['POST'])
def bot_login(request):
    data = request.data
    bot_token = "7585286219:AAGltBgrhw7MZy_9U3gDyjifCJ7D7LPewAk"

    if not verify_telegram_auth(data, bot_token):
        return Response({"error": "Invalid Telegram data"}, status=status.HTTP_400_BAD_REQUEST)

    telegram_id = data.get("id")
    username = data.get("username", f"user_{telegram_id}")
    first_name = data.get("first_name", "")

    user, created = User.objects.get_or_create(
        username=telegram_id,
        defaults={"first_name": first_name}
    )

    user.last_login = now()
    user.save()

    token, _ = Token.objects.get_or_create(user=user)

    return Response({"token": token.key, "user": username})



class UnlockSkinView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            data = request.data 
            user_id = data.get('user_id')
            skin_id = data.get('skin_id')

            if not user_id or not skin_id:
                return Response({'error': 'user_id and skin_id are required'}, status=status.HTTP_400_BAD_REQUEST)

            user = get_object_or_404(User, id=user_id)
            skin = get_object_or_404(models.Skin, id=skin_id)

            if models.Purchase.objects.filter(user=user, skin=skin).exists():
                return Response({'message': 'Skin already unlocked'}, status=status.HTTP_200_OK)

            models.Purchase.objects.create(user=user, skin=skin)

            return Response({
                'message': f'Skin "{skin.name}" unlocked for user {user.username}',
                'skin_id': skin.id,
                'character': skin.character.name
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def telegram_login_page(request):
    return render(request, 'login.html')

def dashboard_page(request):
    return HttpResponse("Login Successfully")


class CharacterListView(APIView):
    # permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        characters = models.Character.objects.all()
        serializer = CharacterSerializer(characters, many=True, context={'user': request.user})
        return Response(serializer.data)
    


class UserCharaterCreateAPIView(APIView):
    def post(self, request):
        serializer = UserCharaterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)