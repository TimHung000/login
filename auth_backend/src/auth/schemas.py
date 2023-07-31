import re

from pydantic import EmailStr, Field, BaseModel

STRONG_PASSWORD_PATTERN = re.compile(r"^(?=.*[\d])(?=.*[!@#$%^&*])[\w!@#$%^&*]{6,128}$")


class RegisterUser(BaseModel):
    name: str
    email: EmailStr
    password: str
    confirmed_password: str

    # @validator("password")
    # def valid_password(cls, password: str) -> str:
    #     if not re.match(STRONG_PASSWORD_PATTERN, password):
    #         raise ValueError(
    #             "Password must contain at least "
    #             "one lower character, "
    #             "one upper character, "
    #             "digit or "
    #             "special symbol"
    #         )
    #     return password

class AuthUser(BaseModel):
    username: EmailStr
    password: str = Field(min_length=1, max_length=128)



class AccessTokenResponse(BaseModel):
    access_token: str
    token_type: str


class BasicResponse(BaseModel):
    message: str