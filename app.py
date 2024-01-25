import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

@st.cache
def load_data():
    return pd.read_csv('jobs_data.csv')

df = load_data()

st.sidebar.header("Filters")

if st.sidebar.button("Reset filters"):
    st.experimental_rerun()

selected_country = st.sidebar.selectbox("Select nation: ", ['No filters'] + list(df['country'].unique()))
selected_company = st.sidebar.selectbox("Select company: ", ['No filters'] + list(df['company_name'].unique()))
unique_skills = list(set(skill for sublist in df['technical_skills'].dropna().apply(eval) for skill in sublist))
selected_skill = st.sidebar.selectbox("Select skill: ", ['No filters'] + unique_skills)

st.header("Filtered job offers")
filtered_data = df
if selected_country != 'No filters':
    filtered_data = filtered_data[filtered_data['country'] == selected_country]
st.dataframe(filtered_data)

st.header("Skills Analysis by Nation")

def plot_skill_distribution(data, country):
    skill_count = {}
    for _, row in data.iterrows():
        if pd.notna(row['technical_skills']):
            skills = eval(row['technical_skills'])
            for skill in skills:
                if skill in skill_count:
                    skill_count[skill] += 1
                else:
                    skill_count[skill] = 1

    top_skills = sorted(skill_count.items(), key=lambda x: x[1], reverse=True)[:10]
    top_skills_names = [skill[0] for skill in top_skills]
    top_skills_counts = [skill[1] for skill in top_skills]

    plt.figure(figsize=(10, 5))
    plt.bar(top_skills_names, top_skills_counts)
    plt.xlabel('Skill')
    plt.ylabel('Frequency')
    plt.title(f"Most Demanded Skills in {country}")
    plt.xticks(rotation=90)
    st.pyplot(plt)

if selected_country != 'No filters':
    plot_skill_distribution(df[df['country'] == selected_country], selected_country)

