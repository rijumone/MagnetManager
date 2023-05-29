FROM python:3.9
WORKDIR /app
RUN python -m pip install --upgrade pip wheel setuptools
COPY requirements.txt .
RUN pip install -r requirements.txt

# CMD python -m http.server
CMD flask --debug run -h 0.0.0.0
