#!/bin/bash

mkdir tempdir
mkdir tempdir/templates
mkdir tempdir/static

cp UserRecords.sqlite tempdir/.
cp coconut2.py tempdir/.
cp -r templates/* tempdir/templates/.
cp -r static/* tempdir/static/.

echo "FROM python" > tempdir/Dockerfile
echo "RUN pip install flask" >> tempdir/Dockerfile
echo "RUN pip install flask-wtf">> tempdir/Dockerfile
echo "RUN pip install flask_sqlalchemy">> tempdir/Dockerfile
echo "RUN pip install wtforms">> tempdir/Dockerfile
echo "COPY  ./static /home/myapp/static/" >> tempdir/Dockerfile
echo "COPY  ./templates /home/myapp/templates/" >> tempdir/Dockerfile
echo "COPY  coconut2.py /home/myapp/" >> tempdir/Dockerfile
echo "COPY  UserRecords.sqlite /home/myapp/" >> tempdir/Dockerfile
echo "EXPOSE 5050" >> tempdir/Dockerfile
echo "CMD python3 /home/myapp/coconut2.py" >> tempdir/Dockerfile

cd tempdir
docker build -t coconutapp .

docker run -t -d -p 5050:5050 --name coconutapprunning coconutapp

