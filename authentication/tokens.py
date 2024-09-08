from rest_framework_simplejwt.tokens import RefreshToken
from authentication.models import User


def create_jwt_pair(user: User):
    refresh = RefreshToken.for_user(user)
    return {
        "access": str(refresh.access_token),
        "refresh": str(refresh),
    }