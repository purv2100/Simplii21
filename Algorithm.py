#!/usr/bin/env python
# coding: utf-8

# In[31]:


jsn = [{
        "creat_consum": "NA",
        "deadline": "2021-09-30T15:00",
        "difficulty": "3",
        "estimate": "2",
        "id": "73IA2",
        "quant_verbal": "NA",
        "task_name": "SE Project",
        "task_type": "physical"
      },
      {
        "creat_consum": "NA",
        "deadline": "2021-09-29T23:04",
        "difficulty": "3",
        "estimate": "5",
        "id": "DXCIN",
        "quant_verbal": "NA",
        "task_name": "GHC ",
        "task_type": "physical"
      },
      {
        "creat_consum": "3",
        "deadline": "2021-09-30T21:30",
        "difficulty": "4",
        "estimate": "5",
        "id": "LOUHF",
        "quant_verbal": "3",
        "task_name": "Interview",
        "task_type": "intellectual"
      },
      {
        "creat_consum": "NA",
        "deadline": "2021-09-29T23:05",
        "difficulty": "2",
        "estimate": "2",
        "id": "NKJGR",
        "quant_verbal": "NA",
        "task_name": "IP Homework ",
        "task_type": "physical"
      }]


# In[49]:


jsn_physical = list(filter(lambda x : x['task_type'] == "physical",jsn))
jsn_intellectual = list(filter(lambda x : x['task_type'] == "intellectual",jsn))


# In[52]:


jsn_intellectual.sort(key=lambda x: (x['deadline'],x["difficulty"],x["estimate"]))


# In[53]:


jsn_physical.sort(key=lambda x: (x['deadline'],x["difficulty"],x["estimate"]))


# In[54]:


jsn_intellectual


# In[55]:


jsn_physical


# In[ ]:




