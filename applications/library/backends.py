from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

UserModel = get_user_model()

class EmailOrUsernameModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # Sihir pencarian: Cari dimana Username = input ATAU Email = input
            user = UserModel.objects.get(
                Q(username__iexact=username) | Q(email__iexact=username)
            )
        except UserModel.DoesNotExist:
            # Kalau nggak ketemu username & emailnya, tolak!
            return None

        # Kalau ketemu, cek passwordnya bener atau nggak
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
            
        return None