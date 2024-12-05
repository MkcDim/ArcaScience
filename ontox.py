import pandas as pd
import os
import argparse
from operator import itemgetter
import networkx as nx
import matplotlib.pyplot as plt


def entity_relationship(onto_graph,onto_data,id_entity):

  
    relationships = {
        label: depth
        for label, depth in nx.single_source_shortest_path_length(onto_graph.reverse(), id_entity).items()
        if label!=id_entity
    }

    # Identifier les frères/sœurs (même parent que start_label)
    start_id = onto_data.loc[onto_data['Preferred Label'] == id_entity, 'Class ID'].values[0]
    parent_ids = onto_data.loc[onto_data['Class ID'] == start_id, 'Parents'].values[0].split('|')

    for parent_id in parent_ids:
        common_parents = onto_data.loc[onto_data['Parents'].str.contains(parent_id, na=False), 'Preferred Label']
        for common_parent in common_parents:
            if common_parent not in relationships and common_parent != id_entity :
                relationships[common_parent] = 0


    return relationships






def main() : 

    parser = argparse.ArgumentParser(description = "Onto-X Project")
    parser.add_argument("--csv",type=str,default=r"data\\onto_x.csv",help = "Path to Onto-X Project CSV file. Default: onto_x.csv")
    parser.add_argument("--id",type=str,default='CERVIX DISORDER',help="ID of the entity we want its relationships")
    args = parser.parse_args()

    try :
        onto_df = pd.read_csv(args.csv,sep=',')
    except FileNotFoundError : 
        print(f"ERROR : Incorrect path for the csv file")
        return
    
    onto_df.drop_duplicates(inplace=True)
    onto_df['Parents'] = onto_df['Parents'].fillna("") # Replaces NaN values in the Parents column with “” to prepare for the eventual separation of the parents

    onto_graph = nx.DiGraph()

    #onto_df['Parents'] = onto_df['Parents'].apply(lambda x: x.split('|') if x else []) # Split Parents separated by "|" to get a table of parents for each Class ID
    # Build dictionnary of onto_df : 

    for index , row in onto_df.iterrows() :
        id = row['Class ID']
        pref_label = row["Preferred Label"]
        if row['Parents'] : 
            parents = row["Parents"].split("|")
            for parent in parents : 
                parent_label = onto_df.loc[onto_df['Class ID'] == parent, 'Preferred Label'].values
                if len(parent_label) > 0:
                    onto_graph.add_edge(parent_label[0], pref_label)


       
    nx.draw(onto_graph)
    plt.savefig("onto_graph.png")

    if args.id not in onto_df['Preferred Label'].values :
        print(f"ERROR : id {args.id} doesn't exist in this csv file")
        return


    # The dictionary creates a key/value link between Class IDs and their labels and Parents, which will facilitate work on loops and data comparison queries
    relationship = entity_relationship(onto_graph,onto_df,args.id)
    sorted_relationships = dict(sorted(relationship.items(),key=itemgetter(1),reverse = True))
    print(sorted_relationships)


if __name__ == "__main__":
    main()