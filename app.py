import streamlit as st
import pandas as pd
import requests
import plotly.express as px
st.set_page_config(page_title="Mini analityka danych", layout="wide")
st.title("📊 Mini analityka danych")
st.markdown("Analiza danych z publicznego API z wykorzystaniem endpointów `/users` i `/posts`.")

@st.cache_data
def load_data():
    users = requests.get("https://jsonplaceholder.typicode.com/users").json()
    posts = requests.get("https://jsonplaceholder.typicode.com/posts").json()

    users_df = pd.DataFrame(users)
    posts_df = pd.DataFrame(posts)

    users_df["full_address"] = users_df["address"].apply(
        lambda x: f"{x['street']}, {x['suite']}, {x['city']} ({x['zipcode']})"
    )
    users_df = users_df.drop(columns=["address", "company"])

    return users_df, posts_df
users_df, posts_df = load_data()
st.header("📘 Przykładowe dane")
st.subheader("Użytkownicy")
st.dataframe(users_df.head())

st.subheader("Posty")
st.dataframe(posts_df.head())
st.header("📈 Statystyki")
posts_per_user = posts_df.groupby("userId").size().reset_index(name="liczba_postów")
merged_df = posts_per_user.merge(users_df, left_on="userId", right_on="id")
avg_posts = merged_df["liczba_postów"].mean()
max_user = merged_df.loc[merged_df["liczba_postów"].idxmax(), "name"]
col1, col2, col3 = st.columns(3)
col1.metric("👥 Liczba użytkowników", len(users_df))
col2.metric("📊 Średnia liczba postów", f"{avg_posts:.1f}")
col3.metric("🔥 Najbardziej aktywny użytkownik", max_user)
st.subheader("📊 Liczba postów na użytkownika")
fig1 = px.bar(
    merged_df,
    x="name",
    y="liczba_postów",
    labels={"name": "Użytkownik", "liczba_postów": "Liczba postów"},
)
st.plotly_chart(fig1, use_container_width=True)
st.subheader("🥧 Procentowy udział liczby postów użytkowników")
fig2 = px.pie(
    merged_df,
    values="liczba_postów",
    names="name",
    title="Procentowy udział postów",
)
st.plotly_chart(fig2, use_container_width=True)
st.markdown("---")
st.caption("Projekt: **Mini analityka danych** | Autor: Tomasz Chrząszczak | Kod współtworzony i poprawiony z pomocą AI 🧠")