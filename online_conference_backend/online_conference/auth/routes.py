import bp
from services import register_user, google_register_user, login_user, google_login_user

@bp.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    # Call the login_user service to handle user login
    response, status_code = login_user(email, password)
    return jsonify(response), status_code

@bp.route('/google-login', methods=['POST'])
def google_login():
    data = request.json
    google_oauth2_code = data.get('google_oauth2_code')

    # Call the google_login_user service to handle Google OAuth2 login
    response, status_code = google_login_user(google_oauth2_code)
    return jsonify(response), status_code

@bp.route('/register', methods=['POST'])
def register():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    confirmed_password = data.get('confirmed_password')
    name = data.get('name')

    # Input validation
    if not email or not password or not confirmed_password or not name:
        return jsonify({'error': 'All fields are required'}), 400
    if password != confirmed_password:
        return jsonify({'error': 'Passwords do not match'}), 400

    # Call the register_user service to handle user registration
    response, status_code = register_user(email, password, name)
    return jsonify(response), status_code

@bp.route('/google-register', methods=['POST'])
def google_register():
    data = request.json
    google_oauth2_code = data.get('google_oauth2_code')

    # Call the google_login_user service to handle Google OAuth2 login
    response, status_code = google_register_user(google_oauth2_code)
    return jsonify(response), status_code