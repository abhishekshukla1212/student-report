from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
students = []

class Student:
    def __init__(self, name, roll):
        self.name = name
        self.roll = roll
        self.marks = {}

    def add_mark(self, subject, mark):
        self.marks[subject] = int(mark)

    def calculate_average(self):
        return sum(self.marks.values()) / len(self.marks) if self.marks else 0

    def get_grade(self):
        avg = self.calculate_average()
        if avg >= 90:
            return 'A'
        elif avg >= 80:
            return 'B'
        elif avg >= 70:
            return 'C'
        else:
            return 'D'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        roll = request.form['roll']
        subject = request.form['subject']
        mark = request.form['mark']

        # Check if student exists
        student = next((s for s in students if s.roll == roll), None)
        if not student:
            student = Student(name, roll)
            students.append(student)

        student.add_mark(subject, mark)
        return redirect(url_for('report', roll=roll))
    return render_template('index.html')

@app.route('/report/<roll>')
def report(roll):
    student = next((s for s in students if s.roll == roll), None)
    if not student:
        return "Student not found", 404

    average = student.calculate_average()
    grade = student.get_grade()
    return render_template('report.html', student=student, average=average, grade=grade)

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

