from jose import JWTError,jwt
from datetime import datetime,timedelta
from ..schemas import tokenS, users
from ..dataBase import DataBase
from ..models import model
from fastapi import Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from ..config import config

SECRET_KEY = config.settings.SECRET_KEY
ALGORITHM = config.settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = config.settings.ACCESS_TOKEN_EXPIRE_MINUTES

oauth  = OAuth2PasswordBearer(tokenUrl='auth/signin')

#create access token
def create_access_token(data:dict):
    to_encode = data.copy()
    expire = datetime.utcnow()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp':expire})
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(token:str,credentials_exception):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=ALGORITHM)
        id:str = payload.get("user_id")
        if id is None:
            raise credentials_exception
        token_data = tokenS.TokenData(id=id)
        return token_data
    except JWTError:
        raise credentials_exception
    
def get_current_user(token:str = Depends(oauth),db:Session = Depends(DataBase.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=f"could not validate credentials",
                                          headers={'WWW-Authenticate':'Bearer'})
    token_data = verify_access_token(token,credentials_exception)
    userData = db.query(model.User).filter(model.User.id == token_data.id).first()
    return userData
    


