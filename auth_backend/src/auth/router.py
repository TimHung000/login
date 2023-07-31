from fastapi import APIRouter, Response, Cookie, Body, Request
from src.auth.service import register_user, google_register_user, login_user, google_login_user, renew_token
from starlette import status
from src.auth.schemas import RegisterUser, BasicResponse, AccessTokenResponse, AuthUser
from typing import Optional, Dict, Any


router = APIRouter()

@router.post('/register', status_code=status.HTTP_201_CREATED, response_model=BasicResponse)
async def register(user_data: RegisterUser):
    return await register_user(user_data)

@router.post('/google-register', status_code=status.HTTP_201_CREATED, response_model=BasicResponse)
async def google_register(request: Request):
    payload = await request.json()
    return await google_register_user(payload['google_oauth2_code'])

@router.post('/login', status_code=status.HTTP_200_OK, response_model=AccessTokenResponse)
async def login(user_data: AuthUser, response: Response):
    return await login_user(user_data, response)

@router.post('/google-login', status_code=status.HTTP_200_OK, response_model=AccessTokenResponse)
async def google_login(request: Request, response: Response):
    payload = await request.json()
    return await google_login_user(payload['google_oauth2_code'], response)

@router.put("/refresh-token", status_code=status.HTTP_200_OK, response_model=AccessTokenResponse)
async def refresh_token(
    response: Response,
    refresh_token: Optional[str] = Cookie(None)
):
    return await renew_token(response, refresh_token)

@router.delete("/refresh-token", status_code=status.HTTP_200_OK, response_model=AccessTokenResponse)
async def refresh_token(
    response: Response,
    refresh_token: Optional[str] = Cookie(None)
):
    return await delete_token(refresh_token, response)