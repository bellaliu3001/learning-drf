from rest_framework.views import APIView
from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from django.http import JsonResponse
from django.shortcuts import HttpResponse
from cryptography.fernet import Fernet
from accounts import models
import hashlib
import time


class Myauthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request._request.GET.get("token")
        print(token)
        token_obj = models.token.objects.filter(token=token).first()
        # print(request.META.get("REMOTE_ADDR"))
        if not token_obj:
            first_name = request._request.GET.get("first_name")
            last_name = request._request.GET.get("last_name")
            token = gen_token(first_name + last_name)
            obj, created = models.details.objects.update_or_create(
                first_name=first_name, last_name=last_name
            )
            token_obj, created = models.token.objects.update_or_create(
                details=obj, token=token
            )
            # raise exceptions.AuthenticationFailed("用户认证失败")
        return (token_obj.details, token_obj)  # 这里返回值一次给request.user,request.auth

    def authenticate_header(self, request):
        pass


def gen_token(msg):
    key = Fernet.generate_key()
    cipher = Fernet(key)
    salt = msg.encode("utf-8")
    token = cipher.encrypt(salt)
    return token.hex()


class Test(APIView):
    authentication_classes = [
        Myauthentication,
    ]

    def get(self, request, *args, **kwargs):
        print(request.user.first_name)
        print(request.auth.token)
        return HttpResponse("get is ok")