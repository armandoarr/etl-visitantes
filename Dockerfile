FROM python:3.8
COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN mkdir etl && mkdir /etl/visitas/
COPY . ./etl
COPY visitas/ /etl/visitas
COPY logs/ /etl/logs

WORKDIR etl/

CMD python file_processor.py
