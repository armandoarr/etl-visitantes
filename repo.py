from contextlib import contextmanager
from model import Estadisticas, Visitantes, Errores, Session
from datetime import datetime

import logging
import sqlalchemy

logging.basicConfig(filename='mysql.log')
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)


@contextmanager
def session_scope():
    session = Session()
    try:
        yield session
        session.commit()
    except Exception as ex:
        session.rollback()
        raise ex
    finally:
        session.close()


class Repository(object):
    def __init__(self, session):
        self.session = session

    def get_visitor_id(self, visitor):
        v = self.session.query(Visitantes).filter(Visitantes.email == visitor['email']).first()
        if not v:
            return None
        else:
            visitor_id = v.visitor_id
            return visitor_id

    def store_statistics(self, estadisticas):
        for e in estadisticas:
            visit_id = self.get_visitor_id(e)
            e['visitor_id'] = visit_id
        reg = [Estadisticas(**est) for est in estadisticas]
        try:
            self.session.bulk_save_objects(reg)
            self.session.commit()
        except Exception as e:
            print(e)
            raise e

    def store_errors(self, errores):
        regs = [Errores(**e) for e in errores]
        try:
            self.session.bulk_save_objects(regs)
            self.session.commit()
        except Exception as ex:
            raise ex

    def add_visitor(self, visitor):
        params = {
            "email": visitor['email'],
            "fechaPrimeraVisita": visitor['fecha_open'],
            "fechaUltimaVisita": visitor['fecha_open'],
            "visitasTotales": 1,
            "visitasAnioActual": 1,
            "visitasMesActual": 1
            }
        q = Visitantes(**params)
        try:
            self.session.add(q)
            self.session.commit()
        except Exception as ex:
            print(ex)
            raise ex
        print(f'visitante {q.visitor_id} agregado')

        return q.visitor_id

    def update_visitor(self, visitor):
        vid = self.get_visitor_id(visitor)
        if not vid:
            self.add_visitor(visitor)
        self.session.query(Visitantes).filter(Visitantes.visitor_id == vid). \
            update({
                "visitasTotales": (Visitantes.visitasTotales+1),
                "visitasMesActual": (Visitantes.visitasMesActual+1),
                "visitasAnioActual": (Visitantes.visitasAnioActual+1),
                "fechaUltimaVisita": visitor['fecha_open']})
        try:
            self.session.commit()
        except Exception as e:
            print('Algo salió mal')
            raise e
