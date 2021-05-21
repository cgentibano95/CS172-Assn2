from parsing import return_index
import sys


# This file should contain code to receive either a document-id or word or both and output the required metrics. See the assignment description for more detail.
global_dic = return_index()

def doc_command(doc):
    total_terms = 0
    for key in global_dic:
        for val in global_dic[key]:
            if val[1] == doc:
                total_terms += 1
    print("Listing for doc: " + doc)
    print("Total terms: " + str(total_terms))
    return

def term_command(term):
    doc_list = []
    doc_ctr = 0
    for x in global_dic[term]:
        if x[1] not in doc_list:
            doc_list.append(x[1])
            doc_ctr += 1
    print("Listing for term: " + term)
    print("TERMID: " + str(global_dic[term][0][0]))
    print("Number of documents containing term: " + str(doc_ctr))
    print("Term Frequency in corpus: " + str(len(global_dic[term])))
    

def dt_command(term, doc):
    term_freq = 0
    positions = []
    for key in global_dic:
        for val in global_dic[key]:
            # if passed, then we're in the doc
            if val[1] == doc and val[0] == global_dic[term][0][0]:
                # here we check to see if global dic doc matches requested doc
                # and we check to see if the termid matches the requested termid
                term_freq += 1
                positions.append(val[2])
                
    print("Inverted list for term: " + term)
    print("In document: " + doc)
    print("TERMID: " + str(global_dic[term][0][0]))
    print("Term Frequency in doc: " + str(term_freq))
    print("Positions: " + str(positions))
        
if sys.argv[1] == "--doc" and len(sys.argv) < 4:
    doc = sys.argv[2]
    doc_command(doc)
elif sys.argv[1] == "--term" and len(sys.argv) < 4:
    term = sys.argv[2]
    term_command(term)
elif sys.argv[1] == "--term" and sys.argv[3] == "--doc":
    dt_command(sys.argv[2],sys.argv[4])


