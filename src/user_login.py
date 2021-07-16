import flask_login
from flask_login import LoginManager, UserMixin

login_manager = LoginManager()


users = {'abhig.123':{'password': 'myp@33w0.rd'}}


class User(UserMixin):
    pass

@login_manager.user_loader
def user_loader(username):
    if username not in users:
        return
    user = User()
    user.id = username
    return user

@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    if username not in users:
        return
    user = User()
    user.id = username
    user.is_authenticated = request.form['password'] == users[username]['password']
    return user