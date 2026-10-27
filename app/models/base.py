from sqlalchemy.orm import DeclarativeBase

"""Gets the DeclarativeBase from the orm, DeclarativeBase should be inherited to maintain metadata of 
the tables created from the Base"""


class Base(DeclarativeBase):
    pass
