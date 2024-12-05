import pandas as pd
import os
import argparse
from operator import itemgetter
import networkx as nx
import matplotlib.pyplot as plt

# Function to find each relationship, and the depth of each relationship.
def entity_relationship(onto_dict,id_entity):

    relationships = {} #dictionnary of each relationship between label and depth of relation ships

    # # Look for shortest path lengths from source to all relation
    #for parents_id in  :

    # return relationships



def main() : 

    parser = argparse.ArgumentParser(description = "Onto-X Project")
    parser.add_argument("--csv",type=str,default=r"data\\onto_x.csv",help = "Path to Onto-X Project CSV file. Default: onto_x.csv")
    parser.add_argument("--id",type=str,default='http://entity/CST/CERVIX%20DIS',help="ID of the entity we want its relationships")
    args = parser.parse_args()

    try :
        onto_df = pd.read_csv(args.csv,sep=',')
    except FileNotFoundError : 
        print(f"ERROR : Incorrect path for the csv file")
        return
    
    onto_df.drop_duplicates(inplace=True)
    onto_df['Parents'] = onto_df['Parents'].fillna("") # Replaces NaN values in the Parents column with “” to prepare for the eventual separation of the parents

    onto_graph = nx.DiGraph()

    onto_df['Parents'] = onto_df['Parents'].apply(lambda x: x.split('|') if x else []) # Split Parents separated by "|" to get a table of parents for each Class ID

    # Build dictionnary of onto_df : 

    for index , row in onto_df.iterrows() :
        label = row["Preferred Label"]
        parents = row["Parents"]
        for parent in parents : 
            onto_graph.add_edge(label,parent)
       
    nx.draw(onto_graph)
    plt.savefig("onto_graph.png")

    if args.id not in onto_df['Preferred Label'] :
        print(f"ERROR : id {args.id} doesn't exist in this csv file")
        return


    # The dictionary creates a key/value link between Class IDs and their labels and Parents, which will facilitate work on loops and data comparison queries
    relationship = entity_relationship(onto_graph,args.id)
    sorted_relationships = dict(sorted(relationship.items(),key=itemgetter(1),reverse = True))
    print(sorted_relationships)


if __name__ == "__main__":
    main()