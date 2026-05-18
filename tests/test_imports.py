def test_imports():
    import pandas as pd
    import pymysql
    import streamlit as st

    assert pd is not None
    assert pymysql is not None
    assert st is not None
