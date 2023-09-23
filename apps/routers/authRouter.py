
from fastapi import Depends,APIRouter,HTTPException,status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..dataBase import DataBase
from ..schemas import tokenS,users
from ..models import model
from ..auth import oauth2

router = APIRouter( 
    prefix="/auth",
    tags=['Authenticaton']
    )

@router.post('/signup',response_model=users.UserOut)
def createUser(user: users.UserCreate, db: Session = Depends(DataBase.get_db)):
    newUser = model.User(**user.model_dump())
    db.add(newUser)
    db.commit()
    db.refresh(newUser)
    return newUser
@router.post('/signin',response_model=tokenS.token)
def login(user_cred: OAuth2PasswordRequestForm=Depends(),db: Session = Depends(DataBase.get_db)):
    user = db.query(model.User).filter(model.User.email == user_cred.username,model.User.password == user_cred.password ).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Invalid Credentials")
    #create token
    access_token = oauth2.create_access_token(data={'user_id':user.id})
    #return token
    return {'access_token':access_token,'token_type':'bearer'}
