# linux login 
./mysql -uroot -p 
# windows login
mysql -u root -p admin

# create database
create database test;

# use database
use test;

# create user table
CREATE TABLE tablename(id INT(10) AUTO_INCREMENT PRIMARY_KEY, name VARCHAR(100), email VARCHAR(100), 
    username VARCHAR(100), password VARCHAR(100), register_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP) 

# create data table
CREATE TABLE articles(it INT(10) AUTO_INCREMENT PRIMARY_KEY, title VARCHAR(100), author VARCHAR(100),
    body TEXT, create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP) 

# grant privileges, replace password with the real password
GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' IDENTIFIED BY 'password' WITH GRANT OPTION;
FLUSH PRIVILEGES;

# show ports
SHOW VARIABLES WHERE Variable_name = 'port' ;

