import mysql.connector
import mysql.connector.errors


def local():
    local_db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root123",
    database="newschema"
    )
    return local_db
