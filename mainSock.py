from flask import Flask, render_template, request,redirect, url_for, flash
from flask_socketio import SocketIO
import data
import pyinotify

app = Flask(__name__)
app.secret_key = 'my unobvious secret key'
sio = SocketIO(app)
userRunning = 11
loggedIn = False
thread = None
@app.route('/')#, defaults={'user': 11})
# @app.route('/<int:user>')
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
        return render_template("index.html", async_mode=sio.async_mode, books=books, ratings=ratings, userID=userRunning, allBooks=allBooks,loggedIn=loggedIn)
    else:
        return render_template("index.html", async_mode=sio.async_mode, books=allBooks, ratings=ratings, userID=userRunning, allBooks=allBooks,loggedIn=loggedIn)

class ModHandler(pyinotify.ProcessEvent):
    def process_IN_ACCESS(self, evt):
        sio.emit('file updated')

def background_thread():
    handler = ModHandler()
    wm = pyinotify.WatchManager()
    notifier = pyinotify.Notifier(wm, handler)
    wm.add_watch('./', pyinotify.IN_ACCESS)
    notifier.loop()

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
    before = data.writeRating(userID,bookID,rating)
    if before:
        flash("Edited previous rating")
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

@sio.on('connect')
def test_connect():
    global thread
    if thread is None:
        thread = sio.start_background_task(target=background_thread)

if __name__ == '__main__':
    sio.run(app)


# <!-- <script type="text/javascript" src="//cdnjs.cloudflare.com/ajax/libs/socket.io/1.3.6/socket.io.min.js"></script>
# <script type="text/javascript" charset="utf-8">
# var socket = io.connect('http://' + document.domain + ':' + location.port);
# socket.on('connect', function() {
#     socket.emit('my event', {data: 'I\'m connected!'});
# });
# socket.on('file updated', function(data) {
#     console.log('the file has been updated');
# });
#
# </script> -->
