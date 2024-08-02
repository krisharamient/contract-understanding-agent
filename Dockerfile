FROM python:3.12-slim

WORKDIR /app

COPY *.py /app

COPY requirements.txt /app

RUN pip3 install -r requirements.txt

EXPOSE 8501

ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501"]