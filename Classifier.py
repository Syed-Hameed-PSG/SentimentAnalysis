import csv
dataset = open("train.csv","r",encoding = "utf8")
reader=csv.reader(dataset)
threshold = 10

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
for row in reader :
    for i in range(1,len(row)):
        word = row[i].split();
        for entry in word:
            if entry.lower() in stop_words:
                continue
            if entry in featureset.keys():
                featureset[entry]=featureset[entry]+1
            else:
                featureset[entry]=1
de_key =[]
for key in featureset:
    if featureset[key] < threshold:
        de_key.append(key)
for entry in de_key:
    del featureset[entry]
print(len(featureset))
prob_table={}
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
    if( row[0] == '2'):
    	flag = 0
    	positive = positive + 1
    else:
        flag = 1
        negative = negative + 1
    word = set()
    for i in range(1,len(row)):
        temp =row[i].split();
        for entry in temp:
            word.add(entry)
    for entry in word:
        if entry in featureset.keys():
            prob_table[entry][flag] = prob_table[entry][flag] + 1
print(positive)
prior_prob_positive = positive / (positive+negative)
prior_prob_negative = negative / (positive+negative)
for key in featureset:
    prob_table[key][0]=(prob_table[key][0]/positive)
    prob_table[key][1]=prob_table[key][1]/negative
print("prior_prob_positive ",end=" ")
print(prior_prob_positive)
print("prior_prob_negative ",end=" ")
print(prior_prob_negative)
csvfile=open('output.csv','w+')
csvfile.write("keyword,positiveprob,negativeprob\n")
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
            word.add(entry)
    for entry in word:
        if entry in featureset:
            pos = pos * prob_table[entry][0]
            neg = neg * prob_table[entry][1]
    if(pos > neg):
        if(row[0] == '2'):
            accuracy = accuracy + 1
    else:
        if(row[0] == '1'):
            accuracy = accuracy + 1
print(accuracy/count)
testdata.close()

