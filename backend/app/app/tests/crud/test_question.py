from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app import crud
from app.core.security import verify_password
from app.models.question import QuestionType
from app.schemas.question import QuestionCreate, QuestionUpdate, Level, QuestionChoiceCreate
from app.tests.utils.utils import random_email, random_lower_string


def test_create_question(db: Session) -> None:
    
    question_in_tab = QuestionCreate(
            level=  Level.country.name,
            label_eng= 'the question ?' ,
            label_fr= 'Question test', 
            label_pt=  'questionna testo',
            datatype=  'CHOICE',
            # choices_eng= ['choice1', 'choice 2'],
            # choices_fr=  ['choice1', 'choice 2'],
            # choices_pt=  ['choice1', 'choice 2'],

            tabheader_eng= ['choice1', 'choice 2'],
            tabheader_fr=  ['choice1', 'choice 2'],
            tabheader_pt=  ['choice1', 'choice 2'],
            multichoices=False,
            choicecreation=False,
            mandatory=False,
            is_active=True,
            user_lastmodifier=1
            )
    question = crud.question.create(db, obj_in= question_in_tab)
    assert question.label_fr == "Question test" 
    question_in_subquestion=QuestionCreate(
            level=  Level.country.name,
            label_eng= 'the question ?' ,
            label_fr= 'Question test', 
            label_pt=  'questionna testo',
            datatype=  'CHOICE',
            # choices_eng= ['choice1', 'choice 2'],
            # choices_fr=  ['choice1', 'choice 2'],
            # choices_pt=  ['choice1', 'choice 2'],

            subquestion_eng= ['choice1', 'choice 2'],
            subquestion_fr=  ['choice1', 'choice 2'],
            subquestion_pt=  ['choice1', 'choice 2'],
            multichoices=False,
            choicecreation=False,
            mandatory=False,
            is_active=True,
            user_lastmodifier=1
            )
    question_sub = crud.question.create(db, obj_in= question_in_subquestion)
    assert question_sub.label_fr=='Question test'

    


# def test_authenticate_user(db: Session) -> None:
#     email = random_email()
#     password = random_lower_string()
#     user_in = UserCreate(email=email, password=password)
#     user = crud.user.create(db, obj_in=user_in)
#     authenticated_user = crud.user.authenticate(db, email=email, password=password)
#     assert authenticated_user
#     assert user.email == authenticated_user.email


# def test_not_authenticate_user(db: Session) -> None:
#     email = random_email()
#     password = random_lower_string()
#     user = crud.user.authenticate(db, email=email, password=password)
#     assert user is None


# def test_check_if_user_is_active(db: Session) -> None:
#     email = random_email()
#     password = random_lower_string()
#     user_in = UserCreate(email=email, password=password)
#     user = crud.user.create(db, obj_in=user_in)
#     is_active = crud.user.is_active(user)
#     assert is_active is True


# def test_check_if_user_is_active_inactive(db: Session) -> None:
#     email = random_email()
#     password = random_lower_string()
#     user_in = UserCreate(email=email, password=password, disabled=True)
#     user = crud.user.create(db, obj_in=user_in)
#     is_active = crud.user.is_active(user)
#     assert is_active


# def test_check_if_user_is_superuser(db: Session) -> None:
#     email = random_email()
#     password = random_lower_string()
#     user_in = UserCreate(email=email, password=password, is_superuser=True)
#     user = crud.user.create(db, obj_in=user_in)
#     is_superuser = crud.user.is_superuser(user)
#     assert is_superuser is True


# def test_check_if_user_is_superuser_normal_user(db: Session) -> None:
#     username = random_email()
#     password = random_lower_string()
#     user_in = UserCreate(email=username, password=password)
#     user = crud.user.create(db, obj_in=user_in)
#     is_superuser = crud.user.is_superuser(user)
#     assert is_superuser is False


# def test_get_user(db: Session) -> None:
#     password = random_lower_string()
#     username = random_email()
#     user_in = UserCreate(email=username, password=password, is_superuser=True)
#     user = crud.user.create(db, obj_in=user_in)
#     user_2 = crud.user.get(db, id=user.id)
#     assert user_2
#     assert user.email == user_2.email
#     assert jsonable_encoder(user) == jsonable_encoder(user_2)


# def test_update_user(db: Session) -> None:
#     password = random_lower_string()
#     email = random_email()
#     user_in = UserCreate(email=email, password=password, is_superuser=True)
#     user = crud.user.create(db, obj_in=user_in)
#     new_password = random_lower_string()
#     user_in_update = UserUpdate(password=new_password, is_superuser=True)
#     crud.user.update(db, db_obj=user, obj_in=user_in_update)
#     user_2 = crud.user.get(db, id=user.id)
#     assert user_2
#     assert user.email == user_2.email
#     assert verify_password(new_password, user_2.hashed_password)
