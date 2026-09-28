import streamlit as st
import mysql.connector


def get_db_connection():

    # Streamlit Cloud / deployed environment
    if "mysql" in st.secrets:

        db = mysql.connector.connect(
            host=st.secrets["mysql"]["host"],
            port=int(st.secrets["mysql"].get("port", 3306)),
            user=st.secrets["mysql"]["user"],
            password=st.secrets["mysql"]["password"],
            database=st.secrets["mysql"]["database"]
        )

        return db

    # Local XAMPP / MySQL environment
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="diabetes_health"
    )

    return db


if __name__ == "__main__":

    try:

        db = get_db_connection()

        print("Database connected successfully!")

        db.close()

    except Exception as e:

        print("Database connection failed!")

        print(e)