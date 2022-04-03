from typing import Any
from app.schemas import Answer, Question
from app.schemas.answer import Lang
from app.schemas.question import QuestionType

from fastapi import APIRouter, Depends
from pydantic.networks import EmailStr

from app import models, schemas
from app.api import deps
from app.core.celery_app import celery_app
from app.utils import send_test_email
from datetime import datetime 

router = APIRouter()


@router.post("/test-celery/", response_model=schemas.Msg, status_code=201)
def test_celery(
    msg: schemas.Msg,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Test Celery worker.
    """
    celery_app.send_task("app.worker.test_celery", args=[msg.msg])
    return {"msg": "Word received"}


@router.post("/test-email/", response_model=schemas.Msg, status_code=201)
def test_email(
    email_to: EmailStr,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Test emails.
    """
    send_test_email(email_to=email_to)
    return {"msg": "Test email sent"}
def lang_adapt(  lang:Lang, datatype:QuestionType , model=Answer, )->Any :
    """
    THis function make a link between attribut of different object and language corresponding to
    that attribut
    """
    if model==Answer:
        if datatype==QuestionType.CHOICE:
            return f'value_choices_{str(lang.name).lower()}'
        elif datatype==QuestionType.DATE:
            return f'value_date'
        elif datatype==QuestionType.TABLE:
            return f'value_tab_{str(lang.name).lower()}'  
        elif datatype==QuestionType.PERCENTAGE:
            return f'value_percentage'
        elif datatype==QuestionType.LIST:
            return f'value_list_{str(lang.name).lower()}'    
        elif datatype==QuestionType.SUBQUESTION:
            return f'value_subquestion_{str(lang.name).lower()}'  
        elif datatype==QuestionType.STRING:
            return f'value_string_{str(lang.name).lower()}'  
        elif datatype==QuestionType.CHOICE:
            return f'value_choices_{str(lang.name).lower()}'
        elif datatype==QuestionType.INTEGER:
            return f'value_integer'
    else: 
        raise ValueError
def reformat_import( datatype:QuestionType, response ):
    if datatype==QuestionType.INTEGER:
        return int(response[0])
    elif datatype in [QuestionType.PERCENTAGE, QuestionType.FLOAT]:
        return float(response[0])
    elif datatype==QuestionType.DATE:
        return  datetime.strptime(response[0], "%d/%m/%Y")
    elif datatype in [QuestionType.STRING, QuestionType.TEXT,]:
        return response[0]
    elif datatype==QuestionType.TABLE:
        return [k.split('//') for k in response]
    else:
        return response
