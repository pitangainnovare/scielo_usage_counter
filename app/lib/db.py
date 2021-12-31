
import app.declararive as models
import app.values as values

from sqlalchemy import and_, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound


def create_tables(str_connection):
    engine = create_engine(str_connection)
    models.Base.metadata.create_all(engine)


def get_session(str_connection):
    engine = create_engine(str_connection)
    session = sessionmaker(bind=engine)
    return session()


def get_collection_id(str_connection, collection_acronym):
    session = get_session(str_connection)
    return session.query(models.Collection).filter(models.Collection.acronym == collection_acronym).one().id


def get_collection_acronym(str_connection, collection_id):
    session = get_session(str_connection)
    return session.get(models.Collection, collection_id).one().acronym


def get_non_parsed_logs(str_connection, collection):
    session = get_session(str_connection)
    try:
        return session.query(
            models.ControlLogFile).filter(
                and_(
                    models.ControlLogFile.collection == collection, 
                    models.ControlLogFile.status == values.LOGFILE_STATUS_QUEUE,
                )
            ).order_by(models.ControlLogFile.year_month_day)
    except NoResultFound:
        return []


def get_logfile_status(str_connection, logfile_id):
    session = get_session(str_connection)
    try:
        return session.query(
            models.ControlLogFile).filter(
                models.ControlLogFile.id == logfile_id
            )
    except NoResultFound:
        return []


def set_logfile_status(str_connection, logfile_id, status):
    session = get_session(str_connection)
    lf = session.get(models.ControlLogFile, logfile_id) 
    lf.status = status
    session.commit()
