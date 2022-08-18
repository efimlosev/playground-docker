FROM python:3
WORKDIR /usr/src/app
ENV APP_ID=""
ENV APP_KEY=""
ENV SECRET_KEY=""


 

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5000
CMD [ "python", "./lru.py" ]


