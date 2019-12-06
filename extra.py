def createRatingMatrix(numP,numB,people):
    ratingMatrix = [[None for x in range(numB)] for y in range(numP)]
    #creating the rating matrix
    for p in range(numP):
        ratings = people[p]["ratings"]
        for r in ratings:
            ratingMatrix[r["bookID"]][p] = r["rating"]
    return ratingMatrix
def sim(a,b):
    numP = getNumPeople()
    numB = getNumBooks()
    people = getPeople()
    ratingMatrix = createRatingMatrix(numP,numB,people)
    #calculating sim for the matrix given
    sim = 0
    top = 0
    botL = 0
    botR = 0
    meanRA = 0
    meanRB = 0
    #calculate meanRA and meanRB
    count = 0
    for i in range(numB):
        if (ratingMatrix[i][a["id"]-1] != None) and (ratingMatrix[i][b["id"]-1] != None):
            count+=1
            meanRA += ratingMatrix[i][a["id"]-1]
            meanRB += ratingMatrix[i][b["id"]-1]
    meanRA /= count
    meanRB /= count
    #calculating sim
    for i in range(numB):
        if (ratingMatrix[i][a["id"]-1] != None) and (ratingMatrix[i][b["id"]-1] != None):
            top += (ratingMatrix[i][a["id"]-1]-meanRA)*(ratingMatrix[i][b["id"]-1]-meanRB)
            botL += (ratingMatrix[i][a["id"]-1]-meanRA)**2
            botR += (ratingMatrix[i][b["id"]-1]-meanRB)**2
    botL = math.sqrt(botL)
    botR = math.sqrt(botR)
    sim = top/(botL*botR)
    return sim

def pred(a,p):
    return 0


#create the rating matrix
ratingMatrix = createRatingMatrix(numP,numB,people)
#create the sim matrix for all people with
for a in range(numP):
  sim[person][a] = sim(person, people[a])
for p in range(numB):
  pred[p] = pred(person,p,sim)
