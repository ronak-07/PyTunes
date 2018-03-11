"""  
  Project : To build an IR model based on a vector space model                  
  Course No : CS F469 Information Retrieval

  Time for pre- processing (Avg. of 3 runs): 78.1299557685852
    
"""
'''
    Tokenizing dataset on requirement    
'''
from nltk import word_tokenize

'''
    library pickle is used to save and load already saved data structures. It saves the pre processing time.
'''
import pickle

import time
import math
import csv
import re


#Dictionary as a hash map. Words are the key and value holds an integer
dictionary_lyrics= dict()

#To save the csv file in a dictioanry format
answer = dict()

#Initilizing a gloabal index used to note number of words in the dictionary_lyrics
index=-1

#Matrix size. Rows = Expected no. of different words in the songs_list
#Matrix size. Columns = 1 + No. of songs in the songs_list.csv. 
songs, words = 1764,18700;

#Matrix for Vector-space Model
vector_space = [[0 for x in range(songs)] for y in range(words)]

#Matrix for storing the Document Term Weight 
document_term_weight= [[0 for x in range(songs)] for y in range(words)]



def pickled():
    """
            This function uses the Pickle Library to permanently store the following:
            Dictionary: dictionary_lyrics , answer
            Matrix:     vector_space, document_term_weight
    """
    with open("dictionary_lyrics.pickle","wb") as f:
        pickle.dump(dictionary_lyrics,f)
    with open("answer.pickle","wb") as f:
        pickle.dump(answer,f)
    with open("vector_space.pickle","wb")as f:
        pickle.dump(vector_space,f)
    with open("document_term_weight.pickle","wb") as f:
        pickle.dump(document_term_weight,f)


def euclidean_normalization_document(key):
    """
            This function is used to calculate weight of each term in each document
    """
    #key is the hash value of song. column holds the term-frequency of the song
    column=[col[key] for col in vector_space]

    #Calculate the root of the summation of square of term- frequency
    denominator= math.sqrt(sum(i*i for i in column))

    #Dividing each term of the column 
    for index,x in enumerate(column):
        document_term_weight[index][key]= x/denominator
    
def update_matrix(i,j):
    #Updating the term-frequency. i the term and j is the hash value of song
    vector_space[i][j]=vector_space[i][j]+1

def make_dictionary(key,lyrics=[]):
    '''
	If the word is already in dictionary update the vector_space.
        dictionary_lyrics[word] returns the hash value of the word that is used to access the term in vector_space Matrix
    '''
    for word in lyrics:
        if len(word)>2:

            if word in dictionary_lyrics:
                update_matrix(int(dictionary_lyrics[word]),int(key))

            #Else first add the word in dictionary and the update the vector_space
            else:
                dictionary_lyrics[word]=[]
                global index
                index+=1;
                dictionary_lyrics[word]=index
                update_matrix(int(dictionary_lyrics[word]),int(key))
            

def main():
    with open("songs_list.csv") as f:
       reader=csv.DictReader(f)
       for row in reader:
           #answer is a dictionary with serial no. as a key and value as the name of the artist, name of the song and lyrics.
           answer[row['key']]=[]
           answer[row['key']].append(row['artist'])
           answer[row['key']].append(row['song'])
           answer[row['key']].append(row['text'])

           #Lyrics will hold words in lower characters and after tokenization.
           lyrics = row['text'].lower()                 
           lyrics = re.split("[,\n -!?:]+",lyrics)

           #Using tokenized lyrics to make dictionary & update the vector_space Matrix.
           make_dictionary(row['key'],lyrics)

           #Applying Euclidean_Normalization to calculate the Weight of each term in document.
           euclidean_normalization_document(int(row['key']))

       #Since the corpus is static, we save them. This will decrease the pre-processing time.
       pickled()
 
if __name__ == "__main__":
    start = time.time()
    main()
    print(time.time()-start)
