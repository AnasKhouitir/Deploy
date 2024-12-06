from flask import Flask, request, jsonify
import pyodbc
from waitress import serve

app = Flask(__name__)

# Configuration de la connexion à la base de données
server = 'studentsdb.database.windows.net'
database = 'StudentsDB'
username = 'anas'
password = 'azerty12345@'
driver = '{ODBC Driver 18 for SQL Server}'

def get_db_connection():
    conn = pyodbc.connect(
        f'DRIVER={driver};SERVER={server};PORT=1433;DATABASE={database};UID={username};PWD={password};TrustServerCertificate=yes'
    )
    return conn

# API GET : Récupérer tous les étudiants
@app.route('/students', methods=['GET'])
def get_students():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Students')
    rows = cursor.fetchall()
    students = [
        {
            "StudentID": row[0],
            "Name": row[1],
            "Age": row[2],
            "Gender": row[3],
            "GPA": row[4],
            "Course": row[5],
            "EnrollmentDate": row[6]
        }
        for row in rows
    ]
    cursor.close()
    conn.close()
    return jsonify(students)

# API POST : Ajouter un étudiant
@app.route('/students', methods=['POST'])
def add_student():
    data = request.json
    student_id = data['StudentID']
    name = data['Name']
    age = data['Age']
    gender = data['Gender']
    gpa = data['GPA']
    course = data['Course']
    enrollment_date = data['EnrollmentDate']
    
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO Students (StudentID, Name, Age, Gender, GPA, Course, EnrollmentDate)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', 
        student_id, name, age, gender, gpa, course, enrollment_date)
        conn.commit()
        response = {"message": "Student added successfully!"}
    except Exception as e:
        response = {"error": str(e)}
    finally:
        cursor.close()
        conn.close()
    return jsonify(response)

if __name__ == '__main__':
    app.run()
