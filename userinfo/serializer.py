__author__ = 'jyoti'

from rest_framework import serializers
from userinfo.models import UserData
from django.contrib.auth.models import User


# This is the serializer which will serialize and deserialize data.
class UserSerializer(serializers.ModelSerializer):
    """
    A serializer for ``User``.
    """
    class Meta(object):
        model = User
        fields = ('username', 'first_name', 'last_name')


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = UserData
        fields = ('id', 'user', 'address', 'phone', 'company', 'comment')

