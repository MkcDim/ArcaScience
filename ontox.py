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

    start_id = onto_data.loc[onto_data['Preferred Label'] == id_entity, 'Class ID'].values[0]
    parent_ids = onto_data.loc[onto_data['Class ID'] == start_id, 'Parents'].values[0].split('|')

    for parent_id in parent_ids:
        common_parents = onto_data.loc[onto_data['Parents'].str.contains(parent_id, na=False), 'Preferred Label']
        for common_parent in common_parents:
            if common_parent not in relationships and common_parent != id_entity :
                relationships[common_parent] = 0


    return relationships


def build_onto_graph(onto_data) :

    onto_graph = nx.DiGraph()

    for index , row in onto_data.iterrows() :
        id = row['Class ID']
        pref_label = row["Preferred Label"]
        if row['Parents'] : 
            parents = row["Parents"].split("|")
            for parent in parents : 
                parent_label = onto_data.loc[onto_data['Class ID'] == parent, 'Preferred Label'].values
                if len(parent_label) > 0:
                    onto_graph.add_edge(parent_label[0], pref_label)


    return onto_graph




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
    
    if args.id not in onto_df['Preferred Label'].values :
        print(f"ERROR : id {args.id} doesn't exist in this csv file")
        return    

    onto_df.drop_duplicates(inplace=True)
    onto_df['Parents'] = onto_df['Parents'].fillna("") # Replaces NaN values in the Parents column with “” to prepare for the eventual separation of the parents

    onto_graph = build_onto_graph(onto_df)
    relationship = entity_relationship(onto_graph,onto_df,args.id)
    sorted_relationships = dict(sorted(relationship.items(),key=itemgetter(1),reverse = True))
    print(sorted_relationships)

if __name__ == "__main__":
    main()