from django.db.models import Q
from django.contrib.auth import get_user_model
from accounts.constants import *

User = get_user_model()


def authenticate(username=None, password=None):
    try:
        user = User.objects.get(Q(username=username)|Q(email=username),Q(state=ACTIVE)|Q(state=INACTIVE))
    except User.DoesNotExist:
        return None
    if user.check_password(password):
        return user


