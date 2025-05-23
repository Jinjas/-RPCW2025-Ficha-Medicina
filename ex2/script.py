from rdflib import Graph, Namespace, RDF, RDFS, OWL, Literal
import csv
import json
import uuid

# Define Namespace
EX = Namespace("http://www.example.org/disease-ontology/")

# Load Existing Ontology
new_graph = Graph()
new_graph.parse("medical.ttl", format="turtle")


# Bind Prefixes
new_graph.bind("", EX)
new_graph.bind("owl", OWL)
new_graph.bind("rdf", RDF)
new_graph.bind("rdfs", RDFS)


# Define Ontology Structure
new_graph.add((EX.Ontology, RDF.type, OWL.Ontology))


# Process Symptoms
with open("Disease_Syntoms.csv", "r") as csv_file:
    reader = csv.DictReader(csv_file)

    for row in reader:
        disease_name = row["Disease"].strip().replace(" ", "_")
        disease_uri = EX[disease_name]

        new_graph.add((disease_uri, RDF.type, EX.Disease))

        symptoms = {
            row[f"Symptom_{i}"].strip().replace(" ", "_")
            for i in range(1, 18)
            if row.get(f"Symptom_{i}") and row[f"Symptom_{i}"].strip()
        }

        for symptom in symptoms:
            symptom_uri = EX[symptom]
            new_graph.add((symptom_uri, RDF.type, EX.Symptom))
            new_graph.add((disease_uri, EX.hasSymptom, symptom_uri))

# Process Disease Descriptions
with open("Disease_Description.csv", "r", encoding="utf-8") as csv_file:
    reader = csv.DictReader(csv_file)

    for row in reader:
        disease_name = row["Disease"].strip().replace(" ", "_")
        description = row["Description"].strip()

        disease_uri = EX[disease_name]

        if (disease_uri, RDF.type, EX.Disease) in new_graph:
            new_graph.add((disease_uri, EX.hasDescription, Literal(description)))


new_graph.serialize(destination="med_doencas.ttl", format="turtle")

