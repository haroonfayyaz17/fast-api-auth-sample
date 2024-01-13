from fastapi import APIRouter, status, Response
from app.utils import omit
from app.database import engine
from sqlalchemy.orm import Session
from sqlalchemy import exc
from typing import List
from app.redis import redis_cache
import app.models as models
import app.schemas as schemas
from app.auth.auth_handler import signJWT

router = APIRouter(prefix="/auth")


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.User, response: Response):
    userDb = models.User(**user.dict())

    db = Session(bind=engine, expire_on_commit=False)
    try:
        db.add(userDb)
        db.commit()

        return {'success': True, 'message': "User created successfully", 'data': omit(userDb.__dict__, ['password'])}
    except exc.IntegrityError as e:
        db.rollback()
        err_msg = str(e).split(':')[1].split("\n")[0].strip().split(".").pop()
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        return {'success': False, 'message': f'{err_msg} should be unique'}
    finally:
        db.close()


@router.post("/login", status_code=status.HTTP_200_OK)
def login(user: schemas.UserLogin, response: Response):
    res = models.User.authenticate(**user.dict())

    if type(res) == str:
        response.status_code = status.HTTP_403_FORBIDDEN
        return {'success': False, 'message': res}

    user = {'user_id': res.id, 'email': res.email}

    jwt_response = signJWT(user)
    token = jwt_response['access_token']

    redis_cache.hset(f'user:{res.id}', mapping={**user, 'token': token})

    return jwt_response
