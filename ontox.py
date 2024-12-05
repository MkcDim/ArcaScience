import pandas as pd
import os

# Function to find each relationship, and the depth of each relationship.
def entity_relationship(onto_dict,id_entity,depth = 0, known_relationship = None):


    # Verification if relationship already did to save time and don't fall into loop
    if known_relationship is None :
        known_relationship = []
    elif id_entity in known_relationship : 
        return {}
    
    entity = onto_dict.get(id_entity)

    if not entity : 
        return {}

    relationships = {entity['label'] : depth} #dictionnary of each relationship between label and depth of relation ships

    # Look for depth relationship with recursive fonction
    for parents_id in entity['parents'] :
        relationships.update(entity_relationship(onto_dict,parents_id,depth + 1))

    return relationships




work_path = os.getcwd()
data_path = os.path.join(work_path,'data')
file_path = os.path.join(data_path,'onto_x.csv')


# Load Data
onto_df = pd.read_csv(file_path,sep=',')


onto_df['Parents'] = onto_df['Parents'].fillna("") # Replaces NaN values in the Parents column with “” to prepare for the eventual separation of the parents
onto_df['Parents'] = onto_df['Parents'].apply(lambda x: x.split('|') if x else []) # Split Parents separated by "|" to get a table of parents for each Class ID

# Build dictionnary of onto_df : 
onto_dict = {
    row['Class ID']: {"label":row["Preferred Label"], "parents" : row["Parents"]}
    for index, row in onto_df.iterrows()
} 
# The dictionary creates a key/value link between Class IDs and their labels and Parents, which will facilitate work on loops and data comparison queries

example_of_entity = 'http://entity/CST/HYPOCHLOREM'
relationship = entity_relationship(onto_dict,example_of_entity)
print(relationship)