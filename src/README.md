# Clio

## Local Installation

### Dependencies to run Clio

*Please refer to `software-components.rst` to know the various software components used in clio*
* Python 3
* MySQL

For Debian-based Linux users
```
$ sudo apt-get install mysql-server
```

### Steps

Make sure you have the dependencies mentioned above before proceeding further.

* **Step 0** - Clone the Clio repository and `cd` into the directory
```
$ git clone https://github.com/eellak/clio.git
$ cd clio/src/
```

* **Step 1** - Install python3 requirements. You need to be present in the root of the project.
```
$ sudo -H pip3 install -r requirements.txt
```
Hint : You may need to upgrade your pip version and install the following packages if you encounter errors while installing the requirements.

* **Step 2** - Create the database. For that we will first open the MySQL shell.
```
$ sudo mysql -u username -p

mysql> CREATE DATABASE clio;

mysql> exit
```
Update the `SQLALCHEMY_DATABASE_URI` in `config.py`  

* **Step 3** - Create the tables.
```
$ python3 manage.py db init
$ python3 manage.py db migrate
$ python3 manage.py db upgrade
```

* **Step 4** - Start the application along with the needed services.
```
# To run
$ python3 app.py
```

* **Step 5** - Go to `localhost:5000` in your web browser to see the application live.
