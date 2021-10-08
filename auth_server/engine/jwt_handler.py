""" Internal module for ease of managing JWT tokens """

# Native imports
import datetime
import base64
import json
import jwt

# Module imports
from rest_framework import serializers

# Application imports
from engine.models import User


class JWTHandler():

    token = None
    user = None

    secret = None
    secret2 = None
    payload = None

    def __init__(self, params):
        """ Bootstrapping parameters """
        try:
            user = params['user']
            if user:
                self.user = user
                self.__strap_user_secret()
                self.access = None
                self.refresh = None
        except KeyError:
            pass
        try:
            token = params['token']
            if token:
                self.token = token
                self.__strap_token_payload()
                self.__strap_user_from_token()
        except KeyError as e:
            pass

    def __strap_token_payload(self):
        """ load the payload from token into state """
        try:
            jwt_payload = self.token.split('.')[1]
            self.payload = json.loads(base64.b64decode(
                jwt_payload + '=' * (-len(jwt_payload) % 4)).decode('ascii'))

        except Exception as exc:
            raise serializers.ValidationError(
                "Token parsing failed to parse payload") from exc

    def __strap_user_secret(self):
        """ Straps the user secret from user object stored in state """
        try:
            self.secret = self.user.retrieve_secret()
            self.secret2 = self.user.retrieve_secret2()
        except Exception as exc:
            raise serializers.ValidationError(
                "Error parsing user secret") from exc

    def __strap_user_from_token(self):
        """ straps the user object to state """
        try:
            self.user = User.objects.get(id=self.payload['uid'])
            self.__strap_user_secret()
        except Exception as exc:
            raise serializers.ValidationError(
                "Error loading user from token") from exc

    def validate_access_token(self):
        """ Method for validating access token """
        try:
            if jwt.encode(self.payload, self.secret, algorithm='HS256') == self.token:
                return True
            else:
                return None
        except Exception as exc:
            raise serializers.ValidationError(
                "Error validating token") from exc

    def __validate_refresh_token(self):
        """ Method for validating refresh token """
        try:
            if jwt.encode(self.payload, self.secret2, algorithm='HS256') == self.token:
                return True
            else:
                return None
        except Exception as exc:
            raise serializers.ValidationError(
                "Error validating token") from exc

    def refresh_tokens(self):
        """ Refreshing access tokens using the refresh token """
        try:
            if self.__validate_refresh_token():
                # Refresh user's access secret
                self.user.generate_new_secret()
                self.user.save()

                # Encode new access token with new access secret
                self.__strap_user_secret()
                self.access = jwt.encode(
                    {
                        "email": self.user.email,
                        "uid": self.user.id,
                        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
                    },
                    self.secret,
                    algorithm='HS256'
                )
            else:
                self.access = None

        except Exception as exc:
            print(exc)
            raise serializers.ValidationError("Error in refreshing tokens") from exc

        return {
            "access": self.access
        }

    def get_tokens(self):
        """ Returns a new set of JWT token encoded with users private secret """
        try:
            if self.secret is not None and self.user is not None:

                # Generate new access token
                self.access = jwt.encode(
                    {
                        "email": self.user.email,
                        "uid": self.user.id,
                        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
                    },
                    self.secret,
                    algorithm='HS256'
                )

                # Generate new refresh token
                self.refresh = jwt.encode(
                    {
                        "email": self.user.email,
                        "uid": self.user.id,
                        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
                    },
                    self.secret2,
                    algorithm='HS256'
                )

        except Exception as exc:
            raise serializers.ValidationError(
                "Unable to generate new tokens") from exc

        # Only returns absolute token value only if it is generated successfully
        return {
            "access": self.access,
            "refresh": self.refresh
        }
