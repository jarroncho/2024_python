from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

# 定義 Student 模型
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    chinese = db.Column(db.Integer, nullable=False)
    english = db.Column(db.Integer, nullable=False)
    math = db.Column(db.Integer, nullable=False)
    physics = db.Column(db.Integer, nullable=False)

# 建立資料庫表格
with app.app_context():
    db.create_all()

# 主頁：顯示所有學生的成績
@app.route('/')
def index():
    students = Student.query.all()
    return render_template('index.html', students=students)

# 新建或更新學生資料
@app.route('/update', methods=['GET', 'POST'])
def update_student():
    if request.method == 'POST':
        name = request.form['name']
        chinese = int(request.form['chinese'])
        english = int(request.form['english'])
        math = int(request.form['math'])
        physics = int(request.form['physics'])

        student = Student.query.filter_by(name=name).first()
        if student:
            # 更新資料
            student.chinese = chinese
            student.english = english
            student.math = math
            student.physics = physics
        else:
            # 新建資料
            student = Student(name=name, chinese=chinese, english=english, math=math, physics=physics)
            db.session.add(student)

        db.session.commit()
        return redirect(url_for('index'))

    return render_template('update_student.html')

if __name__ == '__main__':
    app.run(debug=True)
