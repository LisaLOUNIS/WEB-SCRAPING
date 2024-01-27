import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load data function
@st.cache_resource
def load_data():
    jobs_data = pd.read_csv('jobs_data.csv')
    data_avec_rse = pd.read_csv('donnees_octoparser_avec_rse_score.csv')
    data_sans_rse = pd.read_csv('donnees_octoparser_sans_rse_score.csv')

    # Concaténer les DataFrames
    data_jobs= pd.concat([jobs_data, data_avec_rse, data_sans_rse], ignore_index=True)

    return data_jobs


df = load_data()

# Sidebar for navigation
st.sidebar.title("Navigation")
app_mode = st.sidebar.radio("Choose the view", ["Filter offers", "Skills per country", "RSE Score Analysis"])


# Function to plot skill distribution
def plot_skill_distribution(data, title):
    skill_count = {}
    for _, row in data.iterrows():
        if pd.notna(row['technical_skills']):
            skills = eval(row['technical_skills'])
            for skill in skills:
                skill_count[skill] = skill_count.get(skill, 0) + 1

    top_skills = sorted(skill_count.items(), key=lambda x: x[1], reverse=True)[:10]
    top_skills_names = [skill[0] for skill in top_skills]
    top_skills_counts = [skill[1] for skill in top_skills]

    plt.figure(figsize=(10, 5))
    plt.bar(top_skills_names, top_skills_counts)
    plt.xlabel('Skill')
    plt.ylabel('Frequency')
    plt.title(title)
    plt.xticks(rotation=90)
    st.pyplot(plt)

def plot_rse_score(data):
    # Filtrer les données pour les lignes avec des scores RSE disponibles
    rse_data = data.dropna(subset=['score'])

    # Créer un graphique à barres des scores RSE
    plt.figure(figsize=(10, 5))
    plt.bar(rse_data['company_name'], rse_data['score'])
    plt.xlabel('Entreprise')
    plt.ylabel('Score RSE')
    plt.title('Scores RSE des Entreprises')
    plt.xticks(rotation=90)
    st.pyplot(plt)



# If in 'Filter offers' mode
if app_mode == "Filter offers":
    st.title("Filter Job Offers")

    # Filters
    st.sidebar.header("Filters")
    if st.sidebar.button("Reset filters"):
        st.experimental_rerun()

    selected_country = st.sidebar.selectbox("Select nation: ", ['No filters'] + list(df['country'].unique()))
    selected_company = st.sidebar.selectbox("Select company: ", ['No filters'] + list(df['company_name'].unique()))
    unique_skills = list(set(skill for sublist in df['technical_skills'].dropna().apply(eval) for skill in sublist))
    selected_skill = st.sidebar.selectbox("Select skill: ", ['No filters'] + unique_skills)
    show_ranked_only = st.sidebar.checkbox("Show only ranked offers")

    # Filtered data display
    filtered_data = df
    if selected_country != 'No filters':
        filtered_data = filtered_data[filtered_data['country'] == selected_country]
    if selected_company != 'No filters':
        filtered_data = filtered_data[filtered_data['company_name'] == selected_company]
    if selected_skill != 'No filters':
        filtered_data = filtered_data[filtered_data['technical_skills'].apply(lambda x: selected_skill in eval(x) if pd.notna(x) else False)]
    if show_ranked_only:
        filtered_data = filtered_data[filtered_data['rank'].notna()]

    # Display each job offer in a separate box
    for _, row in filtered_data.iterrows():
        st.write("----")
        st.subheader(row['title'])
        st.markdown(f"**Company:** {row['company_name']}")

        # Gérer les valeurs NaN pour 'score' et 'rank'
        score = row['score']
        rank = row['rank']
        if pd.notna(score) and pd.notna(rank):
            st.markdown(f"**Certified Reputation!** **RSE:** {score}, ranked N. **{int(rank)}** in the word according to RepTrak (2023)")
        elif pd.notna(score):
            st.markdown(f"**Certified Reputation!** **RSE:** {score}")

        st.markdown(f"**Location:** {row['location']}")
        if pd.notna(row['technical_skills']):
            st.markdown(f"**Skills:** {', '.join(eval(row['technical_skills']))}")


# If in 'Skills per country' mode
elif app_mode == "Skills per country":
    st.title("Skills Analysis")

    # Select country for skills analysis
    selected_country_analysis = st.selectbox("Select nation for skills analysis: ", ['All Nations'] + list(df['country'].unique()))

    # Display skill distribution plot
    if selected_country_analysis == 'All Nations':
        plot_skill_distribution(df, "Most Demanded Skills Across All Nations")
    else:
        plot_skill_distribution(df[df['country'] == selected_country_analysis], f"Most Demanded Skills in {selected_country_analysis}")

elif app_mode == "RSE Score Analysis":
    st.title("RSE Score Analysis")
    plot_rse_score(df)

