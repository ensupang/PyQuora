from flask import Flask,render_template,request,redirect,url_for,session
import config
from models import User, Question, Comment
from exts import db
from decorators import login_required

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)

@app.route('/')
def index():
    context = {
        'questions' : Question.query.order_by('-create_time').all()
    }
    return render_template('index.html',**context)

@app.route('/login/', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        telephone = request.form.get('telephone')
        password = request.form.get('password')
        user = User.query.filter(User.telephone == telephone, User.password == password).first()
        if user:
            # setup cookie (don't need log in within 30 days)
            session['user_id'] = user.id
            session.permanent = True
            return redirect(url_for('index'))
        else:
            return 'Wrong phone number or username'

@app.route('/regist/',methods=['GET','POST'])
def regist():
    if request.method == 'GET':
        return render_template('regist.html')
    else:
        telephone = request.form.get('telephone')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        # Mobile number verification
        user = User.query.filter(User.telephone == telephone).first()
        if user:
            return 'Phone number alread existed'
        else:
            # password1 == password2?
            if password1 != password2:
                return 'wrong password'
            else:
                user = User(telephone = telephone, username = username, password = password1)
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('login'))

@app.route('/detail/<question_id>/')
def detail(question_id):
    question = Question.query.filter(Question.id == question_id).first()
    question
    return render_template('detail.html', question = question)

@app.route('/add_command/',methods=['POST'])
@login_required
def add_command():
    comment = request.form.get('comment')
    comment_object = Comment(content = comment)
    question_id = request.form.get('question_id')
    question = Question.query.filter(Question.id == question_id).first()
    user_id = session['user_id']
    user = User.query.filter(User.id == user_id).first()
    comment_object.author = user
    comment_object.question = question
    db.session.add(comment_object)
    db.session.commit()
    return redirect(url_for('detail', question_id = question_id))

@app.route('/question/',methods=['GET','POST'])
@login_required
def question():
    if request.method == 'GET':
        return render_template('question.html')
    else:
        title = request.form.get('title')
        content = request.form.get('content')
        user_id = session.get('user_id')
        question = Question(title = title, content = content)
        user = User.query.filter(User.id == user_id).first()
        question.author = user
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()
