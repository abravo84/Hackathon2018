# coding: utf-8
# encoding: utf-8    
'''
Created on Feb 8, 2018

@author: upf
'''
from bs4 import BeautifulSoup
import os, sys, re
from shutil import copyfile
from get_html_abstracts import add_one_dictionary, CORPUS_PATH
from nltk.tokenize import sent_tokenize
import string
import operator
from lib2to3.fixes.fix_input import context
from pip._vendor.lockfile import pidlockfile


INTRODUCTION = "INTRODUCTION"
OBJECTIVE = "OBJECTIVE"
METHODS = "METHODS"
RESULTS = "RESULTS"
CONCLUSIONS = "CONCLUSIONS"
RESULTS_CONCLUSIONS = "RESULTS_CONCLUSIONS"
UNDEFINED = "UNDEFINED"


def clear_label(text):
    
    text = text.replace("&amp;", "and").translate(None, string.punctuation)
    
    text = text.replace("á", "a")
    text = text.replace("é", "e")
    text = text.replace("í", "i")
    text = text.replace("ó", "o")
    text = text.replace("ú", "u")
    
    text = text.replace("Á", "a")
    text = text.replace("É", "e")
    text = text.replace("Í", "i")
    text = text.replace("Ó", "o")
    text = text.replace("Ú", "u")
    
    text = text.lower().strip()
    return text


def is_kw(kw_list, text):
    
    for l in kw_list:
        if l in text:
            return True
        
    return False

def get_norm_label_es(text, last_label):
    
    intro_kw = []
    intro_kw.append("introducion")
    intro_kw.append("introduccion")
    intro_kw.append("motivo")
    intro_kw.append("antecedente")
    intro_kw.append("contexto")
    intro_kw.append("fundamento")
    intro_kw.append("justificaci")
    intro_kw.append("hipotesis")
    intro_kw.append("resumen")
    intro_kw.append("proposito")
    
    objective_kw = []
    objective_kw.append("objetivo")
    objective_kw.append("finalidad")
    
    methods_kw = []
    methods_kw.append("metodo")
    #methods_kw.append("método")
    methods_kw.append("estudio")
    methods_kw.append("paciente")
    methods_kw.append("material")
    methods_kw.append("diseño")
    methods_kw.append("caso")
    methods_kw.append("ambito")
    methods_kw.append("intervenci")
    methods_kw.append("sujeto")
    methods_kw.append("escenario")
    methods_kw.append("m and m")
    methods_kw.append("participante")
    methods_kw.append("transfondo")
    methods_kw.append("desarrollo")
    methods_kw.append("emplazamiento")
    methods_kw.append("mediciones")
    
    
    
    results_kw = []
    results_kw.append("result")
    
    
    conclusions_kw = []
    conclusions_kw.append("conclusion")
    conclusions_kw.append("discusion")
    conclusions_kw.append("debate")
    conclusions_kw.append("comentario")
    
    if is_kw(intro_kw, text):
        return INTRODUCTION
    
    if is_kw(methods_kw, text):
        return METHODS
    
    if is_kw(objective_kw, text):
        return OBJECTIVE
    
    if is_kw(results_kw, text) and not is_kw(conclusions_kw, text):
        return RESULTS
    
    if is_kw(conclusions_kw, text) and not is_kw(results_kw, text):
        return CONCLUSIONS
    
    if is_kw(conclusions_kw, text) and is_kw(results_kw, text):
        return RESULTS_CONCLUSIONS
    
    return last_label

def get_norm_label_en(text, last_label):
    
    intro_kw = []
    intro_kw.append("introduction")
    intro_kw.append("background")
    intro_kw.append("introducion")
    intro_kw.append("introduccion")
    intro_kw.append("purpose")
    intro_kw.append("antecedent")
    intro_kw.append("rationale")
    intro_kw.append("hypothesi")
    intro_kw.append("fundamentals")
    intro_kw.append("abstract")
    intro_kw.append("context")
    intro_kw.append("propose")
    intro_kw.append("justificat")
    intro_kw.append("bacground")
    intro_kw.append("backgound")
    intro_kw.append("backgraund")
    intro_kw.append("pourpose")
    intro_kw.append("bakground")
    intro_kw.append("bakcground")
    
    
    objective_kw = []
    objective_kw.append("aim")
    objective_kw.append("object")
    objective_kw.append("objetive")
    objective_kw.append("goal")
    objective_kw.append("alm")
    
    methods_kw = []
    methods_kw.append("method")
    methods_kw.append("procedure")
    methods_kw.append("patient")
    methods_kw.append("participant")
    methods_kw.append("case")
    methods_kw.append("design")
    methods_kw.append("material")
    methods_kw.append("scope")
    methods_kw.append("subject")
    methods_kw.append("setting")
    methods_kw.append("metodo")
    methods_kw.append("methord")
    methods_kw.append("methoud")
    methods_kw.append("metthod")
    methods_kw.append("environment")
    methods_kw.append("m and m")
    methods_kw.append("subjetc")
    methods_kw.append("study")
    
    
    results_kw = []
    results_kw.append("result")
    results_kw.append("outcome")
    
    conclusions_kw = []
    conclusions_kw.append("conclusion")
    conclusions_kw.append("discussion")
    conclusions_kw.append("conlcusion")
    conclusions_kw.append("discusion")
    conclusions_kw.append("conclussion")
    conclusions_kw.append("summary")
    conclusions_kw.append("comment")
    conclusions_kw.append("debate")
    conclusions_kw.append("conclusi")
    conclusions_kw.append("final considerations")
    
    if is_kw(intro_kw, text):
        return INTRODUCTION
    
    if is_kw(methods_kw, text):
        return METHODS
    
    if is_kw(objective_kw, text):
        return OBJECTIVE
    
    if is_kw(results_kw, text) and not is_kw(conclusions_kw, text):
        return RESULTS
    
    if is_kw(conclusions_kw, text) and not is_kw(results_kw, text):
        return CONCLUSIONS
    
    if is_kw(conclusions_kw, text) and is_kw(results_kw, text):
        return RESULTS_CONCLUSIONS
    
    return last_label
    
def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)

def create_documents_en(input_path, opath):
    
    #if not os.path.exists(output_folder):
    #    os.makedirs(output_folder)
    
    skip_abst = []
    
    skip_abst.append("S1130-63432013000200003")
    skip_abst.append("S1134-80462013000500004")
    skip_abst.append("S1135-76062015000100004")
    
    
    ofile = open(opath, "w")
    
    
    docs_split = open(input_path).read().split("\n\n")
    n_abts = 0
    
    labels_dict = {}
    total_sent = 0
    
    #reg_pat = r'<b>[a-zA-Z0-9:-]</b>'
    
    reg_pat_b = re.compile(r'\.[\s]?<b>(.*?)</b>')
    reg_pat_b2 = re.compile(r'[\s]?<b>(.*?)</b>')
    
    #reg_pat_i = re.compile(r'\.[\s]?[<b>\s]*<i>(.*?)</i>[<:\.\s]')
    
    reg_pat_i = re.compile(r'\.[\s]*[<b>\s]*<i>(.*?)</i>')
    
    tag_dict = {}
    MAX_LEN=40
    for doc in docs_split[:-1]:
        fields = doc.split("\n")
        pid = fields[0]
        title = fields[1]
        clean_abstract =fields[2]
        html_abstract = fields[3]
        abstract_lines_split = sent_tokenize(clean_abstract.decode("utf-8"))
        total_sent += len(abstract_lines_split)
        
        if pid in skip_abst:
            continue
        
        # and not "<i>" in html_abstract_corr[:30]
        
        html_abstract_corr = ". " + html_abstract
        count = 0
        
        lines = []
        labels = []
        if reg_pat_b.match(html_abstract_corr[:MAX_LEN]) and not "<i>" in html_abstract_corr[:MAX_LEN].split("</b>"[0]):
        
            matches = reg_pat_b.finditer(html_abstract_corr)
        
            
            for m in matches:
                
                
                #ofile.write(m.group(0) + "\n")
                #ofile.write(m.group(1) + "\n\n")
                label = clear_label(m.group(1))
                
                if hasNumbers(label) or not len(label):
                    continue
                if "opinion" in label:
                    continue
                if "b painful" in label:
                    continue
                
                lines.append(m.group(0) )
                labels.append(label)
                add_one_dictionary(tag_dict, label)
                count+=1
            
        elif reg_pat_i.match(html_abstract_corr[:MAX_LEN]):
            matches = reg_pat_i.finditer(html_abstract_corr)
        
            for m in matches:
                #print m.group(0)
                #print m.group(1)
                #print ""
                
                label = clear_label(m.group(1))
                if hasNumbers(label) or not len(label):
                    continue
                if "opinion" in label:
                    continue
                if "b painful" in label:
                    continue
                lines.append(m.group(0) )
                labels.append(label)
                add_one_dictionary(tag_dict, label)
                count+=1
        #else:
        #    print pid
        #    print html_abstract
                   
        if count >= 3:
            ofile.write(pid + "\n")
            i=0
            for l in lines:
                if i == 0:
                    last_label = UNDEFINED
                
                last_label = get_norm_label_en(labels[i], last_label)
                ofile.write(l + "\t" + last_label + "\n")
                i+=1
            ofile.write("\n")
        """ 
        if reg_pat_b.match(html_abstract_corr[:MAX_LEN]) and not "<i>" in html_abstract_corr[:MAX_LEN].split("</b>"[0]):
        
            matches = reg_pat_b2.finditer(html_abstract_corr)
        
            ofile.write(pid + "\n")
            for m in matches:
                ofile.write(m.group(0) + "\n")
                #ofile.write(m.group(1) + "\n\n")
                label = clear_label(m.group(1))
                add_one_dictionary(tag_dict, label)
                count+=1
            
            ofile.write( "\n")   
        """
        #if count < 3: 
        #    print pid
        #    print html_abstract
            
            
        """
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
        """
    for k in sorted(tag_dict.items(), key=operator.itemgetter(1), reverse=True):
        print k[0], k[1]#tag_dict[k]
    
    print len(tag_dict)
    print "total_sent",  total_sent  
    ofile.close()


def create_documents_es(input_path, opath):
    
    #if not os.path.exists(output_folder):
    #    os.makedirs(output_folder)
    
    skip_abst = []
    skip_abst.append("S1130-63432013000200003")
    skip_abst.append("S1134-80462013000500004")
    skip_abst.append("S1135-76062015000100004")
    
    ofile = open(opath, "w")
    
    
    docs_split = open(input_path).read().split("\n\n")
    n_abts = 0
    
    labels_dict = {}
    total_sent = 0
    
    #reg_pat = r'<b>[a-zA-Z0-9:-]</b>'
    
    reg_pat_b = re.compile(r'\.[\s]?<b>(.*?)</b>')
    reg_pat_b2 = re.compile(r'[\s]?<b>(.*?)</b>')
    
    #reg_pat_i = re.compile(r'\.[\s]?[<b>\s]*<i>(.*?)</i>[<:\.\s]')
    
    reg_pat_i = re.compile(r'\.[\s]*[<b>\s]*<i>(.*?)</i>')
    
    tag_dict = {}
    MAX_LEN=40
    for doc in docs_split[:-1]:
        fields = doc.split("\n")
        pid = fields[0]
        title = fields[1]
        clean_abstract =fields[2]
        html_abstract = fields[3]
        abstract_lines_split = sent_tokenize(clean_abstract.decode("utf-8"))
        total_sent += len(abstract_lines_split)
        
        if pid in skip_abst:
            continue
        
        # and not "<i>" in html_abstract_corr[:30]
        
        html_abstract_corr = ". " + html_abstract
        count = 0
        
        lines = []
        labels = []
        if reg_pat_b.match(html_abstract_corr[:MAX_LEN]) and not "<i>" in html_abstract_corr[:MAX_LEN].split("</b>"[0]):
        
            matches = reg_pat_b.finditer(html_abstract_corr)
        
            
            for m in matches:
                
                
                #ofile.write(m.group(0) + "\n")
                #ofile.write(m.group(1) + "\n\n")
                label = clear_label(m.group(1))
                
                if hasNumbers(label) or not len(label):
                    continue
                #if "opinion" in label:
                #    continue
                if "b datos" in label:
                    continue
                
                lines.append(m.group(0) )
                labels.append(label)
                add_one_dictionary(tag_dict, label)
                count+=1
            
        elif reg_pat_i.match(html_abstract_corr[:MAX_LEN]):
            matches = reg_pat_i.finditer(html_abstract_corr)
        
            for m in matches:
                #print m.group(0)
                #print m.group(1)
                #print ""
                
                label = clear_label(m.group(1))
                if hasNumbers(label) or not len(label):
                    continue
                #if "opinion" in label:
                #    continue
                if "b datos" in label:
                    continue
                lines.append(m.group(0) )
                labels.append(label)
                add_one_dictionary(tag_dict, label)
                count+=1
        #else:
        #    print pid
        #    print html_abstract
                   
        if count >= 3:
            ofile.write(pid + "\n")
            i=0
            for l in lines:
                if i == 0:
                    last_label = UNDEFINED
                
                last_label = get_norm_label_es(labels[i], last_label)
                ofile.write(l + "\t" + last_label + "\n")
                i+=1
            ofile.write("\n")
        #if count < 3: 
        #    print pid
        #    print html_abstract
            
    for k in sorted(tag_dict.items(), key=operator.itemgetter(1), reverse=True):
        print k[0], k[1]#tag_dict[k]
    
    print len(tag_dict)
    print "total_sent",  total_sent  
    ofile.close()
    
def stats_log_file_en(opath):
    
    abst_list = open(opath).read().split("\n\n")[:-1]
    
    print len(abst_list)
    
    label_count = {}
    
    first_label = {}
    for abst in abst_list:
        abst_split = abst.split("\n")
        pid = abst_split[0]
        
        i = 0
        for l in abst_split[1:]:
            
            label = l.strip().split("\t")[-1]
            if i==0:
                add_one_dictionary(first_label, label)
            i+=1
            label_count[pid + "#" + label] = 1
        
        
    print first_label
    label_count_true = {}
    for k in label_count:
        add_one_dictionary(label_count_true, k.split("#")[-1])
    for k in sorted(label_count_true.items(), key=operator.itemgetter(1), reverse=True):
        print k[0], k[1]#tag_dict[k]
        
        
def proc_log_en(input_path,log_path, docs_path):
    abst_list = open(log_path).read().split("\n\n")[:-1]
    
    info_labels = {}
    
    for abst in abst_list:
        abst_split = abst.split("\n")
        pid = abst_split[0]
        info_labels[pid] = abst
    
    ofile = open(docs_path, "w")
    ofile.write("<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?>\n\n<corpus>\n")
    docs_split = open(input_path).read().split("\n\n")
    for doc in docs_split[:-1]:
        fields = doc.split("\n")
        pid = fields[0]
        title = fields[1]
        clean_abstract =fields[2]
        html_abstract = fields[3]
        
        if not pid in info_labels:
            continue
        
        label_info = info_labels[pid].split("\n")
        
        """
        S0211-57352010000300002
        . <b>Introduction:</b>    INTRODUCTION
        . <b>Material and Method:</b>    METHODS
        . <b>Results:</b>    RESULTS
        . <b>Conclusions:</b>    CONCLUSIONS
        """
        
        new_line = []
        new_line.append("<article id=\"%s\">"%(pid))
        
        new_line.append("<title>%s</title>"%(title))
        new_line.append("<abstract>")
        for li in label_info[1:]:
            label = li.split("\t")[1]
            tag = li.split("\t")[0]
            
            if tag.startswith(". "):
                tag = tag[2:]
            
            if tag.startswith("."):
                tag = tag[1:]
                
            #html_abstract = BeautifulSoup(html_abstract, "lxml").text.strip()
            html_abstract = html_abstract.replace(tag, "</section>\n<section label=\"%s\">"%(label) )
        
        new_line.append(html_abstract[len("</section>\n"):] .replace("</p>", "").replace("</b>", "").replace("<bsaa>", "").replace("<i>", "").replace("</i>", ""))
        
        #abstract_lines_split = sent_tokenize(clean_abstract.decode("utf-8"))
        new_line.append("</section>\n</abstract>\n</article>\n")
        
        for l in new_line:
            ofile.write(l + "\n")
    ofile.write("</corpus>")
    ofile.close()

def sentence_splitting_en(docs_path, output_path):
    
    xml_text = open(docs_path).read()
    soup = BeautifulSoup(xml_text, 'xml')
    
    articles = soup.find_all("article")
    
    ofile = open(output_path, "w")
    count = 0
    for article in articles:
        new_line = []
        new_line.append( article["id"])
        #print article["id"]
        count+=1
        sections = article.find_all("section")
        nsent = 0
        title= article.find("title")
        #print nsent, "TITLE", title.text
        new_line.append( "TITLE" +"\t"+ title.text)
        for section in sections:
            #print section["label"]
            #sect_txt =  section.text.strip()
            sect_txt = BeautifulSoup(section.text, "lxml").text.strip()
            if sect_txt.startswith(": ") or sect_txt.startswith(". "):
                sect_txt = sect_txt[2:]
                
            sentences = sent_tokenize(sect_txt)
            
            for sent in sentences:
                nsent+=1
                #print nsent, section["label"], sent
                new_line.append(section["label"] +"\t"+ sent)
        final_line = []
        final_line.append(article["id"])
        i=-1
        for nl in new_line[1:]:
            i+=1
            fields = nl.split("\t")
            params = []
            params.append(fields[0])
            params.append(fields[1])
            params.append(str(len(fields[1])))
            params.append(str(i))
            params.append(str(nsent))
            params.append(str(i/float(nsent)))
            final_line.append("\t".join(params))
        
        for fl in final_line:
            ofile.write(fl.encode("utf-8") + "\n")
        ofile.write("\n")
            
    print count
if __name__ == '__main__':
    
    lang = "en"
    
    input_path = os.path.join(CORPUS_PATH,"raw_abstracts_%s.txt"%(lang.upper()))
    output_folder = os.path.join(CORPUS_PATH,"raw_abstracts_%s.txt"%(lang.upper()))
    
    opath = os.path.join(CORPUS_PATH,"tags_%s.log"%(lang.upper()))
    #create_documents_en(input_path, opath)
    
    
    #stats_log_file_en(opath)
    
    
    docs_path = os.path.join(CORPUS_PATH,"abstracts_%s.xml"%(lang.upper()))
    
    #proc_log_en(input_path, opath, docs_path)
    
    
    
    sentences_path = os.path.join(CORPUS_PATH,"sentences_%s.txt"%(lang.upper()))
    sentence_splitting_en(docs_path, sentences_path)
    
    
    
    
    
    lang = "es"
    input_path = os.path.join(CORPUS_PATH,"raw_abstracts_%s.txt"%(lang.upper()))
    output_folder = os.path.join(CORPUS_PATH,"raw_abstracts_%s.txt"%(lang.upper()))
    
    opath = os.path.join(CORPUS_PATH,"tags_%s.log"%(lang.upper()))
    #create_documents_es(input_path, opath)
    
    #stats_log_file_en(opath)
    
    docs_path = os.path.join(CORPUS_PATH,"abstracts_%s.xml"%(lang.upper()))
    
    #proc_log_en(input_path, opath, docs_path)
    
    sentences_path = os.path.join(CORPUS_PATH,"sentences_%s.txt"%(lang.upper()))
    sentence_splitting_en(docs_path, sentences_path)
    