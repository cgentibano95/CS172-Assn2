import re
import os
import zipfile
import string
from collections import Counter, defaultdict

def return_index():
    # Regular expressions to extract data from the corpus
    doc_regex = re.compile("<DOC>.*?</DOC>", re.DOTALL)
    docno_regex = re.compile("<DOCNO>.*?</DOCNO>")
    text_regex = re.compile("<TEXT>.*?</TEXT>", re.DOTALL)
    index_dictionary = defaultdict(list) # global dict
    termid_map = {}
    tid_ctr = 1
    with zipfile.ZipFile("./data/ap89_collection_small.zip", 'r') as zip_ref:
        zip_ref.extractall()
    
    # Retrieve the names of all files to be indexed in folder ./ap89_collection_small of the current directory
    for dir_path, dir_names, file_names in os.walk("ap89_collection_small"):
        allfiles = [os.path.join(dir_path, filename).replace("\\", "/") for filename in file_names if (filename != "readme" and filename != ".DS_Store")]
    ctr = 0
    for file in allfiles:
        
        #print("checking file: " + str(ctr))
        ctr += 1
        with open(file, 'r', encoding='ISO-8859-1') as f:
            filedata = f.read()
            result = re.findall(doc_regex, filedata)  # Match the <DOC> tags and fetch documents
            
            for document in result[0:]: #delete 1 later
                # Retrieve contents of DOCNO tag
                docno = re.findall(docno_regex, document)[0].replace("<DOCNO>", "").replace("</DOCNO>", "").strip()
                # Retrieve contents of TEXT tag
                
                text = "".join(re.findall(text_regex, document))\
                        .replace("<TEXT>", "").replace("</TEXT>", "")\
                        .replace("\n", " ")
                text = text.lower()
                text = text.translate(str.maketrans('', '', string.punctuation))
                
                text_list = text.split()
                with open("stopwords.txt", "r") as a_file:
                    stopwords = []
                    for line in a_file:
                        stripped_word = line.strip()
                        stopwords.append(stripped_word)
                    wordlist  = [word for word in text_list if word.lower() not in stopwords]
                    
                #  lower case, punctuation, and stop-words removed.            
                #  count of all words with stop words removed
                #########################
                #  lastly term id mapping
                for w in wordlist:
                    if w not in termid_map:
                        termid_map[w] = tid_ctr
                        tid_ctr += 1
                    
                # produce token tuples below
                token_tuple = ()
                position = 1
                for w in wordlist:
                    # token tuple will have termid, docno, and positions of each term
                    token_tuple = (termid_map[w], docno, position)
                    index_dictionary[w].append(token_tuple)
                    position += 1
    return(index_dictionary)
