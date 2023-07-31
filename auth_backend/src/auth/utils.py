import bcrypt
from datetime import datetime, timedelta
import jwt
from src.config import get_settings
import aiohttp

async def get_google_access_token(google_oauth2_code: str, redirect_uri: str):
    settings = get_settings()

    # Exchange the Google OAuth2 code for an access token using aiohttp
    payload = {
        'code': google_oauth2_code,
        'client_id': settings.GOOGLE_CLIENT_ID,
        'client_secret': settings.GOOGLE_CLIENT_SECRET,
        'redirect_uri' : redirect_uri,
        'grant_type': 'authorization_code',
    }
    headers = {'Content-type': 'application/x-www-form-urlencoded'}

    async with aiohttp.ClientSession() as session:
        async with session.post(settings.GOOGLE_OAUTH2_TOKEN_URL, data=payload, headers=headers) as response:
            print(response)
            if response.status == 200:
                return await response.json()
            return None

async def get_google_user_info(google_access_token: str):
    settings = get_settings()
    headers = {'Authorization': f'Bearer {google_access_token}'}

    async with aiohttp.ClientSession() as session:
        async with session.get(settings.GOOGLE_OAUTH2_USERINFO_URL, headers=headers) as response:
            print(response)
            if response.status == 200:
                return await response.json()
            return None

def hash_password(password):
    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')

def check_password(password, hashed_password):
    # Check if the provided password matches the hashed password
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

def create_tokens(data: dict, expire: datetime):
    settings = get_settings()
    encoded_jwt = jwt.encode({"exp": expire, **data}, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt