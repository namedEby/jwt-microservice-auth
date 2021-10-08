# jwt-microservice-auth

Microservice authorization using multiple JWT tokens (wallmart oauth2)

## Authentication server

#### Login route

```url
https://localhost:port/tokens/login/
```

This is the only route exposed to the client from the authentication server.
Provides a rest api when a post request is made with suffiecient user credentials will return a set of access tokens.
The initial set of tokens will be for the authentication server itself which will allow refreshing and generation of newer jwt tokens.

```json
{
	"auth":{
		"access": //jwt access token for the authentication server,
		"refresh": //jwt token for refreshing the access token
	},
	["service_name":{
		"access": //jwt access token for the service_name
		"refresh": //jwt refresh token for the service_name
	}]
}
```

The login credentials, in POST body

```json
{
	"email": //user email,
	"password": //user password
}
```

### Flow of authentication/authorization process

When the login route experience a request, the body is parsed and authenticated given the credentials are valid.
After authentication the server then generate and retrieve the user's private secret token.
Using this newly generated token since authentication, is used to encode a JWT token with payload contatinging the user details.
