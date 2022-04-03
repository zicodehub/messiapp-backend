from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import Boolean, Date, Enum

from app.db.base_class import Base

if TYPE_CHECKING:
    from .ma import Ma
    from .answer import Answer
    from .cm import CM
#     from .user import User  # noqa: F401
#TODO make affectation pattern for user 


cm_table = Table('cm_association', Base.metadata,
    Column('country_id', ForeignKey('country.id'), primary_key=True),
    Column('user_id', ForeignKey('user.id'), primary_key=True)
)

class Country(Base):
    """
    It represent a data point
    """
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    is_active = Column(Boolean, default=True, index=True)
    mas= relationship('Ma', back_populates='country')
    cms= relationship(
        "User", 
        secondary= cm_table,
        back_populates="countries")
    answers=relationship("Answer")
