This is the master webservice for crawling.

#Prerequisites
#1. Python
#2. MySQL
#3. HTTP ports must be opened

#Steps to Config/Create

#1. Update MySQL DB config in crawlerMasterWebService.py
#2. Login to mysql and create database
    mysql -uroot -pgghhjj1
    create database crawler
#3. Install the following dependencies
    sudo easy_install web.py
    sudo pip install pymongo
    sudo apt-get install python-bson
    sudo pip install peewee
    sudo pip install requests
    sudo pip install pymysql


#3. Run the server with nohup
    nohup python crawlerMasterWebService.py > webService$(date -d "today" +"%Y%m%d%H%M").log 2>&1&
