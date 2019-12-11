from flask import Flask, render_template,request,redirect, url_for, flash
from flask_babel import Babel,_
import data

app = Flask(__name__)
app.secret_key = 'my unobvious secret key'
app.config['BABEL_TRANSLATION_DIRECTORIES'] = "./translations"
babel = Babel(app)
LANGUAGES = ['en','es']
userRunning = 11
loggedIn = False

@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(LANGUAGES)
    # return 'es'


@app.route('/')
def main():
    global userRunning
    global loggedIn
    #Initialising the user profile
    data.sortProfile(userRunning)
    #Get the user profile
    books = data.getUP()
    allBooks = data.getBooks()
    ratings = data.getRatings()
    if loggedIn:
        return render_template("index.html", books=books, ratings=ratings, userID=userRunning, allBooks=allBooks,loggedIn=loggedIn)
    else:
        return render_template("index.html", books=allBooks, ratings=ratings, userID=userRunning, allBooks=allBooks,loggedIn=loggedIn)


@app.route('/addRating/<int:user>', methods=['POST'])
def addRating(user):
    #Initialising the user profile
    data.sortProfile(user)
    #Get the user profile
    books = data.getUP()
    ratings = data.getRatings()
    bookID = request.form['bookID']
    rating = request.form['rating']
    userID = user
    data.writeRating(userID,bookID,rating)
    return redirect(url_for('main'))

@app.route('/login', methods=['POST'])
def login():
    global userRunning
    global loggedIn
    loggedIn = True
    user = request.form['username']
    userRunning = int(user)
    return redirect(url_for('main'))

@app.route('/logout', methods=['POST'])
def logout():
    global loggedIn
    loggedIn = False
    return redirect(url_for('main'))

@app.route('/deleteRating/<int:bookID>', methods=['POST'])
def removeRating(bookID):
    global userRunning
    data.deleteRating(userRunning,bookID)
    return redirect(url_for('main'))


if __name__ == '__main__':
    app.run()
