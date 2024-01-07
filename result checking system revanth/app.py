from flask import Flask, render_template, request, redirect, url_for, session,jsonify
from pymongo import MongoClient

client = MongoClient('mongodb+srv://revanth200319:Nagasai20032104@cluster0.zrtypbn.mongodb.net/')
app = Flask(__name__)
app.secret_key = '99009'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/loginfaculty')
def facultylogin():
    return render_template('faculty_login.html')

@app.route('/login')
def login():
    return render_template('student_login.html')

@app.route('/feedback')
def feedbackform():
    return render_template('feedback.html')

@app.route('/login_verify',methods=['post'])
def verify():
    name=request.form['uname']
    pas=request.form['psw']
    doc=client['student']['data']
    data=doc.find()
    for i in data:
        if i['username']==name and i['password']==pas:
            session['u']=name
            session['w']='owner'
            student_details = doc.find_one({'username': name})
            print(student_details)
            # Return the rendered template with the student details
            return render_template('student_page.html', student_details=student_details)

    return render_template('student_login.html',res='invalid user or password')


@app.route('/facultyverify',methods=['post'])
def facultyverify():
    name=request.form['uname']
    pas=request.form['psw']
    doc=client['student']['teachers']
    data=doc.find()
    for i in data:
        if i['username']==name and i['password']==pas:
            session['u']=name
            session['w']='owner' 
            # Retrieve student details from the database
            teacher_details = doc.find_one({'username': name})

            # Return the rendered template with the student details
            return render_template('faculty_main_page.html', teacher_details=teacher_details)
    return render_template('faculty_login.html',res='invalid user or password')

@app.route('/studentdata')
def studentdetails():
    db = client['student']
    collection = db['data']
    username=request.form['username']
    # Retrieve student details from the database
    student_details = collection.find_one({'username': 'username'})

    # Return the rendered template with the student details
    return render_template('student_page.html', student_details=student_details)

@app.route('/teacherdata')
def teacherdetails():
    db = client['student']
    collection = db['teachers']
    username=request.form['username']
    # Retrieve student details from the database
    teacher_details = collection.find_one({'username': 'username'})

    # Return the rendered template with the student details
    return render_template('faculty_main_page.html', teacher_details=teacher_details)

@app.route('/check_results', methods=['POST'])
def check_results():
    db = client['student']
    collection = db['result']

    username = request.form['username']
    subject = request.form['subject']

    result_data = collection.find_one({'username': username, 'subject': subject})

    # Return the rendered template with the result data
    return render_template('result.html', result_data=result_data)

@app.route('/add_marks', methods=['GET', 'POST'])
def add_marks():
    if request.method == 'POST':
        db = client['student']
        collection = db['addmarks']
        username = request.form['username']
        subject = request.form['subject']
        marks = request.form['marks']
        overallresult = request.form['overallresult']
        data = {'username': username, 'subject': subject, 'marks': marks, 'overallresult': overallresult}
    
        collection.insert_one(data)
        return render_template('success.html')
    return render_template('enter_student_marks.html')

@app.route('/back')
def returnpage():
    if request.method == 'POST':
        db = client['student']
        collection = db['addmarks']
        username = request.form['username']
        subject = request.form['subject']
        marks = request.form['marks']
        overallresult = request.form['overallresult']
        data = {'username': username, 'subject': subject, 'marks': marks, 'overallresult': overallresult}
    
        collection.insert_one(data)
        return render_template('success.html')
    return render_template('enter_student_marks.html')

if __name__ == '__main__':
    app.run(debug=True)
