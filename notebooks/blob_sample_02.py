# https://www.geeksforgeeks.org/storing-a-blob-in-a-postgresql-database-using-python/

import psycopg2
from config import config

conn = None
try:
    # connect to the PostgreSQL server
    conn = psycopg2.connect(**config)

    # Creating a cursor with name cur.
    cur = conn.cursor()

    # SQL query to insert data into the database.
    # open('File,'rb').read() is used to read the file.
    # where open(File,'rb').read() will return
    # the binary data of the file.
    # psycopg2.Binary(File_in_Bytes) is used to
    # convert the binary data to a BLOB data type.
    BLOB_vdo = psycopg2.Binary(
        open('files\cartoon.mp4', 'rb').read())
    BLOB_pdf = psycopg2.Binary(
        open('files\BlobNotes.pdf', 'rb').read())

    cur.execute('INSERT INTO blob_datastore(s_no,file_name,\
    blob_data) VALUES (%s,%s,%s);',
                (1, 'cartoon.mp4', BLOB_vdo))
    cur.execute('INSERT INTO blob_datastore(s_no,file_name,\
blob_data) VALUES (%s,%s,%s);',
                (2, 'BlobNotes.pdf', BLOB_pdf))

# close the cursor
cur.close()

except(Exception, psycopg2.DatabaseError) as error:
print(error)
finally:
if conn is not None:
    # Commit the changes to the database
    conn.commit()
