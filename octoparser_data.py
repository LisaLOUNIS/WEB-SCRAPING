import pandas as pd
import glob

def lire_tous_csv(dossier):
    # Liste tous les fichiers CSV dans le dossier
    fichiers_csv = glob.glob(f"{dossier}/*.csv")

    # Liste pour stocker les données de chaque fichier CSV
    donnees = []

    # Lire chaque fichier CSV et l'ajouter à la liste des données
    for fichier in fichiers_csv:
        df = pd.read_csv(fichier)
        donnees.append(df)

    # Fusionner toutes les données en un seul DataFrame
    donnees_fusionnees = pd.concat(donnees, ignore_index=True)

    return donnees_fusionnees

# Exemple d'utilisation
dossier = r"C:\Users\lisac\Downloads\Octoparser"
donnees_fusionnees = lire_tous_csv(dossier)

def extraire_competences(description, competences):
    # Vérifier si la description est une chaîne de caractères
    if isinstance(description, str):
        # Trouver les compétences mentionnées dans la description
        competences_trouvees = [comp for comp in competences if comp.lower() in description.lower()]
        return competences_trouvees
    else:
        # Retourner une liste vide si la description n'est pas une chaîne de caractères
        return []


# Liste des compétences à rechercher
skills = [
    "Python", "R", "SQL", "Excel", "Tableau", "PowerBI", "Dataiku", "Snowflake",
    "GCP", "AWS", "AZURE", "Databricks", "Talend", "Spark", "Scala", "Dataiku",
    "Airflow", "S3", "Kafka", "Hadoop", "SQL", "NoSQL", "Cassandra", "MongoDB",
    "ELK", "Git", "Kubernetes", "Docker", "OVH", "Kanban", "Jira", "Jenkins",
    "ElasticSearch", "Linus", "Kibana", "LogStash", "keras", "Tensorflow", "Gitlab",
    "Snowflake", "NLP", "Random Forest", "XGBoost", "SQL Server", "Oracle", "LLM",
    "IA generative", "generative AI", "GPT", "Terraform", "Yolo", "Pytorch",
    "Transformers", "scikit-learn", "pySpark", "Pyspark", "PySpark", "SAS", "scipy",
    "Azure Data Factory", "Java", "VBA", "Matplotlib", "Seaborn", "Pandas","Plotly","Fast API","Flask","Jenkins",
    "NumPy", "SciKit-Learn", "Streamlit", "Dash", "Shiny", "Flask", "Django",
    "BigQuery", "Redshift", "PostgreSQL", "MySQL", "DB2", "SQLite", "MLflow",
    "Plotly", "Bokeh", "D3.js", "GraphQL", "REST API", "Microservices","Selenium","BeautifulSoup","java","C#","C++","HDFS","Mapreduce","Yarn"
]

# Supposons que `donnees_fusionnees` est votre DataFrame
# Appliquer la fonction pour extraire les compétences
donnees_fusionnees['Technical_skills'] = donnees_fusionnees['Job_description'].apply(lambda desc: extraire_competences(desc, skills))

# Afficher le résultat
print(donnees_fusionnees[['Job_description', 'Technical_skills']])


donnees_fusionnees.to_csv("donnees_octoparser.csv", index=False)

rse_score= pd.read_csv('donnees_RSE_entreprises.csv')

result_df = pd.merge(donnees_fusionnees, rse_score, left_on='Company_Name', right_on='Nom de l\'Entreprise')

result_df.to_csv("donnees_octoparser_et_rse_score.csv", index=False)
print(result_df.shape[0])