#!/usr/bin/python
# -*- coding: UTF-8 -*-

import MySQLdb


db = MySQLdb.connect("localhost", "root", "password", "scraping")
cursor = db.cursor()
# cursor.execute("DROP TABLE IF EXISTS EMPLOYEE")

sql = """
CREATE TABLE netbian_info (
  title_name char(32) NOT NULL,
  link_address char(100))
  """

cursor.execute(sql)
db.close()