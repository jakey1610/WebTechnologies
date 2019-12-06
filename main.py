from flask import Flask, render_template, request
import data

app = Flask(__name__)
@app.route('/', defaults={'user': 11})
@app.route('/<int:user>')
def main(user):
    #Initialising the user profile
    data.sortProfile(user)
    #Get the user profile
    books = data.getUP()
    ratings = data.getRatings()
    return render_template("index.html", books=books, ratings=ratings, userID=user)

@app.route('/addRating/<int:user>', methods=['POST'])
def addRating(user):
    #Initialising the user profile
    data.sortProfile(user)
    #Get the user profile
    books = data.getUP()
    ratings = data.getRatings()
    bookID = request.form['bookid']
    rating = request.form['rating']
    userID = user
    data.writeRating(userID,bookID,rating)
    return render_template("index.html", books=books, ratings=ratings, userID=user)



if __name__ == '__main__':
    app.run()
