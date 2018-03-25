# Sentiment Analysis
To analyse the sentiment of a product review ( positive or negative ) using a Naive Bayes Classifier
# Environment
The project was implemented in Python IDE
# Requirements
Operating System : Windows 7/8/10

RAM : A minimum of 2 GB

Hard Disk space : 5 GB 

Platform : Python 3.x (Version 3.0 or later, preferably 3.6.2) 
# Training and Testing Data
Refer at: https://drive.google.com/drive/folders/0Bz8a_Dbh9Qhbfll6bVpmNUtUcFdjYmF2SEpmZUZUcVNiMUw1TWN6RDV3a0JHT3kxLVhVR2M

Download the amazon_review_polarity.csv file, which contains train.csv and test.csv
# Modules used
csv - for reading and writing in csv files
# External Libraries
No external libraries were used in the project. 
# Implementation
The project uses a "Bag of Words" model, where we classify the given product review based on the count(number) of words that are positive or negative.

The various steps involved are:
1. Read the training data from the .csv file

              import csv
              dataset = open("train.csv","r",encoding = "utf8")
              reader=csv.reader(dataset)
2. Add the words in the product review, to the feature set, only when it is above a minimum threshold value ( Here, it has been taken as 1000).

              threshold=1000
3. Define all possible stop words, in a list.
4. Add the words to the feature set, by iterating through every word in the reader object.

              featureset={}                                                   #Initialise the feature set
              for row in reader :                                             #For every line in the review (each row is a line)
                  for i in range(1,len(row)):                                 #Iterating through every word in the line
                      word = row[i].split();                                  #Split the line into words.
                      for entry in word:                                      #For every entry in the word list
                          if entry.lower() in stop_words:                     #Skip all stop words
                              continue
                          if entry in featureset.keys():                      #If the word is already present, increment its entry
                              featureset[entry]=featureset[entry]+1
                          else:
                              featureset[entry]=1                             #For new occurence, set its value to 1
5. Remove the words from the feature set, that are below the minimum threshold value.

              de_key =[]                                        #Initialise the remove words list
              for key in featureset:                            #For every word in the feature set
                  if featureset[key] < threshold:               #If the occurence is less than the minimum threshold, add to de_key list 
                      de_key.append(key)
              for entry in de_key:                               #Delete all the words in the de_key list
                      del featureset[entry]
6. Initialise the probability table (dictionary)

              prob_table={}
              for key in featureset:
                  prob_table[key]=[0,0]
7. If the class label is 2, then it is a positive review, else it is a negative review

              for row in reader:
                  if( row[0] == '2'):
    	                flag = 0
    	                positive = positive + 1
                  else:
                      flag = 1
                      negative = negative + 1
8. Increment the word entry in the probability table. For positive words, add them to the entry with flag 0, else add them to the entry with flag 1 

              word = set()
              for i in range(1,len(row)):                     #Iterating through words
                  temp =row[i].split();
                  for entry in temp:                          #Add words to the word list
                      word.add(entry)
              for entry in word:                              #If the word is found in the feature set, increment the prob table's entry
                  if entry in featureset.keys():
                      prob_table[entry][flag] = prob_table[entry][flag] + 1
9. Calculate the prior probabilities

              prior_prob_positive = positive / (positive+negative)
              prior_prob_negative = negative / (positive+negative)
10. Calculate the posterior probablility using the Naive Bayes Classifier formula.

              pos = pos * prob_table[entry][0]           
              neg = neg * prob_table[entry][1]
