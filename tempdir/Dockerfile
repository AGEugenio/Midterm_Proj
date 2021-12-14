FROM python
RUN pip install flask
RUN pip install flask-wtf
RUN pip install flask_sqlalchemy
RUN pip install wtforms
COPY  ./static /home/myapp/static/
COPY  ./templates /home/myapp/templates/
COPY  coconut2.py /home/myapp/
COPY  UserRecords.sqlite /home/myapp/
EXPOSE 5050
CMD python3 /home/myapp/coconut2.py
