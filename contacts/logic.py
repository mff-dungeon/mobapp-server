from django.contrib.auth.models import User

from server.exceptions import HttpException


class UserCreator(object):


    def create(self, email):
        if self.known(email):
            raise HttpException(412, "Email is already used.")

        user = User.objects.create_user(email, email)

    def known(self, email):
        return User.objects.filter(email=email).count() > 0

