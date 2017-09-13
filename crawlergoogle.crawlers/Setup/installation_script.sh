#!/bin/bash

# Update and install basic ubuntu packages

echo "I am going to update repositories and download following packages"
echo "Packages to download : build-essential git sqlite3 apache2 debconf-utils libxml2-dev libxslt-dev python-mysqldb libmysqlclient-dev"

sudo apt-get update
sudo apt-get install -y build-essential git sqlite3 apache2 debconf-utils libxml2-dev libxslt-dev python-mysqldb libmysqlclient-dev


# setup param for un-interupted mysql server setup with defaul password = gghhjj1 and username = root
sudo debconf-set-selections <<< 'mysql-server mysql-server/root_password password gghhjj1'
sudo debconf-set-selections <<< 'mysql-server mysql-server/root_password_again password gghhjj1'
sudo apt-get -y install mysql-server

# install php5
#sudo apt-get install -y php5 libapache2-mod-php5 php5-mcrypt
#If you are using apache2.4 and PHP 7, run
sudo apt-get -y install php-mbstring php7.0-mbstring php-gettext

# setup param for un-interupted phpmyadmin setup with default password = gghhjj1 and username = root
sudo debconf-set-selections <<< 'phpmyadmin phpmyadmin/dbconfig-install boolean true'
sudo debconf-set-selections <<< 'phpmyadmin phpmyadmin/app-password-confirm password gghhjj1'
sudo debconf-set-selections <<< 'phpmyadmin phpmyadmin/mysql/admin-pass password gghhjj1'
sudo debconf-set-selections <<< 'phpmyadmin phpmyadmin/mysql/app-pass password gghhjj1'
sudo debconf-set-selections <<< 'phpmyadmin phpmyadmin/reconfigure-webserver multiselect apache2'
sudo apt-get -y install phpmyadmin

sudo service apache2 reload

# install build dependency for compiling python2.7 branch
sudo apt-get build-dep -y python python2.7
# download latest python 2./7.11, extract, build and install it
mkdir $HOME/temp_dev
wget -qO- https://www.python.org/ftp/python/2.7.11/Python-2.7.11.tar.xz | tar xJ -C $HOME/temp_dev/
cd $HOME/temp_dev/Python-2.7.11
./configure
make 
sudo make install 

# to avoid pip errors
sudo apt-get install build-essential autoconf libtool pkg-config python-opengl python-imaging python-pyrex python-pyside.qtopengl idle-python2.7 qt4-dev-tools qt4-designer libqtgui4 libqtcore4 libqt4-xml libqt4-test libqt4-script libqt4-network libqt4-dbus python-qt4 python-qt4-gl libgle3 python-dev libssl-dev


# install pip and virtual environment and activate it
wget -qO- https://bootstrap.pypa.io/get-pip.py | sudo python
sudo pip install virtualenv
virtualenv -p /usr/local/bin/python $HOME/venv/scrapy1
#May be this line can be removed from file..not sure..need to update sometime in future
source $HOME/venv/scrapy1/bin/activate
# install required python packages in virtual env
$HOME/venv/scrapy1/bin/pip install scrapy peewee mysql-python pymysql python-dateutil


# now add git repo downlaod part

mkdir $HOME/project
cd $HOME/project
echo "enter git repository url to clone :- "
read url
read name
git clone $url $name
cd $name
git checkout master

#PyMongo
sudo pip install pymongo 
sudo apt-get install python-dev 
sudo pip install MySQL-python

#GooglePlacesAPI
sudo pip install python-google-places

#lxml
sudo apt-get install libxml2-dev libxslt1-dev zlib1g-dev
sudo pip install lxml

#BeautifulSoup4
sudo apt-get install python-bs4

#Marisa-Trie python Implementation
sudo pip install marisa-trie

#Google Client API - "Google text Search API"
sudo pip install --upgrade google-api-python-client

#numpy
sudo pip install numpy

#Dependencies for Master
sudo easy_install web.py
sudo pip install pymongo
sudo apt-get install python-bson
sudo pip install peewee
sudo pip install requests
sudo pip install pymysql
