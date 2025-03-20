# # Local connection
# import psycopg2
# import os
# from dotenv import load_dotenv
# # Get environment variables file(.env)
# load_dotenv()
# # Test on the PostgreSQL connection
# def get_db_connection():
#     return psycopg2.connect(
#         host=os.getenv("DB_HOST"),
#         database=os.getenv("DB_NAME"),
#         user=os.getenv("DB_USER"),
#         password=os.getenv("DB_PASSWORD"),
#         port=os.getenv("DB_PORT")
#     )

# Gould cloud SQL remote connection
# import psycopg2

# def get_db_connection():
#     conn = psycopg2.connect(
#         dbname="FIT5120IE",
#         user="postgres",
#         password="bche0078",
#         # Public IP from Cloud Instance
#         host="34.129.0.237",
#         port="5432"
#     )
#     return conn
import os
import psycopg2
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_db_connection():
    # Get database credentials from environment variables
    dbname = os.getenv('DB_NAME')
    user = os.getenv('DB_USER')
    password = os.getenv('DB_PASSWORD')
    connection_name = os.getenv('CLOUD_SQL_CONNECTION_NAME')

    # Connect using Cloud SQL instance socket
    conn = psycopg2.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=f'/cloudsql/{connection_name}',
    )
    return conn
