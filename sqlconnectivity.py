import mysql.connector


def get_student_details(imagename):
    # Connect to the MySQL database
    conn = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="Yash@432005",
        database="studb"
    )

    # Create a cursor to interact with the database
    cursor = conn.cursor()
    parts = imagename.split(".")
    first_name = parts[0].split(" ")[0]
    last_name = parts[0].split(" ")[1]


    # Remove spaces from the first name and last name
    first_name = first_name.replace(" ", "")
    last_name = last_name.replace(" ", "")

    # Execute a SELECT statement to retrieve information from the StudentDetail table
    cursor.execute("SELECT Stud_Id, First_Name, Middle_Name, Last_Name, Department_Year, Division, Mobile_Number, Address FROM StudentDetail WHERE First_Name = %s AND Last_Name = %s", (first_name, last_name))

    # Fetch the results
    results = cursor.fetchall()
    # Close the cursor and the connection
    cursor.close()
    conn.close()

    return results
