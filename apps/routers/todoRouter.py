
from fastapi import Depends,Response,status,HTTPException,APIRouter
from apps.models.model import todo 
from sqlalchemy.orm import Session
from ..dataBase import DataBase
from ..auth import oauth2
from ..models import model
from ..schemas import todo

router = APIRouter( 
    prefix="/todo",
    tags=['ToDo']
    )


@router.post('/',response_model=todo.todoOut)
def createTodo(todo: todo.todoCreate,db: Session = Depends(DataBase.get_db), currentUser = Depends(oauth2.get_current_user)):
    # print(currentUser.email)
    created_post = model.todo(owner_id = currentUser.id,**todo.model_dump())
    db.add(created_post)
    db.commit()
    db.refresh(created_post)
    return created_post


@router.get('/all',response_model=list[todo.todoOut])
def getTodo(db: Session = Depends(DataBase.get_db)):
    try:
       tasks = db.query(model.todo).all()
    except HTTPException:
        raise HTTPException
    return tasks


@router.delete('/{id}')
def delTodo(id:int, db: Session = Depends(DataBase.get_db),current_user = Depends(oauth2.get_current_user)):
    deleteTodoQuery = db.query(model.todo).filter(model.todo.id == id )
    deleteTodo = deleteTodoQuery.first()
    if deleteTodo == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} was not found!")
    if deleteTodo.owner_id != current_user.id:
         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorised to perform such action")
    deleteTodoQuery.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get('/single',response_model=list[todo.todoOut])
def getSingleTodo(db: Session = Depends(DataBase.get_db),current_user = Depends(oauth2.get_current_user)):
    userTodoQuery = db.query(model.todo).filter(model.todo.owner_id == current_user.id)
    userTodo = userTodoQuery.all()
    return userTodo



