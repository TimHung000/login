from fastapi import APIRouter
from starlette import status


router = APIRouter()

@router.post('/', status_code=status.HTTP_200_OK)
def home():
    return 'home'
