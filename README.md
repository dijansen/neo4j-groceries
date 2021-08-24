# Groceries

Bits of information on how to start a Neo4j instance with APOC (Awesome Procedures On Cypher) en GDS (Graph Data Science) plugins. 

## Installation

Run the following command to start a Neo4j Docker container with the plugins mentioned above automatically installed:

```bash
docker run --name neo4j-groceries -p7474:7474 -p7687:7687 --env NEO4J_AUTH=neo4j/my-password --env 'NEO4JLABS_PLUGINS=["apoc","graph-data-science"]' neo4j:latest
```
Next run the following command to load the [Groceries-dataset](https://www.kaggle.com/heeraldedhia/groceries-dataset):
```bash
python groceries.py
```

## Usage

Navigate to Neo4j Browser, probably running on [http://localhost:7474](http://localhost:7474), unless you altered the Docker-command during installation. Below are several interesting queries to try.

### Show all nodes and relations
Maybe not that interesting at all, but this query will show the full graph. 
```cypher
MATCH (n)
RETURN n
```

### Table with combinations of items
Combination of items should be bought by the same customer on the same date.
```cypher
MATCH (c:Customer)-[p1]->(i1:Item), (c:Customer)-[p2]->(i2:Item)
WHERE  p1.date = p2.date
RETURN  i1.description, i2.description, count(p1) AS amount
ORDER BY amount DESC
```

### Table with items most of bought together
Items most often bought together with 'whole milk'
```cypher
MATCH (c:Customer)-[p1]->(i1:Item), (c:Customer)-[p2]->(i2:Item)
WHERE  p1.date = p2.date and i1.description = "whole milk"
RETURN  i1.description, i2.description, count(p1) AS amount
ORDER BY amount DESC
```

### PageRank & Node Similarity
Create a named graph with the following query:
```cypher
CALL gds.graph.create(
    'my-named-graph',
    ['Customer', 'Item'],
    {
        PURCHASED: {
            type: 'PURCHASED'
        }
    }
);
```
#### PageRank
```cypher
CALL gds.pageRank.stream('my-named-graph')
YIELD nodeId, score
WITH gds.util.asNode(nodeId) as n,  score
WHERE "Item" IN labels(n)
RETURN n.description, score
ORDER BY score DESC
```
You will see that 'whole milk' is part of everyone's diet.
#### Node similarity
```cypher
CALL gds.nodeSimilarity.stream('my-named-graph')
YIELD node1, node2, similarity
RETURN gds.util.asNode(node1), gds.util.asNode(node2), similarity
ORDER BY similarity DESCENDING
```
Not sure yet why customers would like to see similar customers, but it's the idea that counts!

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.