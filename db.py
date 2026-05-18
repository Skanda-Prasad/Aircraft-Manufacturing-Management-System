import os
import pymysql
import pandas as pd
import streamlit as st

_conn = None


def get_connection():
    global _conn
    if _conn:
        return _conn
    host = os.getenv("DB_HOST", "localhost")
    user = os.getenv("DB_USER", "dbms")
    password = os.getenv("DB_PASSWORD", "1234")
    database = os.getenv("DB_NAME", "dbms_project")
    _conn = pymysql.connect(host=host, user=user, password=password, database=database, cursorclass=pymysql.cursors.DictCursor)
    return _conn


def execute_query(query, data=None, fetch=True):
    conn = get_connection()
    with conn.cursor() as cursor:
        try:
            if data:
                cursor.execute(query, data)
            else:
                cursor.execute(query)
            conn.commit()
            if fetch:
                rows = cursor.fetchall()
                try:
                    df = pd.DataFrame(rows)
                except Exception:
                    df = pd.DataFrame(rows)
                return df
            return pd.DataFrame()
        except Exception as e:
            st.error(f"DB Error: {e}")
            conn.rollback()
            return pd.DataFrame()


def close_connection():
    global _conn
    try:
        if _conn:
            _conn.close()
    except Exception:
        pass