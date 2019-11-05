#!/usr/bin/env python
# coding: utf-8

# # Segmenting and Clustering Neighborhoods in Toronto
# 

# ## 1:- Webscraping List of postal codes of Canada from wikipedia.

#  Wikipedia page - https://en.wikipedia.org/wiki/List_of_postal_codes_of_Canada:_M

# In[12]:


import numpy as np
import pandas as pd

import bs4 as bs
import lxml.html as lh
import requests
import urllib.request


# In[13]:


url = "https://en.wikipedia.org/wiki/List_of_postal_codes_of_Canada:_M"


# In[14]:


# Using BS4 as suggested in Assignment.
def scrape_table_bs4(cname,cols):
    page  = urllib.request.urlopen(url).read()
    soup  = bs.BeautifulSoup(page,'lxml')
    table = soup.find("table",class_=cname)
    header = [head.findAll(text=True)[0].strip() for head in table.find_all("th")]
    data   = [[td.findAll(text=True)[0].strip() for td in tr.find_all("td")]
              for tr in table.find_all("tr")]
    data    = [row for row in data if len(row) == cols]
    raw_df = pd.DataFrame(data,columns=header)
    return raw_df

# Parsing using xpath.
def scrape_table_lxml(XPATH,cols):
    page = requests.get(url)
    doc = lh.fromstring(page.content)
    table_content = doc.xpath(XPATH)
    for table in table_content:
        headers = [th.text_content().strip() for th in table.xpath('//th')]
        headers = headers[0:3]
        data    = [[td.text_content().strip() for td in tr.xpath('td')] 
                   for tr in table.xpath('//tbody/tr')]
        data    = [row for row in data if len(row) == cols]
        raw_df = pd.DataFrame(data,columns=headers)
        return raw_df


# In[15]:


#Test in beautifulSoup
raw_TorontoPostalCodes = scrape_table_bs4("wikitable",3)

#Test in lxml ( for xpath based extraction)
#raw_TorontoPostalCodes = scrape_table_lxml("/html/body/div[3]/div[3]/div[4]/div/table[1]",3)

print("# Toronto Postal codes stored in data")
print(raw_TorontoPostalCodes.info(verbose=True))


# ## Data Preprocessing(Cleaning)
# ### Raw data contains some unwanted entries and need cleanup
#   * Drop/ignore cells with un-assigned boroughs.
#   * If a cell has a borough but a Not assigned neighborhood, then the neighborhood will be the same as the borough.
#   * Group the table by PostalCode/Borough, Neighbourhood belonging to same borough will be combined in 'Neighbourhood' column as separated with 'comma'.

# In[16]:


# Ignoring cells with a borough that has Not assigned.
TorontoPostalCodes=raw_TorontoPostalCodes[~raw_TorontoPostalCodes['Borough'].isin(['Not assigned'])]

# Sort and Reset index.
TorontoPostalCodes=TorontoPostalCodes.sort_values(by=['Postcode','Borough','Neighbourhood'], ascending=[1,1,1]).reset_index(drop=True)

# Replecing Neighbourhood as Borought where Neighbourhood == Not assigned.
TorontoPostalCodes.loc[TorontoPostalCodes['Neighbourhood'] == 'Not assigned', ['Neighbourhood']] = TorontoPostalCodes['Borough']
check_unassigned_post_state_sample = TorontoPostalCodes.loc[TorontoPostalCodes['Borough'] == 'Queen\'s Park']
#print('DEBUG:',check_unassigned_post_state_sample) ; # Print sample borough problem post state

# More than one neighborhood can exist in one postal code area. 
# For example, in the table on the Wikipedia page, you will notice that M5A is listed twice 
# and has two neighborhoods: Harbourfront and Regent Park. 
# These two rows will be combined into one row with the neighborhoods separated with a comma.
# -----------------------------------------------------
TorontoPostalCodes = TorontoPostalCodes.groupby(['Postcode','Borough'])['Neighbourhood'].apply(', '.join).reset_index()


# In[19]:


TorontoPostalCodes.head()


# ### printing the number of rows of my dataframe.

# In[26]:


TorontoPostalCodes.shape


# In[27]:


TorontoPostalCodes.to_csv('Toronto.TASK_1_df.csv',index=False)


# In[ ]:





# In[ ]:




