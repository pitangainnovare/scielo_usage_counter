from sqlalchemy import Column, ForeignKey, UniqueConstraint, Index
from sqlalchemy.dialects.mysql import BIGINT, BOOLEAN, DATE, DATETIME, DECIMAL, INTEGER, MEDIUMINT, TINYINT, VARCHAR
from sqlalchemy.dialects.mysql.types import SMALLINT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declarative_mixin


Base = declarative_base()

@declarative_mixin
class MetricMixin:
    id = Column(BIGINT, primary_key=True, autoincrement=True)

    total_item_requests = Column(INTEGER, nullable=False)
    total_item_investigations = Column(INTEGER, nullable=False)
    unique_item_requests = Column(INTEGER, nullable=False)
    unique_item_investigations = Column(INTEGER, nullable=False)


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


class MetricStatus(Base):
    __tablename__ = 'metric_status'
    __table_args__ = (UniqueConstraint('collection', 'metric_table', 'year_month_day',),)
    __table_args__ += (Index('i_col_mt_ymd', 'collection', 'metric_table', 'year_month_day',),)

    id = Column(MEDIUMINT(unsigned=True), primary_key=True, autoincrement=True)

    collection = Column(TINYINT(unsigned=True), ForeignKey('collection.id'))
    metric_table = Column(VARCHAR(32), nullable=False)
    year_month_day = Column(DATE, nullable=False, index=True)
    status = Column(BOOLEAN, default=False)
    updated = Column(DATETIME)


class MetricArticleDetailed(MetricMixin, Base):
    __tablename__ = 'metric_article_detailed'
    __table_args__ = (UniqueConstraint('year_month_day', 'collection', 'article', 'format', 'language', 'geolocation'),)
    __table_args__ += (Index('i_ymd_art_for_lan_geo', 'year_month_day', 'collection', 'article', 'format', 'language', 'geolocation'),)

    article = Column(INTEGER(unsigned=True), ForeignKey('article.id'))
    collection = Column(TINYINT(unsigned=True), ForeignKey('collection.id'))
    format = Column(TINYINT(unsigned=True), ForeignKey('article_format.id'))
    language = Column(SMALLINT(unsigned=True), ForeignKey('article_language.id'))
    geolocation = Column(INTEGER(unsigned=True), ForeignKey('geolocation.id'))

    year_month_day = Column(DATE, nullable=False)


class MetricArticleDaily(MetricMixin, Base):
    __tablename__ = 'metric_article_daily'
    __table_args__ = (UniqueConstraint('collection', 'year_month_day', 'article'),)
    __table_args__ += (Index('i_col_ymd_art', 'collection', 'year_month_day', 'article'),)

    article = Column(INTEGER(unsigned=True), ForeignKey('article.id'))
    collection = Column(TINYINT(unsigned=True), ForeignKey('collection.id'))

    year_month_day = Column(DATE, nullable=False)


class MetricArticleMonthly(MetricMixin, Base):
    __tablename__ = 'metric_article_monthly'
    __table_args__ = (UniqueConstraint('collection', 'year_month', 'article'),)
    __table_args__ += (Index('i_col_ym_art', 'collection', 'year_month', 'article'),)

    article = Column(INTEGER(unsigned=True), ForeignKey('article.id'))
    collection = Column(TINYINT(unsigned=True), ForeignKey('collection.id'))

    year_month = Column(DATE, nullable=False)


class MetricArticleMonthlyLanguage(MetricMixin, Base):
    __tablename__ = 'metric_article_monthly_language'
    __table_args__ = (UniqueConstraint('year_month', 'collection', 'article', 'language'),)
    __table_args__ += (Index('i_ym_art_lan', 'year_month', 'collection', 'article', 'language'),)

    article = Column(INTEGER(unsigned=True), ForeignKey('article.id'))
    collection = Column(TINYINT(unsigned=True), ForeignKey('collection.id'))
    language = Column(SMALLINT(unsigned=True), ForeignKey('article_language.id'))

    year_month = Column(DATE, nullable=False)


class MetricArticleMonthlyFormat(MetricMixin, Base):
    __tablename__ = 'metric_article_monthly_format'
    __table_args__ = (UniqueConstraint('year_month', 'collection', 'article', 'format'),)
    __table_args__ += (Index('i_ym_art_for', 'year_month', 'collection', 'article', 'format'),)

    article = Column(INTEGER(unsigned=True), ForeignKey('article.id'))
    collection = Column(TINYINT(unsigned=True), ForeignKey('collection.id'))
    format = Column(TINYINT(unsigned=True), ForeignKey('article_format.id'))

    year_month = Column(DATE, nullable=False)


class MetricArticleMonthlyGeolocation(MetricMixin, Base):
    __tablename__ = 'metric_article_monthly_geolocation'
    __table_args__ = (UniqueConstraint('year_month', 'collection', 'article', 'geolocation'),)
    __table_args__ += (Index('i_ym_art_geo', 'year_month', 'collection', 'article', 'geolocation'),)

    article = Column(INTEGER(unsigned=True), ForeignKey('article.id'))
    collection = Column(TINYINT(unsigned=True), ForeignKey('collection.id'))
    geolocation = Column(INTEGER(unsigned=True), ForeignKey('geolocation.id'))

    year_month = Column(DATE, nullable=False)


class MetricArticleMonthlyGeolocationLanguage(MetricMixin, Base):
    __tablename__ = 'metric_article_monthly_geolocation_language'
    __table_args__ = (UniqueConstraint('year_month', 'collection', 'article', 'geolocation', 'language'),)
    __table_args__ += (Index('i_ym_art_geo_lan', 'year_month', 'collection', 'article', 'geolocation', 'language'),)

    article = Column(INTEGER(unsigned=True), ForeignKey('article.id'))
    collection = Column(TINYINT(unsigned=True), ForeignKey('collection.id'))
    geolocation = Column(INTEGER(unsigned=True), ForeignKey('geolocation.id'))
    language = Column(SMALLINT(unsigned=True), ForeignKey('article_language.id'))

    year_month = Column(DATE, nullable=False)


class MetricArticleMonthlyGeolocationFormat(MetricMixin, Base):
    __tablename__ = 'metric_article_monthly_geolocation_format'
    __table_args__ = (UniqueConstraint('year_month', 'collection', 'article', 'geolocation', 'format'),)
    __table_args__ += (Index('i_ym_art_geo_for', 'year_month', 'collection', 'article', 'geolocation', 'format'),)

    article = Column(INTEGER(unsigned=True), ForeignKey('article.id'))
    collection = Column(TINYINT(unsigned=True), ForeignKey('collection.id'))
    geolocation = Column(INTEGER(unsigned=True), ForeignKey('geolocation.id'))
    format = Column(TINYINT(unsigned=True), ForeignKey('article_format.id'))

    year_month = Column(DATE, nullable=False)


class MetricArticleMonthlyFormatLanguage(MetricMixin, Base):
    __tablename__ = 'metric_article_monthly_format_language'
    __table_args__ = (UniqueConstraint('year_month', 'collection', 'article', 'format', 'language'),)
    __table_args__ += (Index('i_ym_art_for', 'year_month', 'collection', 'article', 'format', 'language'),)

    article = Column(INTEGER(unsigned=True), ForeignKey('article.id'))
    collection = Column(TINYINT(unsigned=True), ForeignKey('collection.id'))
    format = Column(TINYINT(unsigned=True), ForeignKey('article_format.id'))
    language = Column(SMALLINT(unsigned=True), ForeignKey('article_language.id'))

    year_month = Column(DATE, nullable=False)


class MetricJournalDetailed(MetricMixin, Base):
    __tablename__ = 'metric_journal_detailed'
    __table_args__ = (UniqueConstraint('year_month_day', 'collection', 'format', 'language', 'geolocation', 'journal', 'yop'),)
    __table_args__ += (Index('i_col_ymd_for_lan_geo_yop_jou', 'collection', 'year_month_day', 'format', 'language', 'geolocation' ,'yop', 'journal'),)

    journal = Column(SMALLINT(unsigned=True), ForeignKey('journal.id'))
    collection = Column(TINYINT(unsigned=True), ForeignKey('collection.id'))
    format = Column(TINYINT(unsigned=True), ForeignKey('article_format.id'))
    language = Column(SMALLINT(unsigned=True), ForeignKey('article_language.id'))
    geolocation = Column(INTEGER(unsigned=True), ForeignKey('geolocation.id'))
    yop = Column(INTEGER(4))

    year_month_day = Column(DATE, nullable=False)


class MetricJournalDailyYOP(MetricMixin, Base):
    __tablename__ = 'metric_journal_daily_yop'
    __table_args__ = (UniqueConstraint( 'year_month_day', 'collection', 'yop', 'journal'),)
    __table_args__ += (Index('i_col_ymd_yop_journal', 'collection', 'year_month_day', 'yop', 'journal'),)

    journal = Column(SMALLINT(unsigned=True), ForeignKey('journal.id'))
    collection = Column(TINYINT(unsigned=True), ForeignKey('collection.id'))
    yop = Column(INTEGER(4))

    year_month_day = Column(DATE, nullable=False)


class MetricJournalDaily(MetricMixin, Base):
    __tablename__ = 'metric_journal_daily'
    __table_args__ = (UniqueConstraint( 'year_month_day', 'collection', 'journal'),)
    __table_args__ += (Index('i_col_ymd_journal', 'collection', 'year_month_day', 'journal'),)

    journal = Column(SMALLINT(unsigned=True), ForeignKey('journal.id'))
    collection = Column(TINYINT(unsigned=True), ForeignKey('collection.id'))

    year_month_day = Column(DATE, nullable=False)


class MetricJournalMonthly(MetricMixin, Base):
    __tablename__ = 'metric_journal_monthly'
    __table_args__ = (UniqueConstraint('collection', 'year_month', 'journal'),)
    __table_args__ += (Index('i_col_ym_jou', 'collection', 'year_month', 'journal'),)

    journal = Column(SMALLINT(unsigned=True), ForeignKey('journal.id'))
    collection = Column(TINYINT(unsigned=True), ForeignKey('collection.id'))

    year_month = Column(DATE, nullable=False)


class MetricJournalMonthlyYOP(MetricMixin, Base):
    __tablename__ = 'metric_journal_monthly_yop'
    __table_args__ = (UniqueConstraint('collection', 'year_month', 'yop', 'journal'),)
    __table_args__ += (Index('i_col_ym_jou', 'collection', 'year_month', 'yop', 'journal'),)

    journal = Column(SMALLINT(unsigned=True), ForeignKey('journal.id'))
    collection = Column(TINYINT(unsigned=True), ForeignKey('collection.id'))
    yop = Column(INTEGER(4))

    year_month = Column(DATE, nullable=False)


class MetricJournalMonthlyFormat(MetricMixin, Base):
    __tablename__ = 'metric_journal_monthly_format'
    __table_args__ = (UniqueConstraint('collection', 'year_month', 'format', 'journal'),)
    __table_args__ += (Index('i_col_ym_jou', 'collection', 'year_month', 'format', 'journal'),)

    journal = Column(SMALLINT(unsigned=True), ForeignKey('journal.id'))
    collection = Column(TINYINT(unsigned=True), ForeignKey('collection.id'))
    format = Column(TINYINT(unsigned=True), ForeignKey('article_format.id'))

    year_month = Column(DATE, nullable=False)


class MetricJournalMonthlyLanguage(MetricMixin, Base):
    __tablename__ = 'metric_journal_monthly_language'
    __table_args__ = (UniqueConstraint('collection', 'year_month', 'language', 'journal'),)
    __table_args__ += (Index('i_col_ym_jou', 'collection', 'year_month', 'language', 'journal'),)

    journal = Column(SMALLINT(unsigned=True), ForeignKey('journal.id'))
    collection = Column(TINYINT(unsigned=True), ForeignKey('collection.id'))
    language = Column(SMALLINT(unsigned=True), ForeignKey('article_language.id'))

    year_month = Column(DATE, nullable=False)


class MetricJournalMonthlyGeolocation(MetricMixin, Base):
    __tablename__ = 'metric_journal_monthly_geolocation'
    __table_args__ = (UniqueConstraint('collection', 'year_month', 'geolocation', 'journal'),)
    __table_args__ += (Index('i_col_ym_jou', 'collection', 'year_month', 'geolocation', 'journal'),)

    journal = Column(SMALLINT(unsigned=True), ForeignKey('journal.id'))
    collection = Column(TINYINT(unsigned=True), ForeignKey('collection.id'))
    geolocation = Column(INTEGER(unsigned=True), ForeignKey('geolocation.id'))

    year_month = Column(DATE, nullable=False)


class MetricJournalMonthlyGeolocationFormat(MetricMixin, Base):
    __tablename__ = 'metric_journal_monthly_geolocation_format'
    __table_args__ = (UniqueConstraint('collection', 'year_month', 'geolocation', 'format', 'journal'),)
    __table_args__ += (Index('i_col_ym_jou', 'collection', 'year_month', 'geolocation', 'format', 'journal'),)

    journal = Column(SMALLINT(unsigned=True), ForeignKey('journal.id'))
    collection = Column(TINYINT(unsigned=True), ForeignKey('collection.id'))
    geolocation = Column(INTEGER(unsigned=True), ForeignKey('geolocation.id'))
    format = Column(TINYINT(unsigned=True), ForeignKey('article_format.id'))

    year_month = Column(DATE, nullable=False)


class MetricJournalMonthlyGeolocationLanguage(MetricMixin, Base):
    __tablename__ = 'metric_journal_monthly_geolocation_language'
    __table_args__ = (UniqueConstraint('collection', 'year_month', 'geolocation', 'language', 'journal'),)
    __table_args__ += (Index('i_col_ym_jou', 'collection', 'year_month', 'geolocation', 'language', 'journal'),)

    journal = Column(SMALLINT(unsigned=True), ForeignKey('journal.id'))
    collection = Column(TINYINT(unsigned=True), ForeignKey('collection.id'))
    geolocation = Column(INTEGER(unsigned=True), ForeignKey('geolocation.id'))
    language = Column(SMALLINT(unsigned=True), ForeignKey('article_language.id'))

    year_month = Column(DATE, nullable=False)


class MetricJournalMonthlyFormatLanguage(MetricMixin, Base):
    __tablename__ = 'metric_journal_monthly_format_language'
    __table_args__ = (UniqueConstraint('collection', 'year_month', 'format', 'language', 'journal'),)
    __table_args__ += (Index('i_col_ym_jou', 'collection', 'year_month', 'format', 'language', 'journal'),)

    journal = Column(SMALLINT(unsigned=True), ForeignKey('journal.id'))
    collection = Column(TINYINT(unsigned=True), ForeignKey('collection.id'))
    format = Column(TINYINT(unsigned=True), ForeignKey('article_format.id'))
    language = Column(SMALLINT(unsigned=True), ForeignKey('article_language.id'))

    year_month = Column(DATE, nullable=False)

