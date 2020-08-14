from rest_framework import serializers
from health_bot.models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('user_email', 'user_pw')