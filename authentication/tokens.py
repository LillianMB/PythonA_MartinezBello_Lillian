from django.contrib.auth.tokens import default_token_generator
from rest_framework.decorators import authentication_classes
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from six import text_type
class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            text_type(user.pk) + text_type(timestamp)
        )
    
generate_token = TokenGenerator()