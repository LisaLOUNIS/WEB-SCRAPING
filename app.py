import streamlit as st
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt

# Load data function
@st.cache_resource
def load_data():
    return pd.read_csv('jobs_data.csv')

df = load_data()

# Sidebar for navigation
st.sidebar.title("Navigation")
app_mode = st.sidebar.radio("Choose the view", ["Filter offers", "Skills per country"])

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
        if pd.notna(row["score"]):
            st.markdown(f"**Certified Reputation!** **RSE:** {row['score']}, ranked N. **{int(row['rank'])}** in the word according to RepTrak (2023)")
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