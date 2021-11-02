from flask import Flask, render_template, request, redirect, flash, url_for
import sqlite3
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
login_manager = LoginManager(app)
login_manager.login_view = "login"
class User(UserMixin):
	def __init__(self, id, email, password):
		self.id = str(id)
		self.email = email
		self.password = password
		self.authenticated = False
	def is_active(self):
		return self.is_active()
	def is_anonymous(self):
		return False
	def is_authenticated(self):
		return self.authenticated
	def is_active(self):
		return True
	def get_id(self):
		return self.id
	def get_name(self):
		return self.email
  
@login_manager.user_loader
def loader(user_id):
	database = sqlite3.connect('mydatabase.db')
	cursor=database.cursor()
	cursor.execute("SELECT * from users where id = (?)",[user_id])
	user = cursor.fetchone()
	if user is None:
		return None
	else:
		return User(int(user[0]), user[1], user[2])




@app.route("/")
def index():
	loggedin=0
	if current_user.is_authenticated:
		loggedin = 1 
		return render_template('index.html', isLogged= loggedin, user=current_user.get_name())
	return render_template('index.html', isLogged= loggedin)

@app.route("/about")
def about():
	loggedin=0
	if current_user.is_authenticated:
		loggedin = 1
	return render_template('about.html', isLogged= loggedin)

@app.route("/content")
def content(nome = None, search = None):
	if current_user.is_authenticated:
		return render_template('knowledgebase.html', isLogged = 1,  nome = nome, search = search)
	return redirect ('login')

@app.route("/login", methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect('/')
	if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
		username= request.form['username']
		password = request.form['password']
		database = sqlite3.connect('mydatabase.db')
		cursor=database.cursor()
		cursor = cursor.execute(f"Select * from users where username = '{username}' and password = '{password}'")
		account = cursor.fetchone()
		if account != None:
			user = loader(account[0])
			login_user(user, force=True)
			flash('Logged in Successfully')	
			return redirect('/')
			
	return render_template('login.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
	if request.method == 'POST' and 'username2' in request.form and 'password2' in request.form and 'password3' in request.form:
		if request.form['password2'] != request.form['password3'] :
			flash("Passwords don't match!")
			return redirect('login')
	database = sqlite3.connect('mydatabase.db')
	cursor=database.cursor()
	username, password= request.form['username2'], request.form['password2']
	cursor = cursor.execute(f"Select id from users where username = '{username}'")
	test = cursor.fetchall()
	if test :
		flash("Username already exists!")
		return redirect('login')
	cursor = cursor.execute(f"Insert into users ('username', 'password') values('{username}','{password}')")
	database.commit()
	flash('Registered Successfully! You may now login')	
	return redirect('/login')
	
@app.route("/cartas/<champion>")
def cartas(champion):
	database = sqlite3.connect('mydatabase.db')
	cursor=database.cursor()
	execute = cursor.execute(f"Select * from champions where name = '{champion}'")
	result = execute.fetchall()
	return render_template('cartas.html',champion=result)




@app.route("/nome/<abc>")
def mostrar_nome(abc):
	database = sqlite3.connect('mydatabase.db')
	cursor=database.cursor()
	aaaaaa = cursor.execute(f"Select * from chars where nome = '{abc}'")
	result = aaaaaa.fetchall()
	return render_template('nome.html',nome=result)

@app.route("/logout")
@login_required
def logout():
	logout_user()
	flash('Logged out sucessefully')
	return redirect("/")

@app.route("/search", methods=['GET', 'POST'])
@login_required
def search():
	if request.method == "POST":
		query = request.form["query"]
		if query:
			database = sqlite3.connect('mydatabase.db')
			cursor = database.cursor()
			cartas = cursor.execute(f"SELECT Name FROM champions WHERE Name LIKE '%{query}%'")
			result = cartas.fetchall()
			return render_template('knowledgebase.html', nome=result, search = 1)
	return redirect(url_for("content"))

if __name__ == '__main__':
	app.run(debug=True)

