from fastapi import APIRouter
from fastapi.responses import JSONResponse
from api.logic.db_tools import UserInteractions
from api.schemas import ValidUser

ui = UserInteractions()
router = APIRouter(
    prefix="/user_interactions",
    tags=["users"],
)


@router.post('/user_reg')
def registrate_user(user: ValidUser):
    print(user)
    if ui.createUser({'user': user}):
        return JSONResponse(content={"message": "Success!"}, status_code=200)
    return JSONResponse(content={"message": "Something broken!"}, status_code=500)


@router.post('/user_updt')
def update_user(user_id, new_fields):
    if ui.updateUser({user_id, new_fields}):
        return JSONResponse(content={"message": "Success!"}, status_code=200)
    return JSONResponse(content={"message": "Something broken!"}, status_code=500)


@router.post('/user_del')
def delete_user(user_id):
    if ui.deleteUser(user_id):
        return JSONResponse(content={"message": "Success!"}, status_code=200)
    return JSONResponse(content={"message": "Something broken!"}, status_code=500)
