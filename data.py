import numpy as np
import pandas as pd
import json
import math

def getBooks():
    return pd.read_json('books.json')
def getRatings():
    return pd.read_json('ratings.json')
def getGenres():
    books = getBooks()
    genres = []
    for b in books["genre"]:
        genre = b.split(",")
        genres += genre
    genres = list(set(genres))
    genres.sort()
    return genres
def getUP():
    return pd.read_json('user.json')
def writeRating(userID,bookID,rating):
    newRating = json.loads('{"userID":' + str(userID) +', "bookID":' + str(bookID) + ', "rating":' + str(rating) + '}')
    ratings = getRatings()
    nR = pd.DataFrame(newRating, index=[len(ratings)])
    ratings = ratings.append(nR)
    ratings.to_json('ratings.json',orient="records")
def getNumBooks():
    books = getBooks()
    return len(books)
def getNumPeople():
    ratings = getRatings()
    lenProv = ratings.shape[0]-8
    return lenProv
def getNumRatings():
    ratings = getRatings()
    return len(ratings)
def getBook(name):
    books = getBooks()
    for b in books:
        if b["bName"] == name:
            return b
def sim(a):
    numB = getNumBooks()
    numR = getNumRatings()
    numP = getNumPeople()
    books = getBooks()
    ratings = getRatings()
    #Ratings Data for all the books by all users in a table
    ratingsData = pd.merge(ratings, books, on='bookID')
    personBookRatings = ratingsData.pivot_table(index='userID', columns='bookID', values='rating')
    personBookRatings = personBookRatings.fillna(0)
    #Correlation coefficients of all books with one another
    allCorrelationsPeople = [0 for x in range(numP)]
    personBookRatingsRev = personBookRatings.swapaxes("index", "columns")
    #This gets us the correlation of person with all others
    try:
        #11 is the user which we will make changes to
        curPersonRatings = personBookRatingsRev[11]
        corrPeople = personBookRatingsRev.corrwith(curPersonRatings).drop([11], axis=0)
        allCorrelationsPeople = pd.DataFrame(corrPeople, columns=['Correlation'])
        allCorrelationsPeople.dropna(inplace=True)
        allCorrelationsPeople.sort_values('Correlation', ascending=False, inplace=True).head()
    except:
        pass
    return allCorrelationsPeople

def pred(a,p):
    numB = getNumBooks()
    numP = getNumPeople()
    numR = getNumRatings()
    books = getBooks()
    ratings = getRatings()
    ratingsData = pd.merge(ratings, books, on='bookID')
    meanRatingsData = pd.DataFrame(ratingsData.groupby('userID')['rating'].mean())
    meanRatingsDataRev = meanRatingsData.swapaxes("index", "columns")
    meanA = meanRatingsDataRev[a]
    top = 0
    bottom = 0
    pred = 0
    simA = sim(a)
    simARev = simA.swapaxes("index", "columns")
    ratingsRev = ratings.swapaxes("index", "columns")
    for b in range(1,numP+1):
        try:
            meanB = meanRatingsDataRev[b]["rating"]
            simAB = simARev[b]["Correlation"]
            rB = ratingsRev[b]
            rBInd = rB["bookID"]
            if rBInd == p:
                rBP = rB["rating"]
            top += simAB * (rBP - meanB)
            bottom += simAB
        except:
            pass
    if bottom != 0:
        pred = meanA["rating"] + (top/bottom)
    return pred

#This needs to be fixed
#i is the userID and j is the bookID
def SVDRecBook(M,i,j):
    people = list(M.keys())
    books = list(M.swapaxes("index", "columns").keys())
    if i not in people or j not in books:
        return 0
    numR = getNumRatings()
    ratings = getRatings()
    u,sigma,vT = np.linalg.svd(M, full_matrices=True)
    u,sigma,v = u[:2].transpose(), sigma[:2].transpose(), vT.transpose()[:2].transpose()
    sigma = np.diag(sigma)
    uiv = np.matmul(u[books.index(j)],sigma)
    scaled_uiv = np.matmul(uiv,v[people.index(i)].transpose())
    avR = 0
    count = 0
    for r in range(numR):
        if ratings["bookID"][r] == j:
            avR += ratings["rating"][r]
            count += 1
    avR /= count
    return avR + scaled_uiv

#i is the userID and j is the genre
def SVDRecGenre(M,i,j):
    people = list(M.keys())
    genres = list(M.swapaxes("index", "columns").keys())
    if i not in people or j not in genres:
        return 0
    ratings = getRatings()
    books = getBooks()
    rBooks = pd.merge(ratings,books, on="bookID")
    numR = getNumRatings()
    u,sigma,vT = np.linalg.svd(M, full_matrices=True)
    u,sigma,v = u[:2].transpose(), sigma[:2].transpose(), vT.transpose()[:2].transpose()
    sigma = np.diag(sigma)
    uiv = np.matmul(u[genres.index(j)],sigma)
    scaled_uiv = np.matmul(uiv,v[people.index(i)].transpose())
    avR = 0
    count = 0
    for r in range(numR):
        if rBooks["genre"][r] == j:
            avR += rBooks["rating"][r]
            count += 1
    avR /= count
    return avR + scaled_uiv


def recBook(person):
    #On Other Users
    #Get all of the books and all of the people
    numB = getNumBooks()
    numP = getNumPeople()
    numR = getNumRatings()
    books = getBooks()
    ratings = getRatings()
    booksRev = books.swapaxes("index", "columns")
    ratingsRev = ratings.swapaxes("index", "columns")
    ratingsTab = getRatings().pivot_table(index='bookID', columns='userID', values='rating')
    ratingsTab = ratingsTab.fillna(0)

    #threshold above which would recommend a book
    recs = []
    threshold = 2
    for i in range(numB):
        # a = person
        prediction = SVDRecBook(ratingsTab,person,i+1)
        try:
            if prediction > threshold:
                rec = booksRev[i]
                recs.append((rec,"on similar users..."))

        except:
            pass

    #On Genres
    rBooks = pd.merge(ratings,books, on="bookID")
    r = rBooks.groupby('genre', as_index=False).head()
    gRatingsTab = r.pivot_table(index='genre', columns='userID', values='rating', aggfunc=np.mean)
    gRatingsTab = gRatingsTab.fillna(0)
    genres = list(gRatingsTab.swapaxes("index", "columns").keys())
    numG = len(genres)
    for i in range(numG):
        # a = person
        prediction = SVDRecGenre(gRatingsTab,person,genres[i])
        try:
            if prediction > threshold:
                rec = booksRev[i]
                recs.append((rec,"on similar genres..."))

        except:
            pass

    #Trying to combine where recs came from
    if len(recs)>0:
        recS = list(zip(*recs))
        onDict = dict()
        for rec in recS[0]:
            onDict[rec["bookID"]] = []
        for j in range(len(recS[0])):
            onDict[recS[0][j]["bookID"]].append(recS[1][j])
        for rec in onDict.keys():
            if len(onDict[rec]) == 1:
                onDict[rec] = onDict[rec][0]
            else:
                #remove the ellipsis
                onDict[rec] = onDict[rec][0][:-3] + " and " + onDict[rec][1][3:]
        rO = [booksRev[r-1] for r in onDict.keys()]
        rT = onDict.values()
        recs = list(zip(rO,rT))
    return recs

def sortProfile(user):
    books = recBook(user)
    nB = pd.DataFrame()
    for book in books:
        bookID = book[0]["bookID"]
        bookName = book[0]["bName"]
        bookGenre = book[0]["genre"]
        on = book[1]
        newBook = json.loads('{"bookID":' + str(bookID) +', "bName":"' + str(bookName) + '", "genre":"' + str(bookGenre) + '", "on":"' + str(on) + '"}')
        nB = nB.append(pd.DataFrame(newBook, index=[len(nB)]))
    nB.to_json('user.json',orient="records")
