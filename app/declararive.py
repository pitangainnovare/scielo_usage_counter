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


class ControlLogFile(Base):
    __tablename__ = 'control_log_file'

    id = Column(MEDIUMINT(unsigned=True), primary_key=True, autoincrement=True)

    collection = Column(TINYINT(unsigned=True), ForeignKey('collection.id'))
    full_path = Column(VARCHAR(255), nullable=False, unique=True)
    created = Column(DATETIME, nullable=False)
    size = Column(BIGINT, nullable=False)
    name = Column(VARCHAR(255), nullable=False)
    server = Column(VARCHAR(255), nullable=False)
    year_month_day = Column(DATE, nullable=False, index=True)
    status = Column(TINYINT, default=0)


class ControlLogFileSummary(Base):
    __tablename__ = 'control_log_file_summary'

    id = Column(MEDIUMINT(unsigned=True), primary_key=True, autoincrement=True)

    logfile = Column(MEDIUMINT(unsigned=True), ForeignKey('control_log_file.id'))
    collection = Column(TINYINT(unsigned=True), ForeignKey('collection.id'))
    total_lines = Column(INTEGER, nullable=False)
    lines_parsed = Column(INTEGER)
    total_imported_lines = Column(INTEGER)
    total_ignored_lines = Column(INTEGER)
    sum_imported_ignored_lines = Column(INTEGER)
    ignored_lines_filtered = Column(INTEGER)
    ignored_lines_http_errors = Column(INTEGER)
    ignored_lines_http_redirects = Column(INTEGER)
    ignored_lines_invalid = Column(INTEGER)
    ignored_lines_bots = Column(INTEGER)
    ignored_lines_static_resources = Column(INTEGER)
    total_time = Column(MEDIUMINT)
    created = Column(DATETIME)
    status = Column(TINYINT)


class ControlDateStatus(Base):
    __tablename__ = 'control_date_status'
    __table_args__ = (UniqueConstraint('collection', 'year_month_day'),)

    id = Column(MEDIUMINT(unsigned=True), primary_key=True, autoincrement=True)

    collection = Column(TINYINT(unsigned=True), ForeignKey('collection.id'))
    year_month_day = Column(DATE, nullable=False, index=True)
    status = Column(TINYINT, default=0)
    updated = Column(DATETIME)

