import numpy as np
import email
from np.random import permutation
import re

def read_file(fname):
    """ Lit un fichier compose d'une liste de emails, chacun separe par au moins 2 lignes vides."""
    f = open(fname,'rb')
    raw_file = f.read()
    f.close()
    raw_file = raw_file.replace(b'\r\n',b'\n')
    emails = raw_file.split(b"\n\n\nFrom")
    emails = [emails[0]] + [b"From" + x for x in emails[1:] ]
    return emails

def get_body(em):
    """ Recupere le corps principal de l'email """
    body = em.get_payload()
    if type(body) == list:
        body = body[0].get_payload()
    try:
        res = str(body)
    except Exception:
	 except Exception:
        res=""
    return res

def clean_body(s):
    """ Enleve toutes les balises html et tous les caracteres qui ne sont pas des lettres """
    patbal = re.compile('<.*?>',flags = re.S)
    patspace = re.compile('\W+',flags = re.S)
    return re.sub(patspace,' ',re.sub(patbal,'',s))

def get_emails_from_file(f):
    mails = read_file(f)
    return [ s for s in [clean_body(get_body(email.message_from_bytes(x))) for x in mails] if s !=""]
def split(liste, x):
    """split_indexes = np.random.randint.(0, len(liste) - 1, len(liste))"""
    split_indexes = np.random.randint.permutation(0, len(liste) - 1, len(liste))
  """  permut_split = permute (split_indexes)"""
    split_index = int((x/100)* len(liste))
    splitted_1 = [liste[split_indexes[i]] for i in range(split_index)]
    splitted_2 = [liste[split_indexes[i]] for i in range(split_index, len(liste))]
    return splitted_1, splitted_2
	


def histogram(mail_list):
    lengths = [len(mail) for mail in mail_list]
    bins = dict()
    for length in lengths:
        if length not in bins:
            bins[length] = 0
        bins[length] += 1
    return bins

def apprend_modele(spam,nonspam) : """ 2.3 """
    
   spamEmails= [(email, 'spam') for email in spam] 
        l= len(spamEmails)
            resSp= "P(X=",l,"|Y=1)"
            return resSp
   NoSpamEmails= [(email, 'NoSpam') for email in nonspam] 
        l= len(NoSpamEmails)   
            resNoSp= "P(X=",l,"|Y=-1)" 
            return resNoSp

def predit_email(emails,modele): """ indique pour un email son label i.e : si spam ou non spam """


def taille_email (email) :  """ 3.2"""
	compteur = 0;
	mot = false; """ pas de mot au debut """
	for i in range (len(email))
		car= ord(email[i]) """ ord:tronsformer au code ASCI"""
		if((car>=65 and car<=90) or (car>=97 and car<=122)) and not mot : """ si le caractere est un majuscule ou un miniscule"""
			compteur +=1;
			mot = True
		if (car==32) : """  32 en asci --> un espace donc mots uivant"""
			mot = False
	return compteur
			
def tailles_emails (emails): 
	l= list()
	for i in emails  """ pour chaq mail de la liste"""
		l.append(taille_email(i)
	return l
    
    

spam = get_emails_from_file("spam.txt" )
nospam = get_emails_from_file("nospam.txt")
spams_sizes = tailles_emails(spam)
nonspams_sizes = tailles_emails(nonspam)

