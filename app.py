from flask import Flask, render_template, request, redirect, url_for  # <-- added redirect, url_for
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient("mongodb+srv://Abhishek:Abhi%4012345@student-report.i3gmep4.mongodb.net/?retryWrites=true&w=majority&appName=student-report")
db = client["School"]
students_collection = db["Students"]

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    roll = request.form['roll']
    subjects = request.form.getlist('subject')
    marks = request.form.getlist('marks')

    marks_dict = dict(zip(subjects, map(int, marks)))
    average = sum(marks_dict.values()) / len(marks_dict)

    if average >= 90:
        grade = 'A'
    elif average >= 80:
        grade = 'B'
    elif average >= 70:
        grade = 'C'
    else:
        grade = 'D'

    student_data = {
        'name': name,
        'roll': roll,
        'marks': marks_dict,
        'average': average,
        'grade': grade
    }

    students_collection.insert_one(student_data)
    return render_template("report.html", student=student_data)

@app.route('/students')
def view_all():
    all_students = list(students_collection.find())
    return render_template("students.html", students=all_students)

@app.route("/delete_all", methods=["POST"])
def delete_all():
    students_collection.delete_many({})  # use correct variable
    return redirect(url_for("index"))

if __name__ == '__main__':
    app.run(debug=True)
