from bs4 import BeautifulSoup
import re
import pandas as pd
import numpy as np
import requests

#remote
#url = 'http://www.metacritic.com/browse/games/score/metascore/all/ps4?sort=desc'
#r  = requests.get(url)
#soup = BeautifulSoup(r.text)


#local
#html_doc_name = 'ps4_page1_21_12_2014.html'
#html_doc_name = 'ps4_page2_21_12_2014.html'
#################
#html_doc_name = 'xone_page1_21_12_2014.html'
#html_doc_name = 'xone_page2_21_12_2014.html'
#################
#html_doc_name = 'WiiU_page1_21_12_2014.html'
html_doc_name = 'WiiU_page2_21_12_2014.html'

f = open(html_doc_name,'r')
soup = BeautifulSoup(f)


#print(soup.prettify())


#all the interesting infor lies in this div
els = soup.find_all("div", class_="product_wrap")


#----------------------------Game--names
name_elements = [els[i].find_all("a",text=True) for i in range(len(els))]

pattern = re.compile('\n.*\n')

names = []
for i in range(len(name_elements)):
  match_obj = re.search(pattern,str(name_elements[i]))
  if match_obj != None:
   names.append(match_obj.group(0).strip())
  else:
    names.append(None)


#----------------------------Critic--scores
pattern = re.compile('metascore_w')
critic_scores = [els[i].find_all("div", class_=pattern) for i in range(len(els))]

critic_score_numbers = []
for score in critic_scores:

  match_obj = re.search(re.compile('>[0-9][0-9]<'),str(score))
  
  if match_obj != None:
   critic_score_numbers.append(match_obj.group(0)[1:-1])
  else:
    critic_score_numbers.append(None)
  
#----------------------------User--scores
pattern = re.compile('textscore')
user_scores = [els[i].find_all("span", class_=pattern) for i in range(len(els))]

user_score_numbers = []
for score in user_scores:

  match_obj = re.search(re.compile('>[0-9].[0-9]<'),str(score))
  
  
  if match_obj != None:
   user_score_numbers.append(match_obj.group(0)[1:-1])
  else:
    user_score_numbers.append(None)



#row_list = zip(names,critic_score_numbers,user_score_numbers)
print len(names)
print len(critic_score_numbers)
print len(user_score_numbers)

#replace None with np.nan
replace_None = lambda s : np.nan if s == None else s
names = map(replace_None,names)
critic_score_numbers = map(replace_None,critic_score_numbers)
user_score_numbers = map(replace_None,user_score_numbers)



df = pd.DataFrame({'names':names,'critics':critic_score_numbers,'users':user_score_numbers})
df.to_csv(html_doc_name[:-4]+'csv',index=False)

