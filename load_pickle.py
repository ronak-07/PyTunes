"""  
  Project : To build an IR model based on a vector space model                  
  Course No : CS F469 Information Retrieval

  Time for finding the result(Avg. of 3 runs): 0.056248 seconds (Subject to query length of 3 words)
"""

'''
    Tokenizing dataset on requirement    
'''
from nltk import word_tokenize

'''
    speech_recognition is a library for converting speech to text    
'''
import speech_recognition as sr

'''
    library distance is used to calculate the Levenshtein distnace
'''
import distance


'''
    library pickle is used to save and load already saved data structures. It saves the pre processing time.
'''
import pickle

import time
import math
import re


#Dictionary to hold the term-frequency 
tf= dict()

#Dictioanry to hold the Inverse song-frequency 
idf=dict()

#Dictionary to hold the tf*idf score
tf_weight=dict()

#Dictionary to hold the final_list of the songs to be displayed
final_list=dict()

#Total no. of songs in the songs_list.csv
N= 1762


'''
    Loading the dictionaries and matrices calculated in the Pre-process.py

        dictionary_lyrics:        Dictionary as a hash map. Words are the key and value holds an integer
        answer:                   To save the csv file in a dictioanry format
        vector_space:             Matrix for Vector-space Model
        document_term_weight:     Matrix for storing the Document Term Weight
'''
with open("dictionary_lyrics.pickle","rb") as f:
    dictionary_lyrics=pickle.load(f)
with open("answer.pickle","rb") as f:
        answer=pickle.load(f)
with open("vector_space.pickle","rb") as f:
        vector_space=pickle.load(f)
with open("document_term_weight.pickle","rb") as f:
        document_term_weight=pickle.load(f)



def calculate_tf_weight(words=[]):
    '''
        calculate_tf-weight(words=[])
                1. Calculate idf value.
                2. Calculate the tf_weight 
			tf value = 1 + log(song-frequency)
			idf value= log(Total no. of songs/song-frequency)
                        tf_weight = tf_value*idf_value
    '''
    for word in words:
            deno=tf[word]
            if deno>0:
                    idf[word]=math.log10(N/deno)
            else:
                    idf[word]=0
            tf_weight[word] = idf[word]*(1+ math.log10(tf[word]))



def calculate_tf(words=[]):
    '''
         Calculate the song-frequency that is total no. of songs in which a particular word is present
         dictionary_lyrics[word] returns the hash value of the word that is used to access the term in vector_space Matrix
    '''
    for word in words:
            tf[word]=((sum(x>0 for x in vector_space[dictionary_lyrics[word]])))



def finding_songs(words=[]):
    '''       
        1. Find songs that has at least one word from the query using bag of word model
        2. Calculate song-frequency for these words
        3. Calculate the term_weight for these words
        4. Calculate the tf*idf score for each song that satisfy point 1 above
        5. Arrange the songs in the decreasing order of their tf*idf score
        6. Return the list in point 5 above     
    '''
    #words hold the bag of words which shall be used to find the songs that shall be considered
    #Songs will hold set of songs for which tf*idf score shall be calculated
    
    songs=set()
    
    #Finding the songs that has at least one word from the bag of the word model
    for word in words:
        for index,song in enumerate(vector_space[dictionary_lyrics[word]]):
            if song > 0:
                songs.add(index)

    calculate_tf(words)
    calculate_tf_weight(words)

    #Calculate the summation of tf*idf score of each song for each word
    for song in songs:
        final_list[song]=0
        for word in words:
            final_list[song]=final_list[song] + tf_weight[word]*document_term_weight[dictionary_lyrics[word]][song]

    #List of songs in decreasing order of their tf*idf score
    sort_list=sorted(final_list,key=final_list.__getitem__,reverse=1)
    final_list.clear()
    return (sort_list)


def input_query(query):
        '''
        1. Tokenize Query
        2. For word in Tokenized Query
            If the word is in dictionary, append it for final_query.
            else using distance library use the first word from the returned list. This acts as a spelling correction
        '''
        #Tokenize and then convert to lower case.
        tokenized_query = word_tokenize(query)
        final_query=[]
        for word in tokenized_query:
            word= word.lower()

            #If word is present in dictionary_lyrics
            if word in dictionary_lyrics:
                final_query.append(word)
                
            else:
                #distance.ifast_comp() returns words with a Levenshtein distnace of less than or equal to 2
                select_word=sorted(distance.ifast_comp(word,dictionary_lyrics))

                #If select_word is not empty, using the first suggestion.
                if len(select_word)>0:
                    key=select_word[0][1]
                    final_query.append(key)
        
        if len(final_query)>0:
                   return(finding_songs(final_query))
        else:
            print("Please check the spelling, Levenshtein distnace of 2 results no result")
            

def print_songs(song_list):
    '''
            Printing songs on the console only if GUI is not used.
    '''
    for index,x in enumerate(song_list):
        if index>2:
            break
        print("The artist is: " + answer[str(x)][0] + "\tThe song is: " + answer[str(x)][1])
        print("\nLyrics:\n" + answer[str(x)][2])
        print("\n\n\n")
        

def speechInput():
    '''
            To take input via the Microphone. It uses speech_recognition library to convert speech to text.
    '''
    start=time.time()
    r=sr.Recognizer()
    with sr.Microphone() as source:
            print("Listening Now:")
            audio = r.listen(source)
            if time.time()-start >5:
                    print("Seems like I am not a good ear after all!")

    try:
        print(r.recognize_google(audio))
        inp=input("If you meant this, please press Y else N\t")
        if inp.lower() =='y':
                query =  r.recognize_google(audio)
        else:
                query = input("Sorry! Can you please enter the query.Seems like I am having a bad day!\n")
    except sr.UnknownValueError:
            query = input("Sorry.Can you please enter the query.Seems like I am having a bad day!\n")
    except sr.RequestError as e:
            query = input("Sorry!! Can you please enter the query.Seems like I am having a bad day!\n")

    return query


def main():
    #Keyboard input or Speech Input
    input_via= input("Press 1 for Speech Input and Press any other number for Keyboard input\n")

    if input_via=="1":
        query= speechInput()

    else:
        #If GUI is not used, to take the input through console
        query = input("Please enter the song you would like to search!\n")

    #Processing the input query
    start=time.time()
    song_list= input_query(query)
    print("Time to fetch the query: " + str(time.time()-start) + " seconds")
    
    #Printing the song on console
    print_songs(song_list)
        
if __name__ == "__main__":
    main()
