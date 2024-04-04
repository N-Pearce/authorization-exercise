from flask import Flask, flash, session, redirect, render_template
from models import db, connect_db, User, Feedback
from forms import RegisterUserForm, LoginUserForm, FeedbackForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///practice_authorize_users'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'pwab'

connect_db(app)

with app.app_context():
    db.create_all()

@app.route('/')
def to_register():
    return redirect('/register')

@app.route('/register', methods = ['GET', 'POST'])
def new_user_form():
    form = RegisterUserForm()

    if form.validate_on_submit():
        username = form.username.data
        password = User.hash_password(form.password.data)
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        new_user = User(
            username=username,
            password=password,
            email=email,
            first_name=first_name,
            last_name=last_name
        )
        
        db.session.add(new_user)
        db.session.commit()

        session['user_id'] = username
        return redirect('/secret')
    else:
        return render_template('register.html', form=form)
    
@app.route('/users/<username>')
def show_secret(username):
    if 'user_id' in session:
        if username == session['user_id']:
            user = User.query.get_or_404(session['user_id'])  
            feedbacks = Feedback.query.filter(Feedback.username == user.username)      
            return render_template('secret.html', user=user, feedbacks=feedbacks)
        else:
            username = session['user_id']
            return redirect(f'/users/{username}')
    else:
        return redirect('/register')

@app.route('/logout')
def logout():
    session.pop('user_id')
    return redirect('/')

@app.route('/login', methods = ['GET', 'POST'])
def login_prev_user():
    form = LoginUserForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)
        if user:   
            session['user_id'] = username
            return redirect(f'/users/{username}')
        else:
            flash('incorrect username or password')
            return render_template('login.html', form=form)
    else:
        return render_template('login.html', form=form)
    
# Start of Feedback

@app.route('/users/<username>/feedback/add', methods=['GET', 'POST'])
def new_feedback_form(username):
    if 'user_id' in session:
        if username == session['user_id']:
            form = FeedbackForm()

            if form.validate_on_submit():
                title = form.title.data
                content = form.content.data

                new_feedback = Feedback(
                    title=title,
                    content=content,
                    username=username,
                )
                
                db.session.add(new_feedback)
                db.session.commit()

                user = User.query.get_or_404(username)
                return redirect(f'/users/{username}')
            else:
                return render_template('feedback.html', form=form, action='add')
        else:
            username = session['user_id']
            return redirect(f'/users/{username}/feedback/add')
    else:
        return redirect('/register')
    
@app.route('/feedback/<int:feedback_id>/delete', methods=['POST'])
def delete_feedback(feedback_id):
    username = session['user_id']
    feedback = Feedback.query.get_or_404(feedback_id)
    db.session.delete(feedback)
    db.session.commit()
    return redirect(f'/users/{username}')

@app.route('/feedback/<int:feedback_id>/update', methods=['GET', 'POST'])
def update_feedback(feedback_id):
    feedback = Feedback.query.get_or_404(feedback_id)
    if session['user_id'] == feedback.username:
        form = FeedbackForm(obj=feedback)

        if form.validate_on_submit():
                feedback.title = form.title.data
                feedback.content = form.content.data
                
                db.session.add(feedback)
                db.session.commit()

                user = User.query.get_or_404(session['user_id'])
                return redirect(f'/users/{user}')
        else:
            return render_template('feedback.html', form=form, action='update')
    else:
        return redirect(f'/users/{session["user_id"]}')