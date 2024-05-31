# estatemaster/mixins.py
from rest_framework import serializers
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed

class UserFromTokenMixin:
    def validate(self, data):
        print('ggg')
        request = self.context.get('request')
        if not request:
            raise serializers.ValidationError("Request context is required")

        token_auth = TokenAuthentication()
        try:
            user, auth_token = token_auth.authenticate(request)

        except AuthenticationFailed as e:
            raise serializers.ValidationError(str(e))

        data['user'] = user
        return data
