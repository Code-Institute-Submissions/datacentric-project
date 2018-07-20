import os
import pymysql
# from flask import Flask, render_template, redirect, request, url_for

username = os.getenv('C9_USER')

connection = pymysql.connect(host='localhost',
                            user=username,
                            password='',
                            db='project_db')

try:
    with connection.cursor() as cursor:
        cursor.execute("""CREATE TABLE
                        Test2(name VARCHAR(50), brand VARCHAR(20), size VARCHAR(4), 
                        colour VARCHAR(10), gender VARCHAR(6), desc VARCHAR(100), 
                        price int, contact VARCHAR(50));""")
finally:
    connection.close()