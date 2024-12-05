import pandas as pd
import os




work_path = os.getcwd()
data_path = os.path.join(work_path,'data')
file_path = os.path.join(data_path,'onto_x.csv')


# Load Data
onto_df = pd.read_csv(file_path,sep=',')


onto_df['Parents'] = onto_df['Parents'].fillna("") # Replaces NaN values in the Parents column with “” to prepare for the eventual separation of the parents
onto_df['Parents'] = onto_df['Parents'].apply(lambda x: x.split('|') if x else []) # Split Parents separated by "|" to get a table of parents for each Class ID

# Build dictionnary of onto_df : 