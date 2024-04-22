import os
import pandas as pd
import sqlalchemy as db
from sqlalchemy import func as sfn
from sqlalchemy.orm import sessionmaker
from funcs.tablefuncs import Place


class sqlConnection:

    dbvars = {}
    _session = None
    _engine = None
    _table = None

    def __init__(self):

        self.dbvars = {
            "username": os.getenv("MYSQL_DB_USER"),
            "password": os.getenv("MYSQL_DB_PWD"),
            "host": os.getenv("MYSQL_DB_HOST"),
            "database": os.getenv("MYSQL_DB_DATABASE"),
        }
        self._table = Place
        self.startSession()

    def startSession(self):
        try:
            base_url = db.URL.create("mysql+mysqldb", **self.dbvars)
            url = base_url.update_query_pairs(
                [("charset", os.getenv("MYSQL_DB_CHARSET"))]
            )
            self._engine = db.create_engine(url, echo=True, pool_recycle=600)
            Session = sessionmaker(bind=self._engine)
            self._session = Session()
        except Exception as error:
            print(error)
            exit()

    def createTable(self):
        try:
            self._table.__table__.drop(self._engine, checkfirst=True)
            self._table.__table__.create(self._engine)
        except Exception as error:
            print(error)
            exit()

    def getTablename(self):
        return self._table.__tablename__

    def getTable(self):
        return self._table

    def queryAll(self):
        try:
            return self._session.query(self._table)
        except Exception as error:
            print(error)
            exit()

    def queryFilter(self, filter):
        try:
            return self._session.query(self._table).filter(filter)
        except Exception as error:
            print(error)
            exit()

    def execInsert(self, rows):
        try:
            self._session.execute(db.insert(self._table), rows)
            self._session.commit()
        except Exception as error:
            print(error)
            exit()

    def execUpdatePostcodes(self, params):
        try:
            stmt = (
                db.update(Place)
                .where(Place.objectid == db.bindparam("oid"))
                .values(postcode=db.bindparam("pc"), distance=db.bindparam("d"))
            )
            with self._engine.begin() as conn:
                conn.execute(stmt, params)
        except Exception as error:
            print(error)
            exit()

    def toDataFrame(self):
        try:
            return pd.read_sql_table(self._table.__tablename__, self._engine)
        except Exception as error:
            print(error)
            exit()

    def findIssues(self):
        try:
            result = {}
            subq = (
                db.select(self._table.latlon)
                .group_by(self._table.latlon)
                .having(sfn.count(self._table.latlon) > 1)
            )
            result["DUPLICATE_LATLONS"] = self._session.scalars(
                db.select(self._table).where(self._table.latlon.in_(subq))
            ).all()

            subq = (
                db.select(self._table.location)
                .group_by(self._table.location)
                .having(sfn.count(Place.location) > 1)
            )
            result["DUPLICATE_LOCATIONS"] = self._session.scalars(
                db.select(self._table).where(self._table.location.in_(subq))
            ).all()
            return result
        except Exception as error:
            print(error)
            exit()
