# Onto-X Project API Tool

## Introduction

This project builds a logical representation of the Onto-X ontology from a CSV file. The strategy adopted is to use a directed graph to model the hierarchical relationships between entities. The tool provides a command-line interface (CLI) to obtain the direct and indirect relationships of a given entity, as well as the depth of each relationship.

---

## 1. **Principle applied**
### Data Modeling with a Directed Graph 
- Each entity is represented as a node in the graph.
- Parent-child relationships in the ontology are modeled by edges

### Preserving Hierarchies and Extracting Relationships
- **Path exploration**: Using the shortest-path algorithm (`single_source_shortest_path_length`) to retrieve relationships and their depths.
- **Handling specific cases**: Explicitly processing relationships between entities with shared parents

### Robustness 
- **Data preprocessing**: Handling missing values and duplicates to avoid computation errors.  

---

## 2. **Decisions Made and Their Justifications**  

I started with a very simple version using only pandas and python dictionaries. But I didn't find the solution visual enough. I thought that with a directed graph it would be simpler in the end and would allow for future data visualization that would be easier to implement.

### Why Use a Directed Graph?  
- **Clarity**: Directed graphs naturally represent hierarchies where each relationship has a directional meaning (Parent → Child).  
- **Efficiency**: NetworkX provides optimized functions to traverse relationships and calculate distances.  

### Managing Missing or Indirect Relationships  
- An entity may share parents with other entities without being directly connected. By explicitly adding such relationships at depth 0, we ensure all relevant relationships are captured.  

### Modular Structure  
- The code is organized into clear and separate functions (`build_onto_graph`, `entity_relationship`, etc.), facilitating maintenance and extensibility.  

---

## 3. **Recommendations for Future Work** 

### a) Graph Visualization  
- Add a feature to visualize the hierarchy graphically (using Matplotlib or Graphviz) for better exploration.

### b) CLI Enhancements  
- Include options to export results (JSON, CSV) 
- Include options to query multiple entities simultaneously.  
- Include options to work with different type of file extension (not only CSV)

### c) Expose Functionality via a REST API (FastAPI)  
- **Why?** To enable real-time interaction, making the tool accessible to a broader audience through HTTP requests.  
- **Suggestion**: Implement endpoints to dynamically build the graph and query relationships.  

---

## Usage Example  
### Command:  
```bash
python onto_x.py --csv FILE_PATH --id GIVEN_ID
```
