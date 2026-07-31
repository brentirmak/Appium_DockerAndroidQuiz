import os

import mysql.connector
from mysql.connector.constants import ClientFlag
import time

import pytz
from datetime import datetime, timedelta
from pytz import timezone
from dotenv import load_dotenv

# 1. Load the environment variables from the .env file
load_dotenv()

# 2. Retrieve the secrets using os.getenv()
mysql_url = os.getenv("MYSQL_URL")
mysql_username = os.getenv("MYSQL_USERNAME")
mysql_password = os.getenv("MYSQL_PASSWORD")

# File to store overall Appium Test information locally - also used for DB storing purposes
if "var/lib/jenkins/workspace" in os.getcwd():
    print("We are running script from Jenkins server - path needs to be changed")
    results_log = os.getcwd() + '/Appium_DockerAndroidQuiz.txt'
    print("Results Log Path (per script): ", results_log)
    print("Path for results file has been set")
else:
    print("We are running script from development VM")
    results_log = '/home/brent-ubuntu-26-04/AppiumProjects/Appium_DockerAndroidQuiz/Appium_DockerAndroidQuiz.txt'
    print("Results Log Path (per script): ", results_log)
    print("Path for results file has been set")

print("Connecting to MySQL...")

try:
    config = {
        'user': mysql_username,
        'password': mysql_password,
        'host': mysql_url,
        'database': 'appium',
    }
    cnx = mysql.connector.connect(**config)
except Exception as f:
    print(f)
    print("Was not ale to connect to MYSQL - will sleep and try again")
    time.sleep(10)

    config = {
        'user': mysql_username,
        'password': mysql_password,
        'host': mysql_url,
        'database': 'appium',
    }
    cnx = mysql.connector.connect(**config)

cursor = cnx.cursor()

current_timestamp = datetime.now(pytz.timezone('America/Los_Angeles'))

# 2024-06-10 13:21:28.767966-07:00
print("Current time: ", current_timestamp)
print("")

print("Opening file to post to Credence ...")

text_file = open(results_log, "r")
lines = text_file.readlines()

Answer_Question_trx_time = 'NULL'

for line in lines:
    trx_name, trx_status, trx_duration, run_type = line.split(",")

    if trx_name == 'Answer_Question':
        Answer_Question_trx_time = trx_duration[:5]
        Answer_Question_trx_status = trx_status

print("Inserting results into database ...")

cursor.execute(
    """INSERT INTO appium_docker_android_quiz(RunTimeStamp, RunType, AnswerQuestion)
                  values (%s, %s, %s)""",
    (current_timestamp, run_type, Answer_Question_trx_time))

cnx.commit()
cursor.close()

cnx.close()
text_file.close()