import pandas as pd
import argparse
from operator import itemgetter
import networkx as nx


def entity_relationship(onto_graph,onto_data,id_entity):

    """
    Computes all relationships (direct and indirect) for a given entity in the ontology.

    Parameters:
        onto_graph (DiGraph): The ontology graph where nodes represent entities.
        onto_data (DataFrame): The original ontology data containing IDs, labels, and parents.
        id_entity (str): The label of the entity for which relationships are being queried.

    Returns:
        dict: A dictionary of related entities and their respective depths relative to the start entity.
    """

    # Retrieve all ancestor relationships and their depths
    relationships = {
        label: depth
        for label, depth in nx.single_source_shortest_path_length(onto_graph.reverse(), id_entity).items()
        if label!=id_entity # Exclude the entity itself
    }

    # Handle entities with shared parents that are missed by the graph traversal
    start_id = onto_data.loc[onto_data['Preferred Label'] == id_entity, 'Class ID'].values[0]
    parent_ids = onto_data.loc[onto_data['Class ID'] == start_id, 'Parents'].values[0].split('|')

    for parent_id in parent_ids:
        # Find entities that share the same parent
        common_parents = onto_data.loc[onto_data['Parents'].str.contains(parent_id, na=False), 'Preferred Label']
        for common_parent in common_parents:
            if common_parent not in relationships and common_parent != id_entity :
                relationships[common_parent] = 0 # Depth 0 for shared parent


    return relationships


def build_onto_graph(onto_data) :
    """
    Constructs a directed graph representing the ontology.

    Parameters:
        onto_data (DataFrame): The ontology data containing 'Class ID', 'Preferred Label', and 'Parents'.

    Returns:
        DiGraph: A NetworkX directed graph where edges represent parent-child relationships.
    """
    onto_graph = nx.DiGraph()

    for index , row in onto_data.iterrows() :
        id = row['Class ID']
        pref_label = row["Preferred Label"]
        if row['Parents'] : 
            parents = row["Parents"].split("|")
            for parent in parents : 
                # Retrieve the label of the parent entity
                parent_label = onto_data.loc[onto_data['Class ID'] == parent, 'Preferred Label'].values
                if len(parent_label) > 0:
                    onto_graph.add_edge(parent_label[0], pref_label) # Add Parent → Child edge


    return onto_graph




def main() : 
    """
    Main function for the Command Line Interface (CLI) tool. Parses arguments, builds the ontology graph, and queries relationships.

    """
    # CLI argument parser
    parser = argparse.ArgumentParser(description = "Onto-X Project")
    parser.add_argument("--csv",type=str,default=r"data\\onto_x.csv",help = "Path to Onto-X Project CSV file. Default: onto_x.csv")
    parser.add_argument("--id",type=str,default='CERVIX DISORDER',help="ID of the entity we want its relationships")
    args = parser.parse_args()

    # Load ontology data
    try :
        onto_df = pd.read_csv(args.csv,sep=',')
    except FileNotFoundError : 
        print(f"ERROR : Incorrect path for the csv file")
        return

    # Check if the queried entity exists in the data
    if args.id not in onto_df['Preferred Label'].values :
        print(f"ERROR : id {args.id} doesn't exist in this csv file")
        return    

     # Preprocess the ontology data
    onto_df.drop_duplicates(inplace=True)
    onto_df['Parents'] = onto_df['Parents'].fillna("") # Handle NaN values in the Parents column

    # Build ontology graph
    onto_graph = build_onto_graph(onto_df)

    # Compute and sort relationships for the queried entity
    relationship = entity_relationship(onto_graph,onto_df,args.id)
    sorted_relationships = dict(sorted(relationship.items(),key=itemgetter(1),reverse = True))

    # Display the results
    print("Relationships and depths for entity:", args.id)
    for entity, depth in sorted_relationships.items():
        print(f"{entity}: {depth}")

if __name__ == "__main__":
    main()