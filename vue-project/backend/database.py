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

# Remote connection
import psycopg2

def get_db_connection():
    conn = psycopg2.connect(
        dbname="FIT5120IE",
        user="postgres",
        password="bche0078",
        # Public IP from Cloud Instance
        host="34.129.0.237",
        port="5432"
    )
    return conn
