FROM python:3.8.13 as base

ADD requirements.txt .
RUN pip3 install -r requirements.txt

ENV PYTHONPATH=$PYTHONPATH:/src/

ADD ./ /src/

WORKDIR /src

#FROM base as test
#RUN ["pytest", "-v", "/src/tests"]
RUN python -m spacy download en_core_web_sm 

FROM base as build
ENTRYPOINT ["python3", "/src/ml_service.py"]

