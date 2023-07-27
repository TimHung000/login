from flask import current_app, g
import bcrypt

def get_google_access_token(google_oauth2_code):
    # Exchange the Google OAuth2 code for an access token
    payload = {
        'code': google_oauth2_code,
        'client_id': current_app.config['GOOGLE_CLIENT_ID'],
        'client_secret': current_app.config['GOOGLE_CLIENT_ID'],
        'redirect_uri': 'postmessage',
        'grant_type': 'authorization_code',
    }
    # headers = {'Content-type': 'application/x-www-form-urlencoded'}

    response = requests.post(current_app.config['GOOGLE_OAUTH2_TOKEN_URL'], data=payload)
    if response.status_code == 200:
        return response.json()
    return None

def get_google_user_info(google_access_token):
    # Fetch user information from Google using the access token
    headers = {'Authorization': f'Bearer {google_access_token}'}
    response = requests.get(current_app.config['GOOGLE_OAUTH2_USERINFO_URL'], headers=headers)
    if response.status_code == 200:
        return response.json()
    return None

def hash_password(password):
    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')

def check_password(password, hashed_password):
    # Check if the provided password matches the hashed password
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
