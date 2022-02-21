from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, mapper, clear_mappers
from sqlalchemy.ext.indexable import index_property
from sqlalchemy import (
        Column, Integer, Float, DateTime, create_engine, UnicodeText,
        ForeignKey, Table, MetaData, Index)

import os
import pymysql


mysqlhost = os.environ.get('MYSQL_HOST')
if mysqlhost:
    mysqlpass = os.environ.get('MYSQL_ROOT_PASSWORD')
    mysqluser = os.environ['MYSQL_USER']
    mysqldb = os.environ['MYSQL_DB']
    engine = create_engine(f'mysql+pymysql://{mysqluser}:{mysqlpass}@{mysqlhost}/{mysqldb}')
else:
    engine = create_engine('sqlite:///:memory:')

Session = sessionmaker(bind=engine)
Base = declarative_base()

metadata = MetaData()



class Visitantes(Base):
    __tablename__ = 'visitantes'
    visitor_id = Column(Integer(), primary_key=True)
    email = Column(UnicodeText())
    fechaPrimeraVisita = Column(DateTime())
    fechaUltimaVisita = Column(DateTime())
    visitasTotales = Column(Integer())
    visitasAnioActual = Column(Integer())
    visitasMesActual = Column(Integer())


class Estadisticas(Base):
    __tablename__ = 'estadisticas'
    stat_id = Column(Integer(), primary_key=True)
    email = Column(UnicodeText())
    jyv = Column(UnicodeText())
    badmail = Column(UnicodeText())
    baja = Column(UnicodeText())
    fecha_envio = Column(DateTime(timezone=True))
    fecha_open = Column(DateTime(timezone=True))
    opens = Column(Integer())
    opens_virales = Column(Integer())
    fecha_click = Column(DateTime(timezone=True))
    clicks = Column(Integer())
    clicks_virales = Column(Integer())
    links = Column(Float())
    ips = Column(UnicodeText())
    navegadores = Column(UnicodeText())
    plataformas = Column(UnicodeText())
    visitor_id = Column(Integer(), ForeignKey('visitantes.visitor_id'))


class Errores(Base):
    __tablename__ = 'errores'
    err_id = Column(Integer(), primary_key=True)
    email = Column(UnicodeText())
    jyv = Column(UnicodeText())
    badmail = Column(UnicodeText())
    baja = Column(UnicodeText())
    fecha_envio = Column(UnicodeText())
    fecha_open = Column(UnicodeText())
    opens = Column(UnicodeText())
    opens_virales = Column(UnicodeText())
    fecha_click = Column(UnicodeText())
    clicks = Column(UnicodeText())
    clicks_virales = Column(UnicodeText())
    links = Column(UnicodeText())
    ips = Column(UnicodeText())
    navegadores = Column(UnicodeText())
    plataformas = Column(UnicodeText())
    error = Column(UnicodeText())


def create_all():
    Base.metadata.create_all(engine)
