from src.db import database
from src.auth.schemas import RegisterUser, AccessTokenResponse, AuthUser
from src.auth.exceptions import AllFieldRequired, PasswordConfirm, EmailTaken, RefreshTokenRequired, InvalidToken, AuthorizationFailed, GoogleAuthorizationFailed
from src.config import get_settings
from src.auth.utils import hash_password, check_password, get_google_access_token, get_google_user_info, create_tokens
from datetime import datetime, timedelta
import jwt
from fastapi import Cookie, Response



async def register_user(user_data: RegisterUser):
    # Input validation
    if not user_data.email or not user_data.password or not user_data.confirmed_password or not user_data.name:
        raise AllFieldRequired()
    if user_data.password != user_data.confirmed_password:
        raise PasswordConfirm()

    # Check if the user already exists
    async with database.db_conn_pool.acquire()  as conn:
        async with conn.transaction():
            existing_user = await conn.fetchrow('SELECT id FROM users WHERE email = $1;', user_data.email)
            if existing_user:
                raise EmailTaken()
            print(existing_user)
            # Insert the new user into the database
            hashed_password = hash_password(user_data.password)
            await conn.execute('INSERT INTO users (email, password, name, login_method) VALUES ($1, $2, $3, $4);', user_data.email, hashed_password, user_data.name, 'default')


    return {'message': 'User registered successfully'}

async def google_register_user(google_oauth2_code: str):
    settings = get_settings()

    # get Google access token
    access_token_response = await get_google_access_token(google_oauth2_code, settings.GOOGLE_OAUTH2_REDIRECT_REGISTER)
    if access_token_response is None or 'access_token' not in access_token_response:
        raise GoogleAuthorizationFailed()


    # Use the Google access token to fetch user information
    google_access_token = access_token_response['access_token']
    user_info = await get_google_user_info(google_access_token)
    if user_info is None or 'email' not in user_info or 'name' not in user_info:
        raise GoogleAuthorizationFailed()


    # Check if the user exists in the database
    email = user_info['email']
    name = user_info['name']
    async with database.db_conn_pool.acquire() as conn:
        user = await conn.fetchrow('SELECT id FROM users WHERE email = $1;', email)

        if user:
            raise EMAIL_TAKEN()

        await conn.execute('INSERT INTO users (email, name, password, login_method) VALUES ($1, $2, $3, $4);', email, name, 'google', 'google')
    
    return {'message': 'User registered successfully'}

async def login_user(user_data: AuthUser, response: Response):
    settings = get_settings()
    # Check if the user exists and the password is correct
    async with database.db_conn_pool.acquire() as conn:
        user = await conn.fetchrow('SELECT * FROM users WHERE email = $1;', user_data.username)

    if not user or not check_password(user_data.password, user['password']):
        raise AuthorizationFailed()

    current_time = datetime.utcnow()
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES) + current_time
    access_token = create_tokens({
        "id": user['id'],
        "email": user['email'],
        }, 
        access_token_expires
    )

    refresh_token_expires = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS) + current_time
    refresh_token = create_tokens({
        "id": user['id'],
        "email": user['email'],
        }, 
        refresh_token_expires
    )
    async with database.db_conn_pool.acquire() as conn:

        await conn.execute(
            'INSERT INTO refresh_tokens (token, user_id, created_at, expires_at) VALUES ($1, $2, $3, $4);',
            refresh_token, user['id'], current_time, refresh_token_expires
        )

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        expires=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60 * 1000
    )

    return AccessTokenResponse(
        access_token=access_token,
        token_type="bearer"
    )

async def google_login_user(google_oauth2_code: str, response: Response):
    settings = get_settings()

    # get Google access token
    google_response = await get_google_access_token(google_oauth2_code, settings.GOOGLE_OAUTH2_REDIRECT_LOGIN)
    if google_response is None or 'access_token' not in google_response:
        raise GoogleAuthorizationFailed()

    # Use the Google access token to fetch user information
    google_access_token = google_response['access_token']
    user_info = await get_google_user_info(google_access_token)
    if user_info is None or 'email' not in user_info or 'name' not in user_info:
        raise GoogleAuthorizationFailed()

    # Check if the user exists in the database
    email = user_info['email']
    name = user_info['name']
    async with database.db_conn_pool.acquire() as conn:
        user = await conn.fetchrow('SELECT * FROM users WHERE email = $1;', email)

    if not user:
        raise AuthorizationFailed()

    current_time = datetime.utcnow()
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES) + current_time
    access_token = create_tokens({
        "id": user['id'],
        "email": user['email'],
        }, 
        access_token_expires
    )

    refresh_token_expires = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS) + current_time
    refresh_token = create_tokens({
        "id": user['id'],
        "email": user['email'],
        }, 
        refresh_token_expires
    )

    # Store the refresh token in the database
    async with database.db_conn_pool.acquire() as conn:
        await conn.execute(
            'INSERT INTO refresh_tokens (token, user_id, created_at, expires_at) VALUES ($1, $2, $3, $4);', refresh_token, user['id'], current_time, refresh_token_expires
        )

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        expires=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60 * 1000
    )

    print(access_token)
    return AccessTokenResponse(
        access_token=access_token,
        token_type="bearer"
    )

async def renew_token(response: Response, refresh_token):
    settings = get_settings()
    if not refresh_token:
        raise RefreshTokenRequired()

    async with database.db_conn_pool.acquire() as conn:
        token = await conn.fetchrow(
            """
            SELECT 
                rt.id, 
                rt.token,
                rt.user_id, 
                rt.created_at, 
                rt.expires_at, 
                u.id, 
                u.email 
            FROM 
                refresh_tokens rt
            INNER JOIN users u
                ON rt.user_id = u.id
            WHERE
                rt.token = $1;
            """,
            refresh_token
        )
    if not token:
        raise InvalidToken

    user_id = token['id']
    user_mail = token['email']

    current_time = datetime.utcnow()
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES) + current_time
    new_access_token = create_tokens({
        "id": user_id,
        "email": user_mail,
        }, 
        access_token_expires
    )

    refresh_token_expires = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS) + current_time
    new_refresh_token = create_tokens({
        "id": user_id,
        "email": user_mail,
        }, 
        refresh_token_expires
    )

    response.set_cookie(
        key="refresh_token",
        value=new_refresh_token,
        httponly=True,
        expires=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60 * 1000
    )
    async with database.db_conn_pool.acquire() as conn:
        await conn.execute(
            'INSERT INTO refresh_tokens (token, user_id, created_at, expires_at) VALUES ($1, $2, $3, $4);', new_refresh_token, user_id, current_time, refresh_token_expires
        )
    async with database.db_conn_pool.acquire() as conn:
        await conn.execute(
            'DELETE FROM refresh_tokens WHERE token = $1;',
            refresh_token
        )

    return AccessTokenResponse(
        access_token=new_access_token,
        token_type="bearer"
    )

async def delete_token(response: Response, refresh_token: Cookie()):
    async with database.db_conn_pool.acquire() as conn:
        await conn.execute(
            'DELETE FROM refresh_tokens WHERE token = $1;',
            refresh_token
        )
    response.delet_cookie("refresh_token")


