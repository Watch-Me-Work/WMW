#!/usr/bin/env python
# coding: utf-8

# In[2]:


from bs4 import BeautifulSoup
import requests


# In[18]:


url = "https://docs.google.com/document/d/1ec-GYa0OVgPAnTBupiRDl4JB9Jpiu8H2tUSPN2-VIhM/edit"


# In[34]:


result = requests.get(url)

c = result.content


# In[35]:


soup = BeautifulSoup(c)


# In[36]:


meta = soup.find("meta",{"property":"og:description"})


# In[37]:


print(meta["content"])


# In[ ]:




