import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="Bike Sharing Dashboard", layout="wide")

st.title("🚲 Bike Sharing Dashboard")
st.markdown("Analisis penggunaan sepeda (2011–2012)")

# =========================
# LOAD DATA
# =========================
@st.cache_data
def load_data():
    df = pd.read_csv("dashboard/main_data.csv")
    df['dteday'] = pd.to_datetime(df['dteday'])

    # normalisasi nama kolom
    df.columns = df.columns.str.strip()

    # rename biar konsisten
    if 'cnt_day' in df.columns:
        df.rename(columns={'cnt_day': 'cnt'}, inplace=True)
    if 'workingday_day' in df.columns:
        df.rename(columns={'workingday_day': 'workingday'}, inplace=True)

    return df

day_df = load_data()

# =========================
# SIDEBAR FILTER
# =========================
st.sidebar.header("📅 Filter Data")

start_date = st.sidebar.date_input("Start Date", day_df['dteday'].min())
end_date = st.sidebar.date_input("End Date", day_df['dteday'].max())

filtered_df = day_df[
    (day_df['dteday'] >= pd.to_datetime(start_date)) &
    (day_df['dteday'] <= pd.to_datetime(end_date))
]

# =========================
# KPI CARDS
# =========================
st.subheader("📊 Key Metrics")

col1, col2, col3 = st.columns(3)

col1.metric("Total Rentals", int(filtered_df['cnt'].sum()))
col2.metric("Average Rentals", int(filtered_df['cnt'].mean()))
col3.metric("Max Rentals", int(filtered_df['cnt'].max()))

# =========================
# PERTANYAAN 1
# =========================
st.header("📊 Distribusi Penggunaan Sepeda")

# kategori usage
filtered_df['usage_category'] = pd.qcut(
    filtered_df['cnt'],
    q=3,
    labels=['Low', 'Medium', 'High']
)

col1, col2 = st.columns(2)

with col1:
    fig1, ax1 = plt.subplots()
    sns.countplot(data=filtered_df, x='usage_category', ax=ax1)

    ax1.set_title("Distribusi Kategori Penggunaan")
    ax1.set_xlabel("Kategori")
    ax1.set_ylabel("Jumlah Hari")

    st.pyplot(fig1)

with col2:
    st.markdown("""
    **Insight:**
    - Kategori **Medium dan High mendominasi** penggunaan sepeda.
    - Ini menunjukkan tingkat penggunaan yang tinggi dan stabil.
    - Demand cukup konsisten sepanjang periode.
    """)

# =========================
# PERTANYAAN 2
# =========================
st.header("📈 Tren Penyewaan Sepeda")

col1, col2 = st.columns(2)

with col1:
    fig2, ax2 = plt.subplots(figsize=(10,4))

    sns.lineplot(
        data=filtered_df,
        x='dteday',
        y='cnt',
        hue='workingday',
        ax=ax2
    )

    ax2.set_title("Tren Penyewaan (Working Day vs Holiday)")
    ax2.set_xlabel("Tanggal")
    ax2.set_ylabel("Jumlah Penyewaan")

    st.pyplot(fig2)

with col2:
    st.markdown("""
    **Insight:**
    - Hari kerja menunjukkan **tren lebih stabil dan tinggi**.
    - Hari libur memiliki **fluktuasi lebih besar**.
    - Terdapat pola musiman pada penyewaan sepeda.
    """)

# =========================
# PEAK & DROP
# =========================
st.header("📌 Peak & Drop Analysis")

col1, col2 = st.columns(2)

max_val = filtered_df['cnt'].max()
min_val = filtered_df['cnt'].min()

peak_day = filtered_df[filtered_df['cnt'] == max_val]
low_day = filtered_df[filtered_df['cnt'] == min_val]

with col1:
    st.write("🔺 Penyewaan Tertinggi")
    st.dataframe(peak_day[['dteday', 'cnt']])

with col2:
    st.write("🔻 Penyewaan Terendah")
    st.dataframe(low_day[['dteday', 'cnt']])

st.subheader("📌 Peak & Drop Analysis")

# lebih spesifik
if 'df' not in locals():
    df = day_df

max_val = df['cnt'].max()
min_val = df['cnt'].min()

peak_day = df[df['cnt'] == max_val]
low_day = df[df['cnt'] == min_val]

peak_date = peak_day.iloc[0]['dteday']
low_date = low_day.iloc[0]['dteday']

col1, col2 = st.columns(2)

with col1:
    st.metric("🔺 Tertinggi", int(max_val))
    st.write("Tanggal:", peak_date.date())

with col2:
    st.metric("🔻 Terendah", int(min_val))
    st.write("Tanggal:", low_date.date())

st.markdown("""
**Insight:**
- Terdapat lonjakan signifikan pada waktu tertentu.
- Penurunan biasanya terjadi pada periode dengan permintaan rendah.
- Faktor eksternal seperti musim kemungkinan berpengaruh.
""")