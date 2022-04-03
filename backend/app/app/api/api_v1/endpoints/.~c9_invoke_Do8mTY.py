from re import M
from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from fastapi.encoders import jsonable_encoder
from app.api import deps
from datetime import date


router = APIRouter()

@router.get('/multi', response_model= List[schemas.Question])
def read_some_questions(
    db:Session= Depends(deps.get_db),
    skip: int=0,
    limit: int= 100,
    # current_user: models.User= Depends(deps.get_current_active_user),

)-> Any:
    """
    Retrieve some CMs
    """
    mas= crud.cm.get_multi(db, skip, limit)
    return mas

@router.get('/', 
# response_model= List[schemas.Ma]
)
def read_cms(
    db:Session= Depends(deps.get_db),
    # current_user: models.User= Depends(deps.get_current_active_user),

)-> Any:
    """
    Retrieve all Mas
    """
    cms= crud.cm.get_with_admins(db)
    cms=list(map(jsonable_encoder,cms))
    #TODO: rewrite this with pydantic in a more structured manner
    for i in range(len(cms)):
        cms[i]['cms_admin']= list(map(lambda x : x['id'] ,cms[i]['cms_admin']))

    return cms
@router.get('/affected',
    response_model=List[schemas.CM]
    )
def read_related_cm(
    db:Session=Depends(deps.get_db),
    current_user: models.User= Depends(deps.get_current_active_user),
    ):
    """
    Get the CM that is affected to the current user
    
    """
    cms= crud.cm.get_related(db=db, id_user=current_user.id)
    return cms

@router.post("/", response_model=schemas.CM)
def create_cm( *,
    db: Session=Depends(deps.get_db),
    cm_receive : schemas.CMReceive,
    current_user: models.User= Depends(deps.get_current_active_user)
    )-> Any:
        """
        Create cm
        """
        cm_in = cm_receive.cm
        user_admins=[]
        for admin in cm_receive.cms_admin:
            user_admin= crud.user.get(db=db, id=int(admin))
            user_admins.append(user_admin)
        # user_admins.append(current_user)
        question= crud.cm.create_with_admins(db=db, obj_in=cm_in, admins=user_admins)
        return question


 
@router.put("/{id}", response_model=schemas.CM)
def update_cm(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    cm_in: schemas.CMUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an item.
    #TODO test with changing users admins 
    """
    cm = crud.cm.get(db=db, id=id)
    if not cm:
        raise HTTPException(status_code=404, detail="Question not found")
    if id not in [k.id for k in cm.cms_admin]:
        raise HTTPException(status_code=404, detail="User not allowed to modified this CM")
    
    question = crud.cm.update(db=db, db_obj=cm, obj_in=cm_in)
    return question
@router.delete("/{id}", response_model=schemas.CM)
def deletee_cm(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an item.
    #TODO test with changing users admins 
    """
    cm = crud.cm.get(db=db, id=id)
    if not cm:
        raise HTTPException(status_code=404, detail="Country manager not found")
    if id not in [k.id for k in cm.cms_admin]:
        raise HTTPException(status_code=404, detail="User not allowed to delete this CM")
    
    question = crud.cm.update(db=db, db_obj=cm, obj_in=cm_in)
    return question
