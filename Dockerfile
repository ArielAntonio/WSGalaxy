FROM python:3.7

WORKDIR ./

COPY . .

RUN pip install --upgrade pip && \
	pip install -r requirements.txt 

CMD ["python", "run.py"]