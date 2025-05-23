from rdflib import Graph, Namespace, Literal, RDF, OWL


g = Graph()
g.parse("med_doentes.ttl")

#

q="""
    CONSTRUCT {
        ?patientX :hasDisease ?diseaseY .
    }
    WHERE {
        ?patientX a :Patient .
        ?diseaseY a :Disease .
        ?patientX :hasSymptom ?x .
        ?diseaseY :hasSymptom ?x .
        ?patientX :hasSymptom ?y .
        ?diseaseY :hasSymptom ?y .
        ?patientX :hasSymptom ?z .
        ?diseaseY :hasSymptom ?z .
        FILTER(?x != ?y && ?x != ?z && ?y != ?z) 
    }
"""
n = Namespace("http://www.example.org/disease-ontology/")

g.add((n.hasDisease, RDF.type, OWL.ObjectProperty))

for r in g.query(q):
    
    g.add(r)

(g.serialize("comDiagnosticos.ttl", format="turtle"))