# main image
FROM python:3.7.3

# set directory
WORKDIR /app

# copy files
ADD . /app

# install require
RUN pip install -r requirements.txt

ENV NAME model

# run bot
CMD ["python", "bot.py"]