import logging
from neo4j import GraphDatabase
from neo4j.exceptions import ServiceUnavailable

class App:
    def __init__(self, uri, user, password, database="neo4j"):
        self.database = database
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def loadNodes(self):
        with self.driver.session() as session:
            result = session.write_transaction(self.loadNodes_return)
            print("NODES SUCCESSFULLY LOADED!")
            return result

    @staticmethod
    def loadNodes_return(tx):
        query = (
            "MATCH (p:Person)  "
            "RETURN ID(p), p.name, p.lastName"
        )
        result = list(tx.run(query))
        try:
            return result
        except ServiceUnavailable as exception:
            logging.error("{ query } raised an error: \n { exception}".format(query=query, exception=exception))
            raise

    def loadRelationships(self):
        with self.driver.session() as session:
            result = session.write_transaction(self.loadRelationships_return)
            print("EDGES SUCCESSFULLY LOADED!")
            return result

    @staticmethod
    def loadRelationships_return(tx):
        query = (
            "MATCH (k)-[r:RELATIONSHIP]->(l) "
            "RETURN ID(r), ID(k) as Start, r.Type as Edge, ID(l) as End"
        )
        result = list(tx.run(query))
        try:
            return result
        except ServiceUnavailable as exception:
            logging.error("{ query } raised an error: \n { exception}".format(query=query, exception=exception))
            raise

    def createNode(self, name, lastName):
        with self.driver.session() as session:
            result = session.write_transaction(self.createNode_return, name, lastName)
            for row in result:
                print("Node created: {p}".format(p=row['p']))

    @staticmethod
    def createNode_return(tx, person_name, person_ln):
        query = (
            "CREATE (p: Person{name : $person_name , lastName : $person_ln })"
            "RETURN p"    
        )
        result = tx.run(query, person_name=person_name, person_ln=person_ln)
        try:
            return[{"p": row["p"]["name"]} for row in result]
        except ServiceUnavailable as exception:
            logging.error("{ query } raised an error: \n { exception}".format(query=query, exception=exception))
            raise
    
    def deleteNode(self, id):
        with self.driver.session() as session:
            result = session.write_transaction(self.deleteNode_return, id)
            for row in result:
                print("Node deleted: {p}".format(p=row['p']))

    @staticmethod
    def deleteNode_return(tx, person_id):
        query = (
            "MATCH (p:Person) WHERE ID(p)= $person_id "
            "DETACH DELETE p "
            "RETURN p"
        )
        result = tx.run(query, person_id=person_id)
        try:
            return[{"p": row["p"]["name"]} for row in result]
        except ServiceUnavailable as exception:
            logging.error("{ query } raised an error: \n { exception}".format(query=query, exception=exception))
            raise
    
    def createRelation(self, personOne_id, personTwo_id, relationship):
        with self.driver.session() as session:
            result = session.write_transaction(self.createRelation_return, personOne_id, personTwo_id, relationship)
            for row in result:
                print("Relationship created between: {p1},{p2}".format(p1=row['p1'], p2=row['p2']))

    @staticmethod
    def createRelation_return(tx, personOne, personTwo, rType):
        query = (
            "MATCH (p1: Person) WHERE ID(p1) = $personOne "
            "MATCH (p2: Person) WHERE ID(p2) = $personTwo "
            "CREATE (p1)-[:RELATIONSHIP {Type : $rType}]->(p2) "
            "RETURN p1, p2"
        )
        result = tx.run(query, personOne=personOne, personTwo=personTwo, rType=rType)
        try:
            return[{"p1": row["p1"]["name"], "p2": row["p2"]["name"]} for row in result]
        except ServiceUnavailable as exception:
            logging.error("{ query } raised an error: \n { exception}".format(query=query, exception=exception))
            raise

    def deleteRelation(self, personOne_id, personTwo_id, relationship):
        with self.driver.session() as session:
            result = session.write_transaction(self.deleteRelation_return, personOne_id, personTwo_id, relationship)
            for row in result:
                print("Relationship deleted between: {p1},{p2}".format(p1=row['p1'], p2=row['p2']))

    @staticmethod
    def deleteRelation_return(tx, personOne, personTwo, rType):
        query = (
            "MATCH (p1: Person) WHERE ID(p1) = $personOne "
            "MATCH (p2: Person) WHERE ID(p2) = $personTwo "
            "MATCH (p1)-[r:RELATIONSHIP {Type : $rType}]->(p2) "
            "DELETE r "
            "RETURN p1, p2"
        )
        result = tx.run(query, personOne=personOne, personTwo=personTwo, rType=rType)
        try:
            return[{"p1": row["p1"]["name"], "p2": row["p2"]["name"]} for row in result]
        except ServiceUnavailable as exception:
            logging.error("{ query } raised an error: \n { exception}".format(query=query, exception=exception))
            raise

def createNode(name, lastname):
    app = sessionStart()
    app.createNode(name, lastname)
    app.close()

def createRelationship(idOne, idTwo, relation):
    app = sessionStart()
    idOne = int(idOne)
    idTwo = int(idTwo)
    app.createRelation(idOne, idTwo, relation)
    app.close()

def deleteNode(idNode):
    app = sessionStart()
    idNode = int(idNode)
    app.deleteNode(idNode)
    app.close()

def deleteRelationship(idOne, idTwo, relation):
    app = sessionStart()
    idOne = int(idOne)
    idTwo = int(idTwo)
    app.deleteRelation(idOne, idTwo, relation)
    app.close()

def loadNodes():
    app = sessionStart()
    nodes = app.loadNodes()
    app.close()
    return nodes

def loadEdges():
    app = sessionStart()
    edges = app.loadRelationships()
    app.close()
    return edges

def sessionStart():
    uri = ""
    user = "neo4j"
    password = ""
    return App(uri, user, password)