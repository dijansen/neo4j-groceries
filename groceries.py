from neo4j import GraphDatabase
import pandas as pd

df = pd.read_csv('Groceries_dataset.csv')
pd.to_datetime(df['Date'])

driver = GraphDatabase.driver("neo4j://localhost", auth=("neo4j", "my-password"))

with driver.session() as session:
    print("Cleaning database...")
    session.run(
    """
        MATCH (n)
        DETACH DELETE n
    """
    )

    with session.begin_transaction() as tx:
        for index, row in df.iterrows():
            print("Row", index, "of", len(df))
            customerId = int(row['Member_number']);
            # TODO: case to date
            date = row['Date']
            itemDescription = row['itemDescription'];
            
            tx.run(
            """
                MERGE (c:Customer {id: $customerId})
                MERGE (i:Item {description: $itemDescription})
                MERGE (c)-[p:PURCHASED {date: $date}]->(i)
            
            """, customerId=customerId, itemDescription=itemDescription, date=date)
        tx.commit()

driver.close()