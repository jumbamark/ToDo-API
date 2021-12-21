from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from authentication.serializers import RegisterSerializer, LoginSerializer
from rest_framework import response,status, permissions
from django.contrib.auth import authenticate


# Create your views here.
class RegisterAPIView(GenericAPIView):
    authentication_classes = []
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)

        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(GenericAPIView):
    authentication_classes = []

    serializer_class = LoginSerializer

    def post(self, request):
        email = request.data.get('email', None)
        password = request.data.get('password', None)

        user = authenticate(username=email, password=password)
        if user:
            serializer = self.serializer_class(user)
            return response.Response(serializer.data, status=status.HTTP_200_OK)
        return response.Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


class AuthUserAPIView(GenericAPIView):

    # user should be authenticated to access this view (should atleast have a token)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        user = request.user

        # now that we have the user,we serialize the data and send it back to the client as json
        serializer = RegisterSerializer(user)

        return response.Response({"user": serializer.data})
