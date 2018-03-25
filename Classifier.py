import csv
dataset = open("train.csv","r",encoding = "utf8")                 #Read the data from the .csv file
reader=csv.reader(dataset)
threshold = 1000
#The list of Stop Words
stop_words ={'ourselves', 'hers', 'between', 'yourself','i\'m',     
             'but', 'again', 'there', 'about', 'once', 'during',
              'out', 'very', 'having', 'with','they', 'own',
              'an', 'be', 'some', 'for', 'do', 'its', 'yours', 'such', 'into', 'of', 'most', 'itself', 'other', 'off', 'is', 's', 'am', 'or', 'who', 'as', 'from', 'him', 'each', 'the', 'themselves', 'until', 
	    'below', 'are', 'we', 'these', 'your', 'his', 'through', 'don',  'me', 'were', 'her', 'more', 'himself', 'this', 'down', 'should',
	    'our', 'their', 'while', 'above', 'both', 'up', 'to', 'ours', 'had', 'she', 'all', 'no', 'when', 'at', 'any', 'before', 'them', 'same', 'and', 'been', 
	    'have', 'in', 'will', 'on', 'does', 'yourselves' , 'then', 'that', 'because', 'what' , 'over', 'why', 'so', 'can', 'did',
	 'now', 'under', 'he', 'you', 'herself', 'has', 'just','where', 'too', 'only', 'myself', 'which', 'those', 'i', 'after' ,'few', 'whom', 't', 'being', 'if', 'theirs', 'my', 'against', 'a', 'by', 'doing', 'it', 'how', 'further', 'was', 'here', 'than'
	,' ', '!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ':', ';', '<', '=', '>', '?',
             '@', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '[', '\\', ']', '^', '_', '`', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ' ', '¡', '¢', '£', '¤', '¥', '¦', '§', '¨', '©', 'ª', '«', '¬', '­', '®', '¯', '°', '±', '²', '³', '´', 'µ', '¶', '·', '¸', '¹', 'º', '»', '¼', '½', '¾', '¿', 'À', 'Á', 'Â', 'Ã', 'Ä', 'Å', 'Æ', 'Ç'}
count =0
featureset={}                                                                   
print("started")
featureset={}                                                      #Initialise the feature set
for row in reader :                                                #For every line in the review (each row is a line)
    for i in range(1,len(row)):                                    #Iterating through every word in the line
        word = row[i].split();                                     #Split the line into words.
        for entry in word:                                         #For every entry in the word list
            if entry.lower() in stop_words:                        #Skip all stop words
                continue
            if entry in featureset.keys():                         #If the word is already present, increment its entry
                featureset[entry]=featureset[entry]+1
            else:
                featureset[entry]=1                                #For new occurence, set its value to 1

de_key =[]                                                         #Initialise the remove words list
for key in featureset:                                             #For every word in the feature set
    if featureset[key] < threshold:                                #If the occurence is less than the minimum threshold, add to de_key list 
        de_key.append(key)
for entry in de_key:                                               #Delete all the words in the de_key list
    del featureset[entry]

print(len(featureset))

prob_table={}                                                      #Initialise the probability table                                     
for key in featureset:
    prob_table[key]=[0,0]                                       
flag =0 
positive = 0 
negative = 0
count = 0
dataset.close()
dataset = open("train.csv","r",encoding = "utf8")               
reader=csv.reader(dataset)
for row in reader:
    if( row[0] == '2'):                                            #For positive words
    	flag = 0
    	positive = positive + 1
    else:
        flag = 1                                                   #For negative words
        negative = negative + 1
    word = set()
    for i in range(1,len(row)):
        temp =row[i].split();
        for entry in temp:
            word.add(entry)                                        #Add individual entries to the word list
    for entry in word:
        if entry in featureset.keys():
            prob_table[entry][flag] = prob_table[entry][flag] + 1  #If the entry is in the feature set, increment the corresponding entry in the probability table
print(positive)
prior_prob_positive = positive / (positive+negative)               #Prior probabilities
prior_prob_negative = negative / (positive+negative)
for key in featureset:
    prob_table[key][0]=(prob_table[key][0]/positive)
    prob_table[key][1]=prob_table[key][1]/negative
print("prior_prob_positive ",end=" ")
print(prior_prob_positive)
print("prior_prob_negative ",end=" ")
print(prior_prob_negative)
csvfile=open('output.csv','w+')
csvfile.write("keyword,positiveprob,negativeprob\n")               #Positive and negative probabilities of each keyword in the review (excluding the stop words
for key in featureset:
    print(key,end=" ")
    print(prob_table[key][0],end=" ")
    print(prob_table[key][1])
    csvfile.write(key+",")
    csvfile.write(str(prob_table[key][0]))
    csvfile.write(",")
    csvfile.write(str(prob_table[key][1]))
    csvfile.write("\n")
csvfile.close()
dataset.close()
count = 0
accuracy =0
testdata = open("test.csv","r",encoding = "utf8")
reader=csv.reader(testdata)
for row in reader:
    pos = prior_prob_positive
    neg = prior_prob_negative
    count = count + 1                                             
    word = set()
    for i in range(1,len(row)):
        temp =row[i].split();
        for entry in temp:
            word.add(entry)                                         #For every entry in the word list
    for entry in word:
        if entry in featureset:                                     #If the entry is in the feature set, we find the posterior probability using the Naive Bayes Classifier formula
            pos = pos * prob_table[entry][0]
            neg = neg * prob_table[entry][1]
    if(pos > neg):
        if(row[0] == '2'):
            accuracy = accuracy + 1                                 #Accuracy of the classification
    else:
        if(row[0] == '1'):
            accuracy = accuracy + 1
print((accuracy/count)*100)                                         #Print the total accuracy
testdata.close()

