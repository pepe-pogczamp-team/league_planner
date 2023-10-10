from typing import Any

from django.contrib.auth.models import User
from rest_framework import mixins, permissions, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.request import Request
from rest_framework.response import Response

from league_planner.serializers.user import CreateUserSerializer


class CreateUserView(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = CreateUserSerializer


class LoginView(ObtainAuthToken):
    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        serializer = self.serializer_class(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data.get("user")
        token, created = Token.objects.get_or_create(user=user)
        return Response({"id": user.pk, "token": token.key})
