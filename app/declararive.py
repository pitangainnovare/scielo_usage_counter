from sqlalchemy import Column, ForeignKey, UniqueConstraint, Index
from sqlalchemy.dialects.mysql import BIGINT, BOOLEAN, DATE, DATETIME, DECIMAL, INTEGER, MEDIUMINT, TINYINT, VARCHAR
from sqlalchemy.dialects.mysql.types import SMALLINT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declarative_mixin


Base = declarative_base()



class Collection(Base):
    __tablename__ = 'collection'
    __table_args__ = (UniqueConstraint('acronym',),)

    id = Column(TINYINT(unsigned=True), primary_key=True, autoincrement=True)

    acronym = Column(VARCHAR(3), nullable=False)
    name = Column(VARCHAR(128), nullable=False, index=True)
