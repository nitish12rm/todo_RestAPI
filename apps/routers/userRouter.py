
from fastapi import Depends,APIRouter
from sqlalchemy.orm import Session
from ..dataBase import DataBase
from ..schemas import users
from ..models import model

router = APIRouter( 
    prefix="/user",
    tags=['User']
    )



@router.get('/',response_model=list[users.UserOut])
def getUser(db: Session = Depends(DataBase.get_db)):
    users = db.query(model.User).all()
    return users