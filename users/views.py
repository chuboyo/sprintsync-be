from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import action
from rest_framework.exceptions import (
    AuthenticationFailed,
    NotAuthenticated,
)
from .serializers import UserLoginSerializer, UserSerializer
from .permissions import UserPermission
from django.contrib.auth import get_user_model


# Create your views here.

class UserViewset(viewsets.ModelViewSet):

    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()
    permission_classes = (UserPermission,)

    def get_serializer_class(self):
        if self.action == "login":
            return UserLoginSerializer
        return UserSerializer

    def perform_authentication(self, request):
        if self.action in [
            "login",
            "create",
        ]:
            return True

        return super().perform_authentication(request)

    @action(detail=False, methods=["post"])
    def login(self, request):
        serializer = self.get_serializer_class()(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data
            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            })
        except AuthenticationFailed as e:
            return Response({"message": str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        except NotAuthenticated as e:
            return Response({"message": str(e)}, status=status.HTTP_403_FORBIDDEN)

