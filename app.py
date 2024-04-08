from flask import Flask,url_for,request,render_template,abort,redirect,session
from markupsafe import escape
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)

@app.route('/')
def start():
    return 'Index Page'

@app.route('/hello')
def hello():
    return 'Hello, World'

@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return f'User {escape(username)}'

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return f'Post {post_id}'

@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    # show the subpath after /path/
    return f'Subpath {escape(subpath)}'

@app.route('/projects/')
def projects():
    return 'The project page'

@app.route('/about')
def about():
    return 'The about page'

@app.route('/')
def index():
    return 'index'

@app.route('/login')
def login():
    return 'login'

@app.route('/user/<username>')
def profile(username):
    return f'{username}\'s profile'

with app.test_request_context():
    print(url_for('index'))
    print(url_for('login'))
    print(url_for('login', next='/'))
    print(url_for('profile', username='John Doe'))

    #@app.route('/login', methods=['GET', 'POST'])
   # def login():
      #  if request.method == 'POST':0
         #   return do_the_login()
     #   else:
         #   return show_the_login_form()
    
    url_for('static', filename='style.css')

    @app.route('/hello/')
    @app.route('/hello/<name>')
    def template(name=None):
        return render_template('hello.html', name=name)

with app.test_request_context('/hello', method='POST'):
    # now you can do something with the request until the
    # end of the with block, such as basic assertions:
    assert request.path == '/hello'
    assert request.method == 'POST'

    @app.route('/login', methods=['POST', 'GET'])
    def fileupload():
        error = None
        if request.method == 'POST':
            if valid_login(request.form['username'],
            request.form['password']):
                return log_the_user_in(request.form['username'])
            else:
                error = 'Invalid username/password'
    # the code below is executed if the request method
    # was GET or the credentials were invalid
        return render_template('login.html', error=error)

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['the_file']
        f.save('/var/www/uploads/uploaded_file.txt')

    @app.route('/')
    def cookie():
         username = request.cookies.get('username')
    # use cookies.get(key) instead of cookies[key] to not get a
    # KeyError if the cookie is missing.

@app.route('/')
def redirect():
    return redirect(url_for('login'))

@app.route('/login')
def error():
    abort(401)
    this_is_never_executed()

@app.errorhandler(404)
def not_found(error):
    return render_template('error.html'), 404

@app.route("/me")
def me_api():
    user = get_current_user()
    return {
        "username": user.username,
        "theme": user.theme,
        "image": url_for("user_image", filename=user.image),
    }

@app.route("/users")
def users_api():
    users = get_all_users()
    return [user.to_json() for user in users]

# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/')
def session1():
    if 'username' in session:
        return f'Logged in as {session["username"]}'
    return 'You are not logged in'

@app.route('/login', methods=['GET', 'POST'])
def session2():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    return '''
        <form method="post">
            <p><input type=text name=username>
            <p><input type=submit value=Login>
        </form>
    '''

@app.route('/logout')
def session3():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))
