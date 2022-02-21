import pysftp
import re
import csv
import os
import sys
import logging

from datetime import datetime
from zipfile import ZipFile
from repo import session_scope, Repository

hostname = 'hostname'
username = 'username'
password = 'password'
file_path = '/home/vinkOS/archivosVisitas'

# sftp_connection = pysftp.Connection(hostname=hostname, username=username, password=password)

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.info('this is information')


def get_sftp_files():
    # with pysftp.Connection(hostname=hostname, username=username, password=password) as conn:
    #     print('Conexión exitosa...')

    # #conn.pwd(file_path)
    # local_path = '/home/etl/visitas'
    # files = conn.listdir_attr()
    # list_of_files = [attr.filename for attr in files]
    # for l in list_of_files:
    #     conn.get(file_path+'/'+ l, local_path)
    file_path = os.path.join(sys.path[0], 'visitas/')
    archivos = [file for file in os.listdir(file_path) if os.path.isfile(file_path+file)]

    return archivos


# def del_sftp_files(files):
#     with sftp_connection as conn:
#         for f in file:
#             conn.execute('rm -f {0}/{1}'.format(file_path, f))


def validate_files(files):
    match = '^[report]+[_]+[0-9]+[.txt]'
    for f in files:
        if not (re.search(match, f)):
            files.remove(f)
            logger.warning(f'Archivo {f} malo')
    return files


def validate_email(email):
    match = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    if(re.search(match, email)):
        #print("Valid Email")
        return True
    else:
        #print("Invalid Email")
        return False


def validate_dates(dt):
    try:
        datetime.strptime(dt, "%d/%m/%Y %H:%M")
        return True
    except:
        logger.warning('fecha invalida: {0}'.format(dt))
        return False


def convert_dates(items):
    for item in items:
        item.update({
            "fecha_envio": datetime.strptime(item['fecha_envio'], "%d/%m/%Y %H:%M"),
            "fecha_open": datetime.strptime(item['fecha_open'], "%d/%m/%Y %H:%M"),
            "fecha_click": datetime.strptime(item['fecha_click'], "%d/%m/%Y %H:%M")})
        if 'jk' in item.keys():
            item.update({'jyv': item['jk']})
            item.pop('jk')
        if 'fgh' in item.keys():
            item.update({'fgh': item['fgh']})
            item.pop('fgh')
        item.update({'links': item['links'].replace(',', '.')})
    return items


def parse_files(file):
    with open('visitas/'+file, 'r') as f:
        csv_reader = csv.reader(f, delimiter=',')
        rows = [row for row in csv_reader]
    header = rows.pop(0)
    header = [h.lower().strip().replace(" ", "_") for h in header]
    regs = []
    for row in rows:
        d = {header[i]: row[i] for i in range(len(header))}
        regs.append(d)
    return regs


def validate_processed_files(processed):
    valid = []
    invalid = []
    for p in processed:
        check1 = validate_dates(p['fecha_envio'])
        check2 = validate_dates(p['fecha_open'])
        check3 = validate_dates(p['fecha_click'])
        check_email = validate_email(p['email'])
        if check_email and check1 and check2 and check3:
            valid.append(p)
        else:
            p['error'] = 'Invalid dates or email'
            invalid.append(p)
    return valid, invalid


def process_files():
    files = get_sftp_files()
    parseados = [parse_files(f) for f in files if files]
    if not parseados:
        logger.info('No hay archivos que procesar')
        pass
    for p in parseados:
        validos, invalidos = validate_processed_files(p)
        validos = convert_dates(validos)
        with session_scope() as session:
            repo = Repository(session)
            for v in validos:
                repo.update_visitor(v)
            repo.store_statistics(validos)
            #repo.store_errors(invalidos)
    bfile = create_backups(files)
    logger.info('Archivo de respaldo {0} creado'.format(bfile))
    # del_sftp_files(parseados)


def create_backups(files):
    now = datetime.now().date().isoformat()
    backup_file = 'backup_reports_{0}.zip'.format(now)
    backup_dir = os.path.join(sys.path[0], 'visitas/bckp/')
    zipobject = ZipFile(backup_dir+backup_file, 'w')
    for f in files:
        zipobject.write('visitas/'+f)
    zipobject.close()
    return backup_file


if __name__ == '__main__':
    process_files()
