from typing import Generic
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterUserSerializer, UserSerializer
from loginapp.models import CustomUser, CardOwnership
from triadtrackerapp.models import TriadCard

class CustomUserCreate(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        reg_serializer = RegisterUserSerializer(data=request.data)
        if reg_serializer.is_valid():
            newuser = reg_serializer.save()
            cards = TriadCard.objects.all()
            for card in cards:
                CardOwnership(user=newuser, card=card).save()
            if newuser:
                return Response(status=status.HTTP_201_CREATED)
            return Response(reg_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BlacklistTokenView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try: 
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception as e:
            return Response(status=status.HTTP_4000_BAD_REQUEST)

class UserDetail(APIView):
    def get(self, request, format=None):
        user = CustomUser.objects.get(id=request.user.id)
        serializer = UserSerializer(user, many=False)

        return Response(serializer.data)