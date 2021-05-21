from math import sqrt
from os import write
import string
import sys
from parsing import return_index

global_dic = return_index()

'''
Returns a query dictionary
with key = query number and value = list of words from the query

query_dict[query number] : [words, from, query]
'''
def returnQuery(query_file):
    query_nums = []
    file1 = open(query_file,"r+") 
    Lines = file1.readlines()
    word_list = []
    for l in Lines:
        query_nums.append(int(l.split(".")[0]))
        l = l.translate(str.maketrans('', '', string.punctuation))
        word_list.append(l.split()[1:])
    # removed leading digits
    with open("stopwords.txt", "r") as a_file:
            stopwords = []
            for line in a_file:
                stripped_word = line.strip()
                stopwords.append(stripped_word)

    query_dict = {}
    key = 0
    for line in word_list:
        temp_list = []
        #print(line)
        for word in line:
            if word not in stopwords:
                temp_list.append(word.lower())
        query_dict[query_nums[key]] = temp_list
        key += 1
    # stop words removed and made all words lowercase
    return query_dict

'''
returns a 2D list of top ten cos sim scores, with a rank 1-10
'''
def calcTopTen(scores_lib):
    scores = []
    for docs in scores_lib:
        scores.append([docs,scores_lib[docs]])

    top_ten = sorted(scores,key=lambda l:l[1], reverse=True)
    ranked_ten = []
    rank = 1
    
    for doc,score in top_ten[0:10]:
        ranked_ten.append([doc,round(score,6),rank])
        #print(doc + " score: " + str(score) + " rank: " + str(rank))
        rank += 1
        
    return ranked_ten

'''
Calculates cos sim using binary weights

This is all just for one query at a time
'''
def calcCos(query):

    found_docs = []
    # first find all docs containing the word
    for word in query:
        if word in global_dic:
            if(len(global_dic[word]) > 0):
                # if here, we found docs that contain the word from query
                for docs in global_dic[word]:
                    # append all docs for the provided query to a list
                    found_docs.append(docs[1])

    # now go through each document that contains the word
    score_lib = {}
    for docno in found_docs:
        doc_list = [0] * len(query)
        query_list = [1] * len(query)
        ctr = 0
        for word in query:
            # go through each word in query
            if (word in global_dic):
                for docs in global_dic[word]:
                    # find all docs that contain the word
                    if docs[1] == docno:
                        # if the document number matches the global doc, then we can change it to 1
                        # also means that the word is found in the doc
                        doc_list[ctr] = 1
            # next word, iterate index ctr
            ctr += 1
        # done with all words, calculate cos sim.
        dot_product = sum(i[0] * i[1] for i in zip(doc_list, query_list))
        doc_denom = sqrt(sum(map(lambda x:x*x,doc_list)))
        q_denom = sqrt(sum(map(lambda x:x*x,query_list)))
        if doc_denom != 0 or q_denom != 0:
            score = dot_product / (doc_denom * q_denom)
        # score is done for one query
        score_lib[docno] = score

    # now calculate top ten since we have all scores
    top_ten = calcTopTen(score_lib)

    # top ten is a 2d list that has scores and ranks
    return top_ten

'''
Calc scores takes care of the query, and passes it into another function
that then takes care of calculating binary weights
& calculates cos similarity
'''
def calcScores(query_lib):
    # run through each query
    query_scores = {}
    #query_scores[query number] : list of top ten documents with their scores
    for query_no in query_lib:
        #print("trying query number: " + str(query_no))
        query_scores[query_no] = calcCos(query_lib[query_no])
    
    return query_scores

'''
this function writes to a file provided by user in terminal
'''
def writeToFile(query_scores, results_txt):
    with open(results_txt, 'w') as f:
        for qno in query_scores:
            for x in query_scores[qno]:
                f.write(str(qno) + " Q0 " + str(x[0]) + " " + str(x[2]) + " " + str(x[1]) + " Exp\n")
    return

#######
# main operations
#######
query_txt = sys.argv[1]
results_txt = sys.argv[2]
query = returnQuery(query_txt)
query_scores = calcScores(query)
# we now have top 10 scores for query
# query_scores[query number] : (docno, score, rank)
# we can write to provided results txt file
writeToFile(query_scores, results_txt)




