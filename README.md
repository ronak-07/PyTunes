
PyTunes
===========

A GUI implementation for searching song and saving lyrics in a text file.

Vector space model implementation considering the cosine score. 
The weight of document has been calculated using Euclidean normalization. 
The length of lyrics and presence of uncommon words has been accounted.
To account for spelling suggestion in case of absence of such a word, distance package has been used.
In case of opting for console, input can be given via voice as well. speech_recognition package has been used for it.

General Description
-------------------

### Pre-process.py

Since the data corpus is static, we decided to tradeoff space with time. This is uses the Pickle Library to permanently store the following:
    Dictionary: 		dictionary_lyrics , answer
    Matrix:     		vector_space, document_term_weight
- Each row is read from the song_list.csv and answer - dictionary with serial no. as a key and value as the name of the artist, name of the song and lyrics is updated.
 
-	Using the nltk package lyrics are tokenized and are converted to lower case.

-	Using tokenized lyrics we make dictionary which act as a hash map to words in the lyrics and to access that term in the vector_space Matrix.

-	Apply Euclidean Normalization to calculate the Weight of each term in document.

-	Since the corpus is static, we save them. This will decrease the pre-processing time for future process.

### PyTunes.py
This is for a graphical user interface (GUI) which uses load_pickle.py for fetching the songs with top ten tf*idf scores. 
-	The search button when pressed calls the input_query() form load_pickle.py. It returns a list of songs with decreasing order of tf*idf scores.

-	Using the answer dictionary prepared in the pre-processing.py we append the results to display.

-	The song details button when clicked again fetches the lyrics, artist and the name of the song using the answer dictionary.

-	The lyrics can be saved in a separate folder – “Saved Songs” which will be automatically created if it doesn’t exist.



### load_pickle.py
Time to fetch query (Avg. of 3 runs): 0.05624 seconds (Subject to query length of 3 words)

It uses the saved pickle files to calculate the tf-idf scores.

-	Process the input query by converting to lower case and tokenization (using nltk package). It includes checking for spelling correction (using distance package) if word is not present in the dictionary.

-	Calculate tf: that is total no. of songs in which a particular word is present

-	Calculate tf-weight:

        1. Calculate idf value                 
        2. Calculate the tf_weight 
            tf value = 1 + log(song-frequency)
            idf value= log(Total no. of songs/song-frequency)
            tf_weight = tf_value*idf_value

-	Calculate the summation of tf*idf score of each song for each word
 
-	Return the songs key in decreasing order of their tf*idf score to PyTunes.py if console is used otherwise return it to print it on the console


Contributors
-------------
[Ronak Sisodia](https://github.com/ronak-07)
