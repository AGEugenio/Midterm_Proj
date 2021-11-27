FROM python
RUN pip install flask
RUN pip install flask flask-pymongo pymongo[srv]
COPY  ./static /home/myapp/static/
COPY  ./templates /home/myapp/templates/
COPY  coconut.py /home/myapp/
EXPOSE 5050
CMD python3 /home/myapp/coconut.py
