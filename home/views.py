from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.conf import settings
from .serializers import ForgotPasswordSerializer
from django.contrib.auth import authenticate, login
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer,UserLoginSerializer,PasswordChangeSerializer
from django.contrib.auth.forms import PasswordChangeForm
from rest_framework.views import APIView
from rest_framework.response import Response

from django.contrib.auth.forms import SetPasswordForm
from rest_framework.views import APIView
from rest_framework.response import Response









class PasswordChangeView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = PasswordChangeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        old_password = serializer.validated_data['old_password']
        new_password = serializer.validated_data['new_password']

        if request.user.is_anonymous:
            return Response({'detail': 'Anonymous users cannot change passwords.'}, status=400)

        user = request.user

        if not user.check_password(old_password):
            return Response({'detail': 'Invalid old password.'}, status=400)

        form = SetPasswordForm(user=user, data={'new_password1': new_password, 'new_password2': new_password})
        if form.is_valid():
            form.save()
            return Response({'detail': 'Password changed successfully.'})
        else:
            return Response(form.errors, status=400)


# class PasswordChangeView(APIView):
#     def post(self, request, *args, **kwargs):
#         serializer = PasswordChangeSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         user = request.user
#         old_password = serializer.validated_data['old_password']
#         new_password = serializer.validated_data['new_password']

#         form = PasswordChangeForm(user=user, data=request.data)
#         if form.is_valid():
#             form.save()
#             return Response({'detail': 'Password changed successfully.'})
#         else:
            return Response(form.errors, status=400)




class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {'message': 'User registered successfully.'},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        
class UserLoginView(APIView):
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        user = authenticate(request, username=username, password=password)
        if user:
            # Remove the login() function call
            return Response({'message': 'Logged in successfully.'})
        return Response({'message': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# class UserLoginView(APIView):
#     serializer_class = UserLoginSerializer

#     def post(self, request):
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         username = serializer.validated_data['username']
#         password = serializer.validated_data['password']
#         user = authenticate(request, username=username, password=password)
#         if user:
#             login(request, user)
#             return Response({'message': 'Logged in successfully.'})
#         return Response({'message': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)









class ForgotPasswordView(generics.GenericAPIView):
    serializer_class = ForgotPasswordSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get('email')
        user = User.objects.get(email=email)

        token = default_token_generator.make_token(user)
        reset_password_url = f'{settings.FRONTEND_URL}/reset-password/{user.pk}/{token}'

        message = f'Hello {user.username},\n\nYou can reset your password by clicking on the following link:\n\n{reset_password_url}'

        send_mail(
            'Password Reset',
            message,
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )

        return Response({'detail': 'Email sent'}, status=status.HTTP_200_OK)
