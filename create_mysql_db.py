#!/usr/bin/python
# -*- coding: UTF-8 -*-

import MySQLdb


db = MySQLdb.connect("localhost", "root", "password", "scraping")
cursor = db.cursor()
# cursor.execute("DROP TABLE IF EXISTS EMPLOYEE")

sql = """
CREATE TABLE website (
  guid CHAR(32) PRIMARY KEY,
  title_name TEXT,
  link_address TEXT,
  updated DATETIME) DEFAULT CHARSET=utf8;
  """

cursor.execute(sql)
db.close()