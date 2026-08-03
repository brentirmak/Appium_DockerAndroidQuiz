import os
import time
from datetime import datetime

import mysql.connector
import pytz
from dotenv import load_dotenv


# ============================================================
# Load environment variables
# ============================================================

load_dotenv()


# ============================================================
# MySQL configuration
#
# These values come from Jenkins environment variables:
#
# MYSQL_HOST=10.0.0.164
# MYSQL_PORT=3306
# MYSQL_USERNAME=your_username
# MYSQL_PASSWORD=your_password
# ============================================================

mysql_host = os.getenv("MYSQL_HOST", "10.0.0.164")
mysql_port = int(os.getenv("MYSQL_PORT", "3306"))
mysql_username = os.getenv("MYSQL_USERNAME")
mysql_password = os.getenv("MYSQL_PASSWORD")
mysql_database = os.getenv("MYSQL_DATABASE", "appium")


# ============================================================
# Results log path
# ============================================================

if "var/lib/jenkins/workspace" in os.getcwd():

    print("We are running script from Jenkins server")
    results_log = os.path.join(
        os.getcwd(),
        "Appium_DockerAndroidQuiz.txt"
    )

    print("Results Log Path (per script):", results_log)
    print("Path for results file has been set")

else:

    print("We are running script from development VM")

    results_log = (
        "/home/brent-ubuntu-26-04/"
        "AppiumProjects/Appium_DockerAndroidQuiz/"
        "Appium_DockerAndroidQuiz.txt"
    )

    print("Results Log Path (per script):", results_log)
    print("Path for results file has been set")


# ============================================================
# Verify MySQL configuration
# ============================================================

print("==========================================")
print("MySQL Configuration")
print("==========================================")
print("MYSQL_HOST =", mysql_host)
print("MYSQL_PORT =", mysql_port)
print("MYSQL_USERNAME =", mysql_username)
print("MYSQL_DATABASE =", mysql_database)
print("==========================================")


# ============================================================
# Validate required credentials
# ============================================================

if not mysql_username:
    raise RuntimeError(
        "MYSQL_USERNAME environment variable is not set."
    )

if not mysql_password:
    raise RuntimeError(
        "MYSQL_PASSWORD environment variable is not set."
    )


# ============================================================
# Connect to MySQL
# ============================================================

print("Connecting to MySQL...")

config = {
    "user": mysql_username,
    "password": mysql_password,
    "host": mysql_host,
    "port": mysql_port,
    "database": mysql_database,
}


try:

    cnx = mysql.connector.connect(**config)

    print(
        f"MySQL connection established to "
        f"{mysql_host}:{mysql_port}"
    )

except Exception as first_error:

    print("==========================================")
    print("MySQL connection failed")
    print("==========================================")
    print(first_error)
    print("Will sleep for 10 seconds and retry...")
    print("==========================================")

    time.sleep(10)

    try:

        cnx = mysql.connector.connect(**config)

        print(
            f"MySQL connection established after retry "
            f"to {mysql_host}:{mysql_port}"
        )

    except Exception as second_error:

        print("==========================================")
        print("MySQL connection failed after retry")
        print("==========================================")
        print(second_error)
        print("==========================================")

        raise


# ============================================================
# Create cursor
# ============================================================

cursor = cnx.cursor()


# ============================================================
# Current timestamp
# ============================================================

current_timestamp = datetime.now(
    pytz.timezone("America/Los_Angeles")
)

print("Current time:", current_timestamp)
print("")


# ============================================================
# Open Appium results file
# ============================================================

print("Opening file to post to Credence ...")

if not os.path.isfile(results_log):

    print("ERROR: Results file does not exist:")
    print(results_log)

    cursor.close()
    cnx.close()

    raise FileNotFoundError(results_log)


with open(results_log, "r") as text_file:

    lines = text_file.readlines()


# ============================================================
# Parse transaction results
# ============================================================

Answer_Question_trx_time = "NULL"
Answer_Question_trx_status = "NULL"
run_type = "UNKNOWN"


for line in lines:

    line = line.strip()

    if not line:
        continue

    parts = line.split(",")

    if len(parts) != 4:
        print("Skipping malformed results line:")
        print(line)
        continue

    trx_name, trx_status, trx_duration, current_run_type = parts

    run_type = current_run_type

    if trx_name == "Answer_Question":

        Answer_Question_trx_time = trx_duration[:5]
        Answer_Question_trx_status = trx_status


# ============================================================
# Insert results into MySQL
# ============================================================

print("Inserting results into database ...")

cursor.execute(
    """
    INSERT INTO appium_docker_android_quiz
        (RunTimeStamp, RunType, AnswerQuestion)
    VALUES
        (%s, %s, %s)
    """,
    (
        current_timestamp,
        run_type,
        Answer_Question_trx_time,
    ),
)

cnx.commit()

print("Results successfully inserted into MySQL.")


# ============================================================
# Close database connection
# ============================================================

cursor.close()
cnx.close()

print("MySQL connection closed.")