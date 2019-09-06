#!/usr/bin/python

from drivers import mysql

db = mysql.Database()

db.connect("localhost", "powermon", "powermongem", "powermon")

#db.execute('''CREATE TABLE IF NOT EXISTS device_types ( 
#id  int(11) NOT NULL AUTO_INCREMENT,
#name varchar(50),
#PRIMARY KEY (id))''')

#db.execute("INSERT INTO device_types (name) VALUES ('GEM')")

#db.execute('''CREATE TABLE IF NOT EXISTS devices (
#id int(11) NOT NULL AUTO_INCREMENT,
#name varchar(50),
#serial varchar(50),
#PRIMARY KEY (id))''')

#db.execute('''CREATE TABLE IF NOT EXISTS channels (
#id int(11) NOT NULL AUTO_INCREMENT,
#name varchar(50),
#device_id int(11) NOT NULL,
#channel_num int(11) NOT NULL,
#PRIMARY KEY (id))''')
#
#db.execute('''CREATE TABLE IF NOT EXISTS circuits (
#id int(11) NOT NULL AUTO_INCREMENT,
#name varchar(50),
#capacity int(11),
#channel_id int(11) NOT NULL,
#PRIMARY KEY (id))''')

#db.execute('''CREATE TABLE IF NOT EXISTS channel_packets (
#id int(11) NOT NULL AUTO_INCREMENT,
#channel_id int(11) NOT NULL,
#voltage SMALLINT(11) NOT NULL,
#seconds MEDIUMINT(11) NOT NULL,
#wattsec BIGINT(11) NOT NULL,
#datetime DATETIME NOT NULL,
#PRIMARY KEY (id))''')

db.execute('''CREATE TABLE IF NOT EXISTS aggregate_by_minute (
id int(11) NOT NULL AUTO_INCREMENT,
datetime DATETIME NOT NULL,
wattsec BIGINT(11) NOT NULL,
PRIMARY KEY (id))''')

db.execute('''CREATE TABLE IF NOT EXISTS aggregate_status (
id int(11) NOT NULL AUTO_INCREMENT,
datetime DATETIME,
channel_id INT(11) NOT NULL,
PRIMARY KEY (id))''')
