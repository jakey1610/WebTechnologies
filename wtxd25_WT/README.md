# Online Book Recommendation System
#### Jake Mortimer - wtxd25
### Components
##### 1) Dataset
I have provided a dataset of books and ratings as specified in the coursework description. This is encoded in __JSON__. The user can leave ratings from the interface provided and this dynamically updates the dataset. In order to __create a new user__, one simply needs to login as this user.
#### 2) User Profiling
Makes use of the __SVD Recommendation Algorithm__, specified below, and stores the books that the user may be interested in in a __user.json__ file.
#### 3) Recommendation Algorithm
Used SVD on a Matrix of __books against users__ with ratings per book as the values, as well as on a Matrix of __genres against users__ with average ratings per genre as values. This gives a more __accurate and extensive__ recommendation. Have also implemented some simple fixes to the __cold-start__ and __popularity bias__ problems.
#### 4) Interface
Specified in the __How to run__ section in more detail.
### How to run
- Navigate to __~/../wtxd25_WT/__.
- Run the server on __localhost:5000__ by running the command __python3 main.py__.
- Visit URL __localhost:5000__ in browser.
- You can login to the required user from the navbar. The most comprehensive at the moment is user __3__.
- This will show the __recommendations__ for each of the users.
- To leave a __rating__ fill in the __form__ below the selection of books and previous ratings.
- When you leave a rating the page will be __reloaded__ with the rating you have given included.
- Can also __edit__ or __delete__ ratings using the corresponding buttons on each of the displayed previous ratings.
- Depending on the __Accept-Language__ in the HTTP header; currently only English and Spanish supported, the __language of the page will change__.
