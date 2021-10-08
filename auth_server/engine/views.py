""" API endpoint views """

# Module imports
from rest_framework.views import APIView
from rest_framework.response import Response

# Application imports
from engine.serializers import (
    UserLoginSerializer,
    RefreshTokenSerializer
)


class GenerateTokensView(APIView):
    """ API for token generation """

    # API setup
    permission_classes = ()
    authentication_classes = ()

    # Response variables
    response = None
    response_code = None

    def post(self, request):
        """ Method handling post request made to this API endpoint """

        # Login serializer initialization with the incoming data
        loginSerializer = UserLoginSerializer(data=request.data)

        # API logic
        if loginSerializer.is_valid():
            self.response = loginSerializer.data
            self.response_code = 200
        else:
            self.response = loginSerializer.errors
            self.response_code = 400

        # API response using response variables
        return Response(self.response, self.response_code)


class RefreshTokenView(APIView):
    """ API for access token refreshing """

    # API setup
    permission_classes = ()
    authentication_classes = ()

    # Response variables
    response = None
    response_code = None

    def post(self, request):
        """ Method handling post request made to this API endpoint """

        # Refresh serializer initialization with the incoming data
        refreshSerializer= RefreshTokenSerializer(data=request.data)

        # API logic
        if refreshSerializer.is_valid():
            self.response = refreshSerializer.data
            self.response_code = 200
        else:
            self.response = refreshSerializer.errors
            self.response_code = 400

        # API response using response variables
        return Response(self.response, self.response_code)



