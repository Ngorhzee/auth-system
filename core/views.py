from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from .serialiser import UsersSerialiser
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404

@api_view(['POST'])
def login(request: Request)->Response:
    user = get_object_or_404(User, username = request.data['username'])
    if not user.check_password(request.data['password']):
        return Response({"error":"Password Incorrect"})
    token, created = Token.objects.get_or_create(user=user)
    serialiser = UsersSerialiser(instance=user)

    return Response({"token": token, "user":serialiser.data})


@api_view(['POST'])
def signup(request: Request)->Response:
    serialiser = UsersSerialiser(data=request.data)
    if serialiser.is_valid():
        serialiser.save()
        user = User.objects.get(username = request.data["username"])
        user.set_password(request.data["password"])
        user.save()
        token = Token.objects.create(user=user)
        return Response({"token":token,"user": serialiser.data})
    return Response({"error":serialiser.errors})


@api_view(['POST'])
def testToken(request: Request)->Response:
    return Response()