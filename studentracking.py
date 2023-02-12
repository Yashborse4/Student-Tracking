import mysql.connector


def insert_student_record( fullname, department_year, division, mobile_number):
    # connect to the database
    db = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="Yash@432005",
        database="studb"
    )

    # create a cursor to execute SQL queries
    cursor = db.cursor()

    # define the SQL query to insert a new record into the StudentTrack table
    sql = "INSERT INTO StudentTrack (FullName, Department_Year, Division, Mobile_Number) VALUES (%s, %s, %s,%s)"

    # create a tuple of values to insert
    values = (fullname, department_year, division, mobile_number)

    # execute the query and insert the values into the database
    cursor.execute(sql, values)

    # commit the changes to the database
    db.commit()

    # print the number of rows that were affected
    print(cursor.rowcount, "record inserted.")

    # close the cursor and database connection
    cursor.close()
    db.close()
