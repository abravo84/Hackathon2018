'''
Created on Feb 8, 2018

@author: upf
'''
from bs4 import BeautifulSoup
import os, sys, re
from shutil import copyfile
from get_html_abstracts import add_one_dictionary, CORPUS_PATH
from nltk.tokenize import sent_tokenize




def create_documents(input_path, output_folder):
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    
    docs_split = open(input_path).read().split("\n\n")
    n_abts = 0
    
    labels_dict = {}
    total_sent = 0
    for doc in docs_split[:-1]:
        fields = doc.split("\n")
        pid = fields[0]
        title = fields[1]
        clean_abstract =fields[2]
        html_abstract = fields[3]
        abstract_lines_split = sent_tokenize(clean_abstract.decode("utf-8"))
        total_sent += len(abstract_lines_split)
        continue
        html_abstract = html_abstract.replace("<b>", "\n<section name=").replace("<i>", "").replace("</i>", "").replace("</b>", "").replace(":", ">\n").replace(".", ">\n")
        abstract_lines_split = html_abstract.split("\n")
        
        
        #ofile.write("<article id="+pid+">\n<title>\n" + title.encode("utf8") + "\n</title>\n")
        
        doc_text = "<article id="+pid+">\n<title>\n" + title + "\n</title>\n"
        n_abts+=1
        print pid, n_abts
        #ofile.write("<abstract>\n")
        doc_text += "<abstract>\n"
        sec_flag =False
        for l in abstract_lines_split:
            if not len(l):
                continue
            #ofile.write(l.strip().replace("</p>", "")+"\n")
            doc_text += l.strip().replace("</p>", "")+"\n"
            if "<section" in l:
                sec_flag = True
                add_one_dictionary(labels_dict, l)
            else:
                if sec_flag:
                    #ofile.write("</section>\n")
                    doc_text += "</section>\n"
                sec_flag=False
        #ofile.write("</abstract>\n</article>\n\n")
        doc_text += "</abstract>\n</article>\n\n"
        #ofile.flush()
        #print doc_text
    print "total_sent",  total_sent  
        
if __name__ == '__main__':
    
    lang = "es"
    
    input_path = os.path.join(CORPUS_PATH,"raw_abstracts_%s.txt"%(lang.upper()))
    output_folder = os.path.join(CORPUS_PATH,"raw_abstracts_%s.txt"%(lang.upper()))
    
    create_documents(input_path, output_folder)