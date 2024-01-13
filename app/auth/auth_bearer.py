from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.redis import redis_cache

from app.auth.auth_handler import decodeJWT


class JWTBearer(HTTPBearer):
    """
    Custom class for handling JWT (JSON Web Token) authentication in FastAPI.

    Args:
        auto_error (bool): Whether to automatically raise an HTTPException on authentication error. Defaults to True.

    Methods:
        __init__(self, auto_error: bool = True):
            Initializes the JWTBearer instance.

        __call__(self, request: Request) -> str:
            Validates the JWT token in the request and returns the token if valid.

        verify_jwt(self, jwtoken: str) -> bool:
            Verifies the authenticity and validity of the provided JWT token.

    Usage:
        Use this class as a dependency in your FastAPI route to enforce JWT authentication.

    Example:
        ```python
        from fastapi import FastAPI, Depends

        app = FastAPI()

        jwt_bearer = JWTBearer()

        @app.get("/secure-data")
        async def secure_data(token: str = Depends(jwt_bearer)):
            return {"message": "This is secure data!"}
        ```
    """

    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=403, detail="Invalid authentication scheme.")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(
                    status_code=403, detail="Invalid token or expired token.")
            return credentials.credentials
        else:
            raise HTTPException(
                status_code=403, detail="Invalid authorization code.")

    def verify_jwt(self, jwtoken: str) -> bool:
        isTokenValid: bool = False

        try:
            payload = decodeJWT(jwtoken)
            if not payload:
                return isTokenValid

            user_data = redis_cache.hgetall(f'user:{payload["user_id"]}')
            if not user_data:
                return isTokenValid

            if user_data['token'] != jwtoken:
                return isTokenValid

        except Exception as e:
            payload = None
        if payload:
            isTokenValid = True

        return isTokenValid
