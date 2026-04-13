from sqlalchemy import and_, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound

import datetime

from scielo_usage_counter import values

import scielo_usage_counter.database.declararive as models


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
            ).order_by(models.ControlLogFile.date)
    except NoResultFound:
        return []


def _get_date_status(dates):
    date_status = {}

    for r in dates:
        date_status[r.date] = r.status

    return date_status


def _get_previous_and_next_dates(date, interval=2):
    all_days = [date]

    for i in range(1, interval + 1):
        all_days.append(date + datetime.timedelta(days=-i))
        all_days.append(date + datetime.timedelta(days=+i))

    return all_days


def _get_enabled_dates_by_status_value(session, collection, date_status: dict, status_value: int):
    enabled_dates = []

    for date, status in date_status.items():
        pn_dates = _get_previous_and_next_dates(date)
        is_valid_date = _check_previous_and_next_dates(session, collection, pn_dates)

        if status == status_value and is_valid_date:
            enabled_dates.append(date)

    return enabled_dates


def _check_previous_and_next_dates(session, collection, dates):
    for d in dates:
        try:
            cds = session.query(models.ControlDateStatus).filter(
                and_(
                    models.ControlDateStatus.collection == collection,
                    models.ControlDateStatus.date == d,
                )
            ).one()

            if cds.status not in {values.DATE_STATUS_EXTRACTING_PRETABLE, values.DATE_STATUS_NO_LOG} and cds.status < values.DATE_STATUS_LOADED:
                return False

        except NoResultFound:
            return False

    return True


def _reconcile_dates_without_valid_logs(session, collection, now=None, wait_days=values.NO_LOG_WAIT_DAYS):
    if now is None:
        now = datetime.datetime.now()

    cutoff_date = (now - datetime.timedelta(days=wait_days)).date()

    date_statuses = session.query(models.ControlDateStatus).filter(
        models.ControlDateStatus.collection == collection
    ).all()
    existing_dates = {date_status.date for date_status in date_statuses}

    log_rows = session.query(models.ControlLogFile.date, models.ControlLogFile.status).filter(
        and_(
            models.ControlLogFile.collection == collection,
            models.ControlLogFile.date.isnot(None),
        )
    ).all()

    all_log_dates = {date for date, _ in log_rows}
    valid_or_pending_log_dates = {
        date for date, status in log_rows if status != values.LOGFILE_STATUS_INVALIDATED
    }

    reference_dates = sorted(existing_dates.union(all_log_dates))
    changed = False

    if reference_dates:
        current_date = reference_dates[0]
        last_reference_date = min(reference_dates[-1], now.date())

        while current_date <= last_reference_date:
            if current_date not in existing_dates:
                new_status = values.DATE_STATUS_QUEUE
                if current_date <= cutoff_date and current_date not in valid_or_pending_log_dates:
                    new_status = values.DATE_STATUS_NO_LOG

                session.add(
                    models.ControlDateStatus(
                        collection=collection,
                        date=current_date,
                        status=new_status,
                    )
                )
                changed = True

            current_date += datetime.timedelta(days=1)

    for date_status in date_statuses:
        has_valid_or_pending_log = date_status.date in valid_or_pending_log_dates
        if date_status.status == values.DATE_STATUS_QUEUE and not has_valid_or_pending_log and date_status.date <= cutoff_date:
            date_status.status = values.DATE_STATUS_NO_LOG
            changed = True

    if changed:
        session.commit()


def get_non_pretable_dates(str_connection, collection):
    session = get_session(str_connection)
    try:
        _reconcile_dates_without_valid_logs(session, collection)

        parsed_dates = session.query(models.ControlDateStatus).filter(
            and_(
                models.ControlDateStatus.collection == collection,
                models.ControlDateStatus.status == values.DATE_STATUS_LOADED,
            )
        ).order_by(models.ControlDateStatus.date.desc())

        date2status = _get_date_status(parsed_dates)

        return _get_enabled_dates_by_status_value(session, collection, date2status, values.DATE_STATUS_LOADED)

    except NoResultFound:
        return []


def get_unsorted_pretables(str_connection, collection):
    session = get_session(str_connection)
    try:
        unsorted_pretable_dates = session.query(models.ControlDateStatus).filter(
            and_(
                models.ControlDateStatus.collection == collection,
                models.ControlDateStatus.status == values.DATE_STATUS_EXTRACTING_PRETABLE,
            )
        ).order_by(models.ControlDateStatus.date.desc())

        date2status = _get_date_status(unsorted_pretable_dates)

        return _get_enabled_dates_by_status_value(session, collection, date2status, values.DATE_STATUS_EXTRACTING_PRETABLE)

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


def set_control_date_status(str_connection, collection, date, status):
    session = get_session(str_connection)
    try:
        cds = session.query(models.ControlDateStatus).filter(
            and_(
                models.ControlDateStatus.collection == collection,
                models.ControlDateStatus.date == date,
            )
        ).one()
        cds.status = status
        session.commit()
    except NoResultFound:
        ...
    except MultipleResultsFound:
        ...
