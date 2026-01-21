from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session
from database.setup_postgres import get_db
from fastapi import APIRouter, UploadFile, File
from service.create_contract_service import upload_file
from request.create_contract_request import create_contract_request, load_history_contract_request
from service.create_contract_service import create_contract, load_template_name, delete_template_service, download, load_history, load_session_service, delete_session_service


router = APIRouter()

@router.post("/create-contract")
async def create_contract_controller(request_data: create_contract_request,
                                     db: Session = Depends(get_db)):

    return await create_contract(create_contract_request=request_data, db=db)


@router.post("/upload-contract")
async def upload_contract(file: UploadFile = File(...), 
                          db: Session = Depends(get_db)):
    return await upload_file(file, db)

@router.get("/load-template")
async def load_template(db: Session = Depends(get_db)):

    return await load_template_name(db)

@router.delete("/delete-template/{id}")
async def delete_template(id:str, 
                          db: Session = Depends(get_db)):

    return await delete_template_service(db, id)


@router.get("/download/{id}")
def dowload_file(id:str):

    return download(id)



@router.post("/load_history")
async def load_history_end_point(request:load_history_contract_request, 
                           db: Session = Depends(get_db)):
    
    return await load_history(request, db)


@router.get("/session")
async def load_session(db: Session = Depends(get_db)):
    return await load_session_service(db)


@router.delete("/session/{id}")
async def load_session(id:int, db: Session = Depends(get_db)):
    
    return await delete_session_service(id, db)