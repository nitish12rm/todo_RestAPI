from fastapi import FastAPI
from .dataBase.DataBase import engine
from fastapi.middleware.cors import CORSMiddleware
from .routers import authRouter,todoRouter,userRouter
from .models import model
app = FastAPI()


#this is used to create the models defined in python to the database when we r not using alembic
#alembic can create database by using alembic revision --autogenerate
model.Base.metadata.create_all(bind=engine)

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get('/')
def root():
    msg = 'Welcome to the ToDo api made with <3 by nitish'
    return msg

app.include_router(authRouter.router)
app.include_router(userRouter.router)
app.include_router(todoRouter.router)


