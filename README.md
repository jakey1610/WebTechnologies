# Online Book Recommendation System
#### Jake Mortimer - wtxd25
### Components
##### 1) Dataset
I have provided a dataset of books and ratings as specified in the coursework description. This is encoded in __JSON__. The user can leave ratings from the interface provided and this dynamically updates the dataset. In order to __create a new user__, one simply needs to add the URL parameter for the userID desired and leave a __rating__.
#### 2) User Profiling
Makes use of the __SVD Recommendation Algorithm__, specified below, and stores the books that the user may be interested in in a __user.json__ file.
#### 3) Recommendation Algorithm
Used SVD on a Matrix of __books against users__ with ratings per book as the values, as well as on a Matrix of __genres against users__ with average ratings per genre as values. This gives a more __accurate and extensive__ recommendation.
#### 4) Interface
Specified in the __How to run__ section in more detail.
### How to run
- Navigate to __~/../wtxd25_WT/__.
- Run the server on __localhost:5000__ by running the command __python3 main.py__.
- Go to your browser and enter URL __localhost:5000__.
- The default user is userID __11__. This can be changed using URL parameters; e.g __localhost:5000/1__ would show the page for userID __1__.
- This will show the __recommendations__ for each of the users.
- Recommendations are based on the __SVD Recommendation Algorithm__ and covers both similar __users__ and __genres__
- Depending on the page that you are on (which user __../<userID>__), the rating you leave will be for this particular user.
- To leave a __rating__ fill in the __form__ below the selection of books.
- When you leave a rating the page will be __reloaded__ with the rating you have given included.
- This may affect other users which can be seen by navigation around website, but will __not__ change the current users: I have made it so that the current user is __not involved in SVD Decomposition__.
