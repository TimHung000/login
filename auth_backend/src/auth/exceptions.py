from src.exceptions import BadRequest, NotAuthenticated, PermissionDenied, Conflict

class ErrorCode:
    AUTHENTICATION_REQUIRED = "Authentication required."
    AUTHORIZATION_FAILED = "Authorization failed. User has no access."
    GOOGLE_AUTHORIZATION_FAILED = "Failed to get user info from Google"
    INVALID_TOKEN = "Invalid token."
    INVALID_CREDENTIALS = "Invalid credentials."
    EMAIL_TAKEN = "Email is already taken."
    ALL_FIELD_REQUIRED = "All field required"
    PASSWORD_CONFIRM = "Passwords do not match'"
    REFRESH_TOKEN_NOT_VALID = "Refresh token is not valid."
    REFRESH_TOKEN_REQUIRED = "Refresh token is required either in the body or cookie."
    


class AuthRequired(NotAuthenticated):
    DETAIL = ErrorCode.AUTHENTICATION_REQUIRED

class AuthorizationFailed(PermissionDenied):
    DETAIL = ErrorCode.AUTHORIZATION_FAILED

class GoogleAuthorizationFailed(PermissionDenied):
    DETAIL = ErrorCode.GOOGLE_AUTHORIZATION_FAILED
    
class InvalidToken(NotAuthenticated):
    DETAIL = ErrorCode.INVALID_TOKEN

class InvalidCredentials(NotAuthenticated):
    DETAIL = ErrorCode.INVALID_CREDENTIALS

class EmailTaken(Conflict):
    DETAIL = ErrorCode.EMAIL_TAKEN

class AllFieldRequired(BadRequest):
    DETAIL = ErrorCode.ALL_FIELD_REQUIRED

class PasswordConfirm(BadRequest):
    DETAIL = ErrorCode.PASSWORD_CONFIRM

class RefreshTokenRequired(NotAuthenticated):
    DETAIL = ErrorCode.REFRESH_TOKEN_REQUIRED