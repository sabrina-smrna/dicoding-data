import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="Bike Sharing Dashboard", layout="wide")

st.title("🚲 Bike Sharing Dashboard")
st.markdown("Analisis penyewaan sepeda tahun 2011–2012")

# =========================
# LOAD DATA
# =========================
@st.cache_data
def load_data():
    df = pd.read_csv("dashboard/main_data (1).csv")
    df['dteday'] = pd.to_datetime(df['dteday'])
    return df

df = load_data()

# =========================
# SIDEBAR FILTER
# =========================
st.sidebar.header("🔎 Filter Data")

year = st.sidebar.multiselect(
    "Pilih Tahun",
    options=sorted(df['year'].unique()),
    default=sorted(df['year'].unique())
)

month = st.sidebar.multiselect(
    "Pilih Bulan",
    options=sorted(df['month'].unique()),
    default=sorted(df['month'].unique())
)

season = st.sidebar.multiselect(
    "Pilih Musim",
    options=sorted(df['season'].unique()),
    default=sorted(df['season'].unique())
)

filtered_df = df[
    (df['year'].isin(year)) &
    (df['month'].isin(month)) &
    (df['season'].isin(season))
]

# =========================
# BUSINESS QUESTIONS
# =========================
st.subheader("📌 Pertanyaan Bisnis")

st.markdown("""
### 1. Bagaimana distribusi kategori penggunaan sepeda?
### 2. Bagaimana tren penyewaan antara hari kerja dan hari libur?
""")

# =========================
# METRICS
# =========================
st.subheader("📊 Ringkasan Data")

col1, col2, col3 = st.columns(3)

col1.metric("Total Penyewaan", f"{int(filtered_df['cnt'].sum()):,}")
col2.metric("Rata-rata Harian", f"{int(filtered_df['cnt'].mean()):,}")
col3.metric("Maksimum Penyewaan", f"{int(filtered_df['cnt'].max()):,}")

# =========================
# EDA DISTRIBUSI
# =========================
st.subheader("📊 Distribusi Penyewaan")

fig_dist, ax_dist = plt.subplots()
sns.histplot(filtered_df['cnt'], bins=30, ax=ax_dist)
ax_dist.set_title("Distribusi Jumlah Penyewaan")
st.pyplot(fig_dist)

# =========================
# PERTANYAAN 1
# =========================
st.subheader("📌 Distribusi Kategori Penggunaan")

if 'usage_category' not in filtered_df.columns:
    filtered_df['usage_category'] = pd.qcut(
        filtered_df['cnt'], q=3, labels=['Rendah','Sedang','Tinggi']
    )

fig1, ax1 = plt.subplots()
sns.countplot(x='usage_category', data=filtered_df, ax=ax1)
st.pyplot(fig1)

dist = filtered_df['usage_category'].value_counts(normalize=True) * 100
st.write(dist)

# JAWABAN 1
st.markdown("### ✅ Jawaban Pertanyaan 1")

top_category = dist.idxmax()
top_value = dist.max()

st.info(f"""
Kategori penggunaan sepeda didominasi oleh **{top_category}** dengan proporsi sekitar **{top_value:.2f}%**.

Hal ini menunjukkan adanya pola penggunaan tertentu dimana sebagian besar penyewaan berada pada kategori tersebut, 
yang dapat dimanfaatkan untuk strategi operasional seperti pengelolaan stok sepeda.
""")

# =========================
# PERTANYAAN 2
# =========================
st.subheader("📌 Hari Kerja vs Hari Libur")

workingday_avg = filtered_df.groupby('workingday')['cnt'].mean()

fig2, ax2 = plt.subplots()
sns.barplot(x=workingday_avg.index, y=workingday_avg.values, ax=ax2)
ax2.set_xticklabels(['Libur','Hari Kerja'])
st.pyplot(fig2)

# HITUNG SELISIH
libur = workingday_avg.get(0, 0)
kerja = workingday_avg.get(1, 0)

# JAWABAN 2
st.markdown("### ✅ Jawaban Pertanyaan 2")

if libur > 0:
    selisih = ((kerja - libur) / libur) * 100

    st.info(f"""
Rata-rata penyewaan pada hari kerja lebih tinggi sebesar **{selisih:.2f}%** dibanding hari libur.

Hal ini menunjukkan bahwa sepeda lebih banyak digunakan untuk aktivitas rutin seperti bekerja atau sekolah, 
dengan pola yang lebih stabil dibandingkan hari libur yang cenderung fluktuatif.
""")

# LINE CHART
fig3, ax3 = plt.subplots(figsize=(10,5))
sns.lineplot(data=filtered_df, x='dteday', y='cnt', hue='workingday', ax=ax3)
st.pyplot(fig3)

# =========================
# ANALISIS LANJUTAN
# =========================
st.subheader("🚀 Analisis Musiman")

season_avg = filtered_df.groupby('season')['cnt'].mean()

fig4, ax4 = plt.subplots()
sns.barplot(x=season_avg.index, y=season_avg.values, ax=ax4)
st.pyplot(fig4)

st.markdown("""
**Insight:**
- Penyewaan dipengaruhi oleh musim  
- Ada periode dengan demand lebih tinggi  
""")

# =========================
# KESIMPULAN
# =========================
st.subheader("📌 Kesimpulan")

st.markdown("""
- Kategori penggunaan sepeda menunjukkan adanya periode demand tinggi  
- Hari kerja memiliki penyewaan lebih tinggi dibanding hari libur  
- Terdapat pola musiman dalam penggunaan sepeda  

Dashboard ini dapat digunakan untuk:
- Optimalisasi distribusi sepeda  
- Perencanaan operasional  
- Strategi promosi berbasis data  
""")

# =========================
# FOOTER
# =========================
st.markdown("---")
st.markdown("🚀 Sabrina Marliani - Proyek Analisis Data - Streamlit Dashboard")