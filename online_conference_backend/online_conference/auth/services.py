from flask import current_app, g
import psycopg2
from online_conference.db import get_db_conn
from utils import auth_utils

def register_user(email, password, name):
    # Check if the user already exists
    with get_db_conn() as conn:
        with conn.cursor() as cursor:
            cursor.execute('SELECT id FROM users WHERE email = %s', (email,))
            if cursor.fetchone():
                return {'error': 'User with this email already exists'}, 409

    # Insert the new user into the database
    hashed_password = auth_utils.hash_password(password)
    with get_db_conn() as conn:
        with conn.cursor() as cursor:
            cursor.execute('INSERT INTO users (email, password, name) VALUES (%s, %s, %s)', (email, hashed_password, name))
            conn.commit()

    return {'message': 'User registered successfully'}, 201

def google_register_user(google_oauth2_code):
    # Exchange the Google OAuth2 code for an access token
    access_token_response = auth_utils.get_google_access_token(google_oauth2_code)

    if access_token_response is None or 'access_token' not in access_token_response:
        return {'error': 'Google login failed'}, 401

    google_access_token = access_token_response['access_token']

    # Use the Google access token to fetch user information
    user_info = auth_utils.get_google_user_info(google_access_token)

    if user_info is None or 'email' not in user_info or 'name' not in user_info:
        return {'error': 'Failed to get user info from Google'}, 401

    email = user_info['email']
    name = user_info['name']

    # Check if the user exists in the database
    user = get_user_by_email(email)

    if not user:
        # User does not exist, register the user using Google login method
        with get_db_conn() as conn:
            with conn.cursor() as cursor:
                cursor.execute('INSERT INTO users (email, name, login_methods) VALUES (%s, %s, %s)', (email, name, 'google'))
                conn.commit()

    return {'message': 'User registered successfully'}, 201


def login_user(email, password):
    # Check if the user exists and the password is correct
    user = get_user_by_email(email)
    if user and auth_utils.check_password(password, user['password']):
        # User authenticated successfully, generate and return the access token
        access_token = generate_access_token(user['id'])
        return {'access_token': access_token}, 200

    return {'error': 'Invalid credentials'}, 401

def google_login_user(google_oauth2_code):
    # Exchange the Google OAuth2 code for an access token
    access_token_response = auth_utils.get_google_access_token(google_oauth2_code)

    if access_token_response is None or 'access_token' not in access_token_response:
        return {'error': 'Google login failed'}, 401

    google_access_token = access_token_response['access_token']

    # Use the Google access token to fetch user information
    user_info = auth_utils.get_google_user_info(google_access_token)

    if user_info is None or 'email' not in user_info or 'name' not in user_info:
        return {'error': 'Failed to get user info from Google'}, 401

    email = user_info['email']
    name = user_info['name']

    # Check if the user exists in the database
    user = get_user_by_email(email)

    if not user:
        return {'error': f'{email} doesn\'t exist'}, 401
    else:
        access_token = generate_access_token(user['id'])
        return {'access_token': access_token}, 200