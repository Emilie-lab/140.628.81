#####
import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# Streamlit app setup
st.title("Sankey Diagram: MRICloud data for subject 127")

#load the url
url = "https://raw.githubusercontent.com/bcaffo/MRIcloudT1volumetrics/master/inst/extdata/multilevel_lookup_table.txt"
multilevel_lookup = pd.read_csv(url, sep = "\t").drop(['Level5'], axis = 1)
multilevel_lookup = multilevel_lookup.rename(columns = {
    "modify"   : "roi",
    "modify.1" : "level4",
    "modify.2" : "level3",
    "modify.3" : "level2",
    "modify.4" : "level1"})
multilevel_lookup = multilevel_lookup[['roi', 'level4', 'level3', 'level2', 'level1']]
multilevel_lookup.head()


## load in the subject data
id = 127
subjectData = pd.read_csv("https://raw.githubusercontent.com/smart-stats/ds4bio_book/main/book/assetts/kirby21AllLevels.csv")
subjectData = subjectData.loc[(subjectData.type == 1) & (subjectData.level == 5) & (subjectData.id == id)]
subjectData = subjectData[['roi', 'volume']]
## Merge the subject data with the multilevel data
subjectData = pd.merge(subjectData, multilevel_lookup, on = "roi")
subjectData = subjectData.assign(icv = "ICV")
subjectData = subjectData.assign(comp = subjectData.volume / np.sum(subjectData.volume))
subjectData.head()


# Display 'icv', 'level1', 'level2', 'level3'
# create empty lists
sources = []
targets = []
values = []

# from ICV to Level 1
# sum up the volumes
grouped = subjectData.groupby(['icv', 'level1'], as_index=False)['comp'].sum()

#add to empty lists
sources.extend(grouped['icv'].tolist())
targets.extend(grouped['level1'].tolist())
values.extend(grouped['comp'].tolist())


# from Level 1 to Level 2
# sum up the volumes
grouped = subjectData.groupby(['level1', 'level2'], as_index=False)['comp'].sum()

#add to lists
sources.extend(grouped['level1'].tolist())
targets.extend(grouped['level2'].tolist())
values.extend(grouped['comp'].tolist())


# from Level 2 to Level 3
# sum up the volumes
grouped = subjectData.groupby(['level2', 'level3'], as_index=False)['comp'].sum()

#add to lists
sources.extend(grouped['level2'].tolist())
targets.extend(grouped['level3'].tolist())
values.extend(grouped['comp'].tolist())


# Create a list of unique labels from sources and targets
label_list = list(set(sources + targets))

# Create a dictionary of nodes
node_mapping = {}

#for every label(node) in the label_list, give it an ordered number
for i, node in enumerate(label_list):
  node_mapping[node] = i



#create empty list for the source numbers
source_num = []

#for sou in sources(list), give the text a number
for sou in sources:
  number = node_mapping[sou] #look up its number
  source_num.append(number) #append to the new list (source_num)


#create empty list for the target numbers
target_num = []

#for target in targets(list), give the text a number
for tar in targets:
  number = node_mapping[tar] #look up its number
  target_num.append(number) #append to the new list (target_num)




# Create Sankey diagram using Plotly
fig = go.Figure(go.Sankey(
    node = dict(
      pad = 15,
      thickness = 20,
      line = dict(color = "black", width = 0.5),
      label = label_list,
      color = "pink"
    ),
    link=dict(
        source=source_num,
        target=target_num,
        value=values
    )
))

# Display in Streamlit
st.plotly_chart(fig)