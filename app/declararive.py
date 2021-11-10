from sqlalchemy import Column, ForeignKey, UniqueConstraint, Index
from sqlalchemy.dialects.mysql import BIGINT, BOOLEAN, DATE, DATETIME, DECIMAL, INTEGER, MEDIUMINT, TINYINT, VARCHAR
from sqlalchemy.dialects.mysql.types import SMALLINT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declarative_mixin


Base = declarative_base()

