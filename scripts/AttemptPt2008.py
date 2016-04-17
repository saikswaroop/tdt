__author__ = 'vibhabhambhani'
import os
import pickle
import math

def tokenizeAndDocumentVectorCreation(fileoutput,tfRawD):
    words = fileoutput.split()
    length = len(words)
    uniqueWordsInDoc = set()
    for word in words:
        uniqueWordsInDoc.add(word)
        if word not in tfRawD:
            tfRawD[word]=1
        else:
            tfRawD[word]+=1
    for i in tfRawD:
      tfRawD[i]=float(tfRawD[i])/length

    return uniqueWordsInDoc,words,length,tfRawD

def extractVocab(V,uniqueWordsInDoc):
    tempV=dict(V)
    copyOfUniqueWordsInDoc=set(uniqueWordsInDoc)
    while copyOfUniqueWordsInDoc.__len__()!=0:
        x = copyOfUniqueWordsInDoc.pop()
        if x in tempV:
            tempV[x] = tempV[x]+1
        else:
            tempV[x] = 1
    return tempV

def updateAvgLength(lenAvg,length,N):
    return (lenAvg*N+length)/(N+1)

def updateN(N):
    return N+1

def calcluatetfD(tfRawD,lenD,lenAvg):
    tfD ={}
    for i in tfRawD:
            tfD[i]=float(tfRawD[i])/(tfRawD[i]+0.5+1.5*(lenD/lenAvg))
    return tfD

def calculatetfT(tfRaw,length):
    tfT={}
    for i in tfRaw:
            tfT[i]=float(tfRaw[i])/(tfRaw[i]+0.5+1.5*(length/lenAvg))
    return tfT


def calculateidf(V,N):
    idf={}
    for word in V:
        print("N")
        print(N)
        Nor=(math.log((1.0*N/V[word]),10))
        idf[word]=Nor/math.log((N+1),10)
    return idf


def CalcProductDoc(tfD, idf):
    Dh ={}
    for word in tfD:
            Dh[word]=tfD[word]*idf[word]
    return Dh
def CalcProductTopic(tfT,idf):
    Th ={}
    for word in tfT:
            Th[word]=tfT[word]*idf[word]
    return Th

def similarity(Dh,Th):
    Dh_Th=0
    DhSquared=0
    ThSquared=0
    for word in V:
        if word in Dh:
            Dvalue=Dh[word]
        else:
            Dvalue=0
        if word in Th:
            Tvalue=Th[word]
        else:
            Tvalue=0

        Dh_Th+=1.0*Dvalue*Tvalue
        #print(Dh_Th)
        DhSquared+=1.0*Dvalue*Dvalue
        ThSquared+=1.0*Tvalue*Tvalue
    cosineDeno=math.sqrt(DhSquared*ThSquared)
    similarity=float(Dh_Th)/cosineDeno
    return similarity

#Read the topics file
topics=[]
topicsFile = "/Users/vibhabhambhani/Desktop/NLP/Project/Program/topics.txt"
topics= pickle.load( open( topicsFile, "rb" ) )

#Define folder for topic outputs
outputFolder ="/Users/vibhabhambhani/Desktop/NLP/Project/output"
outputFile="/Users/vibhabhambhani/Desktop/NLP/Project/output.txt"

#Read the input folder
inputFolder = "/Users/vibhabhambhani/Desktop/NLP/Project/inputData"

#docs list containing the list of documents inputFolder
docs=[]

#Read documents in the input folder in the docs list
for item in os.listdir(inputFolder):
   if not item.startswith('.') and os.path.isfile(os.path.join(inputFolder, item)):
        docs.append(os.path.join(inputFolder, item))

#For each document
for doc in docs:
    #### split by words
    DVector=[]
    uniqueWordsInDoc=set()
    docOpen = open(doc,"r")
    tfRawD={}
    uniqueWordsInDoc,DVector,lenD,tfRawD= tokenizeAndDocumentVectorCreation(docOpen.read(),tfRawD)

    ####create a vocabulary V which will contain a list of words and the
    for topic in topics:
        #dictionaryOfTopics.append({'topic':topic,'T':T,'V':V,'lenAvg':lenAvg,'N':N})

        #### df of the words
        #print(topic['V'])
        V=extractVocab(topic['V'],uniqueWordsInDoc)

        #print(V)
        ####lenAvg documents
        lenAvg=0
        lenAvg=updateAvgLength(topic['lenAvg'],lenD,topic['N'])
        #print(lenAvg)
        ####update N
        N=0
        N=updateN(topic['N'])
        #print(N)
        ###tdf
        '''
        #Step2: TF-IDF SCORE COMPUTATION
        #   tf =         tfRaw
        #       ---------------------
        #       tfRaw +0.5 +1.5 *  lenD
        #                         ------
        #                         lenAng
        #take as input a folder path which contains documents to be classified

        #for each document in the folder

        #construct D vector

        #TF SCORE COMPUTATION

        #get the "lenD" length of the document value
        #update the "lenAvg" the average length of document value (use N and lenAvg and lenD)
        #get all the unique words in a set for D_raw
        #get all the raw frequencies of the unique words found in D_raw and store them in a dictionary "tf_raw" which contains
        ## [term]:number of occurrences in document D
        #calculate "tf" dictionary [terms]:modified values -- incorporating the length feature
        '''
        #Calculated tfD --- tf of Document
        print(tfRawD.__len__())
        print(uniqueWordsInDoc.__len__())
        print("tfRawD and uniqueWords")
        print(tfRawD)
        print(uniqueWordsInDoc)
        print("tfRaw of topic")
        print(topic['tfRaw'])
        tfD={}
        tfD = calcluatetfD(tfRawD,lenD,lenAvg)
        print("tfD")
        print(tfD)
        #Calculated tfT --- tf of Topic
        tfT={}
        tfT = calculatetfT(topic['tfRaw'],topic['length'])
        print("tfT")
        print(tfT)

        #IDF SCORE COMPUTATION
        #update idf statistics
        idf={}
        idf = calculateidf(V,N)
        print("V")
        print(V)
        print("idf")
        print(idf)

        #tf.idf for document

        Dh={}
        Dh = CalcProductDoc(tfD, idf)


        #tf.idf for topic
        Th={}
        Th = CalcProductTopic(tfT,idf)

        #print(Dh)
        #print(Th)
        '''
        #update the 'N' number of documents count

        #update the vocabulary V which has document frequency in it. df --- for already existing words update the score ---- for new words add them to the vocabulary
        ##with the no.docs they appear in ---'V'dictionary [term]:no.of docs the term appears in---

        #calculate 'idf' scores for all terms in 'D_raw' using 'V' and 'N'values

        #Compute tf.idf


        #apply tf.idf dictionary [term]:value weighting to D and T vectors --- 2 tf.idf dictionaries -- one for D and one for T

        '''
        #print(Dh)

        #Step3: Story similarity computation
        similarityValue=similarity(Dh,Th)
        print(similarityValue)
        #for each 'h' in 'T' do
        ####'Dh*Th'+='Dh'*'Th' #where Dh = tf.idf for term h
        ####'DhSquared'+=squared('Dh')
        ####'ThSquared'+=squared('Th')
        #'cosineDeno'=sqrt('DhSquared'*'ThSquared')
        #similarity(D,T)='Dh*Th'/'cosineDeno'