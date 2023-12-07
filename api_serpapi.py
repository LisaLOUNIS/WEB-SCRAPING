import requests

def fetch_all_google_jobs_data(api_key, query, location, hl="en", chips=None):
    """
    Récupère les données de toutes les pages de l'API Google Jobs pour une recherche donnée.

    Paramètres :
    api_key (str): Clé privée SerpApi.
    query (str): Requête de recherche.
    location (str, optionnel): Lieu géographique pour la recherche.
    hl (str): Langue pour la recherche.
    chips (list, optionnel): Conditions supplémentaires pour la requête.

    Retourne :
    list: Toutes les réponses JSON analysées de l'API.
    """
    all_results = []
    start = 0
    while True:
        # Paramètres pour la requête API
        params = {
            "engine": "google_jobs",
            "q": query,
            "start": start,
            "hl": hl,
            "api_key": api_key
        }

        if location:
            params["location"] = location

        if chips:
            params["chips"] = ','.join(chips)

        # URL de base pour l'API Google Jobs
        base_url = "https://serpapi.com/search.json"

        # Envoi d'une requête GET à l'API
        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            data = response.json()
            all_results.append(data)

            # Vérifier s'il y a encore des résultats
            if "jobs_results" not in data or not data["jobs_results"]:
                break

            start += 10  # Incrémenter pour la prochaine page
        else:
            break

    return all_results

# Utilisation de la fonction
# Remplacez 'your_api_key' par votre clé SerpApi réelle
complete_data = fetch_all_google_jobs_data("65c15aeae94ce28a059108557e76ff428c362bd6550714533d91c1cf3c77f016", "Data Scientist", "Ile-De-France, France")
