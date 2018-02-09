# coding: utf-8
# encoding: utf-8    
'''
Created on Dec 12, 2017

@author: upf
'''

import os, sys
from nltk.corpus.reader import lin
import urllib2, re
from bs4 import BeautifulSoup
from nltk.tokenize import sent_tokenize

CORPUS_PATH = "/home/upf/corpora/SciELO_corpus"

SCIELO_HTML_URL = "http://scielo.isciii.es/scielo.php?script=sci_arttext&pid=%s"

SCIELO_HTML_ABSTRACT_URL = "http://scielo.isciii.es/scielo.php?script=sci_abstract&pid=%s&lng=%s&nrm=iso"

SCIELO_XML_URL = "http://scielo.isciii.es/scieloOrg/php/articleXML.php?pid=%s&lang=es"

def get_html(url):
    i = 0
    while True:
        try:
            i+=1
            if i>15:
                break
            usock = urllib2.urlopen(url, timeout = 100)
            break
        except:
            continue
    
    if i > 5:
        print "ERROR", url
        return None
    data = usock.read()
    usock.close()
    return data  


def create_article_list():
    fulltext_path = os.path.join(CORPUS_PATH, "full_texts", "clean_raw_text")
    
    count = 0
    
    output_path = os.path.join(CORPUS_PATH,"articles_list.txt")
    
    ofile = open(output_path, "w")
    
    for subfolder in sorted(os.listdir(fulltext_path)):
        subfolder_path = os.path.join(fulltext_path, subfolder)
        for filename in sorted(os.listdir(subfolder_path)):
            filename_path = os.path.join(subfolder_path, filename)
            for lin in file(filename_path):
                break
            lin = lin.lower()
            if lin.startswith("articulo") or lin.startswith("artículo") or lin.startswith("original"):
                count+=1
                ofile.write(filename.replace(".txt", "") + "\n")
    
    print count
    
    ofile.close()


def add_one_dictionary(dictionary, key):
    if key in dictionary:
        aux = dictionary.get(key)
        dictionary[key] = aux + 1
    else:
        dictionary[key] = 1
    return dictionary  



def get_abstracts_from_html(art_list_path, lang, raw_output_path, log_path):
    """
    if not os.path.isfile(raw_output_path):
        rawfile = open(raw_output_path, "w")
        rawfile.close()
    
    if not os.path.isfile(log_path):
        olog = open(log_path, "w")
        olog.close()
    """
    done_dict = {}
    #for lin in file(log_path):
    #    done_dict[lin.strip()]= 1
    
    olog = open(log_path, "w")
    rawfile   = open(raw_output_path, "w") 
    n_abts = 0
    
    
    stop = True
    for lin in file(art_list_path):
        
        pid = lin.strip()
        
        print "---> ", pid
        if pid in done_dict:
            continue
        
        #if pid == "S0213-91112015000300008":
        #    stop = False

        
        #if stop:
        #    continue
        
        url = SCIELO_HTML_ABSTRACT_URL%(pid, lang)
        html_text = get_html(url)
        
        if not html_text:
            msg = "NOT HTML TEXT"
            olog.write(pid + "\t" + msg + "\n")
            continue
        
        soup = BeautifulSoup(html_text, 'lxml')
        
        text_set = soup.find_all('p',attrs={'xmlns':''} )
        title, abstract = get_abstracts_from_xml(pid, lang)
        
        if abstract==None:
            msg = "NOT ABSTRACT"
            olog.write(pid + "\t" + msg + "\n")
            continue
        
        is_abstr = False
        abstract_lines_split = []
        for t in text_set:
            t = str(t).strip().replace("<p xmlns=\"\">", "")
            if t.startswith("<a href=\"http://scielo.isciii.es/"):
                continue
            if "<b>" in t[:10]:
                cleantext = BeautifulSoup(t, "lxml").text
                abstract_lines_split = sent_tokenize(cleantext)
                
                for l in abstract_lines_split:
                    
                    if l.strip() in abstract and len(l) >30:
                        is_abstr=True
                        break
                    
            if is_abstr:
                n_abts+=1
                print pid, n_abts
                rawfile.write(pid + "\n")
                rawfile.write(title.encode("utf8") + "\n")
                rawfile.write(abstract.encode("utf8") + "\n")
                rawfile.write(t + "\n\n")
                rawfile.flush()
                break
        
        
    rawfile.close()    
    olog.close()   

def get_abstracts_from_html_old(art_list_path, lang, raw_output_path, output_path, log_path):
    
    
    if not os.path.isfile(output_path):
        ofile = open(output_path, "w")
        ofile.close()
        
    ofile = open(output_path, "a")
    
    
    if not os.path.isfile(raw_output_path):
        rawfile = open(raw_output_path, "w")
        rawfile.close()
    
    rawfile   = open(raw_output_path, "a")  
        
      
    if not os.path.isfile(log_path):
        olog = open(log_path, "w")
        olog.close()
    
    done_dict = {}
    for lin in file(log_path):
        done_dict[lin.strip()]= 1
    
    olog = open(log_path, "a")
    
    n_abts = 0
    
    labels_dict = {}
    
    for lin in file(art_list_path):
        
        pid = lin.strip()
        if pid in done_dict:
            continue
        #pid = "S1699-695X2008000100005"
        
        url = SCIELO_HTML_ABSTRACT_URL%(pid, lang)
        html_text = get_html(url)
        
        if not html_text:
            msg = "NOT HTML TEXT"
            olog.write(pid + "\t" + msg + "\n")
            continue
        
        soup = BeautifulSoup(html_text, 'lxml')
        
        text_set = soup.find_all('p',attrs={'xmlns':''} )
        title, abstract = get_abstracts_from_xml(pid, lang)
        
        if abstract==None:
            msg = "NOT ABSTRACT"
            olog.write(pid + "\t" + msg + "\n")
            continue
        
        
        
        is_abstr = False
        abstract_lines_split = []
        for t in text_set:
            t = str(t).strip().replace("<p xmlns=\"\">", "")
            if t.startswith("<a href=\"http://scielo.isciii.es/"):
                continue
            if "<b>" in t[:10]:
                t_n = t.replace("<b>", "\n<section name=").replace("<i>", "").replace("</i>", "").replace("</b>", "").replace(":", ">\n").replace(".", ">\n")
                abstract_lines_split = t_n.split("\n")
                for l in abstract_lines_split:
                    if l.strip().decode("utf8") in abstract and len(l) >30:
                        is_abstr=True
                        break
            if is_abstr:
                rawfile.write(pid + "\n")
                rawfile.write(t + "\n\n")
                break
        
        
        if is_abstr:
            #print title
            ofile.write("<article id="+pid+">\n<title>\n" + title.encode("utf8") + "\n</title>\n")
            n_abts+=1
            print pid, n_abts
            ofile.write("<abstract>\n")
            sec_flag =False
            for l in abstract_lines_split:
                if not len(l):
                    continue
                ofile.write(l.strip().replace("</p>", "")+"\n")
                if "<section" in l:
                    sec_flag = True
                    add_one_dictionary(labels_dict, l)
                else:
                    if sec_flag:
                        ofile.write("</section>\n")
                    sec_flag=False
            ofile.write("</abstract>\n</article>\n\n")
            ofile.flush()
            msg = "OK!!"
            olog.write(pid + "\t" + msg + "\n")
            olog.flush()
            continue
            
            
            
        msg = "OK BUT NO ABSTRACT WITH SECTIONS"
        olog.write(pid + "\t" + msg + "\n")
        olog.flush()
            #print "..."
            #print t#.encode("utf8")
            #print "...................."
        
        #html_text = html_text.split("<!--version=html-->")[1].split("\n")[0].replace("<P", "<p").replace("/P>", "/p>").replace("</p>", "\n")
        #html_text_split = html_text.split("\n")
        
        
        
        #print BeautifulSoup(html_text, "lxml").text
    olog.write("-----------------------" + "\n")  
    for k in labels_dict:
        print k, labels_dict[k]
        olog.write(k + "\t" +str(labels_dict[k]) + "\n")  
    ofile.close()   
        
    olog.close()   
        
def get_abstracts_from_xml(pid, lang):
    
    url = SCIELO_XML_URL%(pid)
    xml_text = get_html(url)
    #soup = BeautifulSoup(xml_text, 'html.parser')
    
    
    soup = BeautifulSoup(xml_text, 'xml')
    text = soup.find('abstract',attrs={'xml:lang':lang})
    
    title = soup.find('article-title',attrs={'xml:lang':lang})
    
    if text == None:
        print pid, "NO", title, text
        return None, None

    return title.text, text.text


def create_documents(input_path, output_folder):
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    
    docs_split = open(input_path).read().split("\n\n")
    n_abts = 0
    
    labels_dict = {}
    for doc in docs_split:
        fields = doc.split("\n")
        
        pid = fields[0]
        title = fields[1]
        clean_abstract =fields[3]
        html_abstract = fields[4]
        
        
        html_abstract = html_abstract.replace("<b>", "\n<section name=").replace("<i>", "").replace("</i>", "").replace("</b>", "").replace(":", ">\n").replace(".", ">\n")
        abstract_lines_split = html_abstract.split("\n")
        
        
        #ofile.write("<article id="+pid+">\n<title>\n" + title.encode("utf8") + "\n</title>\n")
        
        doc_text = "<article id="+pid+">\n<title>\n" + title.encode("utf8") + "\n</title>\n"
        n_abts+=1
        print pid, n_abts
        #ofile.write("<abstract>\n")
        doc_text += "<abstract>\n"
        sec_flag =False
        for l in abstract_lines_split:
            if not len(l):
                continue
            #ofile.write(l.strip().replace("</p>", "")+"\n")
            print l.strip().replace("</p>", "")+"\n"
            doc_text += l.strip().replace("</p>", "")+"\n"
            if "<section" in l:
                sec_flag = True
                add_one_dictionary(labels_dict, l)
            else:
                if sec_flag:
                    #ofile.write("</section>\n")
                    print "</section>\n"
                    doc_text += "</section>\n"
                sec_flag=False
        #ofile.write("</abstract>\n</article>\n\n")
        doc_text += "</abstract>\n</article>\n\n"
        #ofile.flush()
    

if __name__ == '__main__':
    
    #create_article_list()
    
    art_list_path = os.path.join(CORPUS_PATH,"articles_list.txt")
    
    lang = "es"
    
    
    raw_output_path = os.path.join(CORPUS_PATH,"raw_abstracts_%s.txt"%(lang.upper()))
    log_path = os.path.join(CORPUS_PATH,"abstracts_labels_%s.log"%(lang.upper()))
    get_abstracts_from_html(art_list_path, lang,raw_output_path, log_path)
    
    
    output_path = os.path.join(CORPUS_PATH,"abstracts_labels_%s.txt"%(lang.upper()))
            