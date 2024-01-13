from fastapi import APIRouter, status, Response, Depends, Request
import app.schemas as schemas
from app.auth.auth_bearer import JWTBearer
from app.auth.auth_handler import decodeJWT
from app.utils import omit

router = APIRouter(prefix="/user", dependencies=[Depends(JWTBearer())])


@router.post("/", status_code=status.HTTP_200_OK)
async def add_user(user: dict, request: Request) -> dict:
    token = request.headers["authorization"].split(" ")[1]
    user = decodeJWT(token)

    return omit(user, ['expires'])