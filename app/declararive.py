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


class Journal(Base):
    __tablename__ = 'journal'
    __table_args__ = (UniqueConstraint('print_issn', 'electronic_issn', 'scielo_issn'),)
    __table_args__ += (Index('i_print_issn', 'print_issn'),)
    __table_args__ += (Index('i_electronic_issn', 'electronic_issn'),)
    __table_args__ += (Index('i_scielo_issn', 'scielo_issn'),)

    id = Column(SMALLINT(unsigned=True), primary_key=True, autoincrement=True)

    print_issn = Column(VARCHAR(9), nullable=False, index=True)
    electronic_issn = Column(VARCHAR(9), nullable=False, index=True)
    scielo_issn = Column(VARCHAR(9), nullable=False, index=True)


class JournalCollection(Base):
    __tablename__ = 'journal_collection'
    __table_args__ = (UniqueConstraint('collection', 'journal'),)

    id = Column(SMALLINT(unsigned=True), primary_key=True, autoincrement=True)

    collection = Column(TINYINT(unsigned=True), ForeignKey('collection.id'))
    title = Column(VARCHAR(255), nullable=False)
    uri = Column(VARCHAR(255))
    publisher_name = Column(VARCHAR(255))

    journal = Column(SMALLINT(unsigned=True), ForeignKey('journal.id'))


class ArticleLanguage(Base):
    __tablename__ = 'article_language'
    __table_args__ = (UniqueConstraint('language'),)

    id = Column(SMALLINT(unsigned=True), primary_key=True, autoincrement=True)

    language = Column(VARCHAR(6), nullable=False)


class ArticleFormat(Base):
    __tablename__ = 'article_format'
    __table_args__ = (UniqueConstraint('format'),)

    id = Column(TINYINT(unsigned=True), primary_key=True, autoincrement=True)

    format = Column(VARCHAR(10), nullable=False)


class Article(Base):
    __tablename__ = 'article'
    __table_args__ = (UniqueConstraint('collection', 'pid'),)
    __table_args__ += (Index('i_col_pid_jou_yop', 'collection', 'pid', 'journal', 'yop'),)

    id = Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)

    collection = Column(TINYINT(unsigned=True), ForeignKey('collection.id'))
    pid = Column(VARCHAR(128), nullable=False)
    yop = Column(SMALLINT(4))
    journal = Column(SMALLINT(unsigned=True), ForeignKey('journal.id'))


class Geolocation(Base):
    __tablename__ = 'geolocation'
    __table_args__ = (UniqueConstraint('latitude', 'longitude'),)
    __table_args__ += (Index('i_geo', 'latitude', 'longitude'),)

    id = Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)

    latitude = Column(DECIMAL(9, 6))
    longitude = Column(DECIMAL(9, 6))

