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

    # Mapping season
    season_map = {
        1: "Spring",
        2: "Summer",
        3: "Fall",
        4: "Winter"
    }

    # Mapping month
    month_map = {
        1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr",
        5: "May", 6: "Jun", 7: "Jul", 8: "Aug",
        9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"
    }

    df['season_name'] = df['season'].map(season_map)
    df['month_name'] = df['month'].map(month_map)

    return df

df = load_data()

# =========================
# SIDEBAR FILTER
# =========================
st.sidebar.header("🔎 Filter Data")

year = st.sidebar.multiselect(
    "📅 Pilih Tahun",
    options=sorted(df['year'].unique()),
    default=sorted(df['year'].unique())
)

month = st.sidebar.multiselect(
    "📆 Pilih Bulan",
    options=list(df['month_name'].unique()),
    default=list(df['month_name'].unique())
)

season = st.sidebar.multiselect(
    "🌦️ Pilih Musim",
    options=list(df['season_name'].unique()),
    default=list(df['season_name'].unique())
)

filtered_df = df[
    (df['year'].isin(year)) &
    (df['month_name'].isin(month)) &
    (df['season_name'].isin(season))
]

# =========================
# PERTANYAAN BISNIS
# =========================
st.subheader("📌 Pertanyaan Bisnis")

st.markdown("""
1. Bagaimana distribusi tingkat penggunaan sepeda (rendah, sedang, tinggi)?  
2. Bagaimana perbedaan penyewaan sepeda antara hari kerja dan hari libur?
""")

# =========================
# METRICS
# =========================
st.subheader("📊 Ringkasan Data")

col1, col2, col3 = st.columns(3)

col1.metric("Total Penyewaan", f"{int(filtered_df['cnt'].sum()):,}")
col2.metric("Rata-rata Harian", f"{int(filtered_df['cnt'].mean()):,}")
col3.metric("Penyewaan Maksimum", f"{int(filtered_df['cnt'].max()):,}")

# =========================
# DISTRIBUSI
# =========================
st.subheader("📊 Distribusi Jumlah Penyewaan")

fig_dist, ax_dist = plt.subplots()
sns.histplot(filtered_df['cnt'], bins=30, ax=ax_dist)
ax_dist.set_xlabel("Jumlah Penyewaan")
ax_dist.set_ylabel("Frekuensi")
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
ax1.set_xlabel("Kategori Penggunaan")
ax1.set_ylabel("Jumlah Data")
st.pyplot(fig1)

dist = filtered_df['usage_category'].value_counts(normalize=True) * 100
st.write("Distribusi (%):")
st.write(dist)

# Insight Q1
st.markdown("### ✅ Jawaban Pertanyaan 1")

top_category = dist.idxmax()
top_value = dist.max()

st.info(f"""
Sebaran penggunaan sepeda terbagi ke dalam tiga kategori, yaitu rendah, sedang, dan tinggi. 
Dari hasil analisis, kategori **{top_category}** menjadi yang paling dominan dengan proporsi sekitar **{top_value:.2f}%**.

Pembagian kategori ini menggunakan metode kuantil (qcut), sehingga jumlah data pada tiap kategori relatif seimbang. 
Namun demikian, kategori **tinggi** merepresentasikan periode dengan jumlah penyewaan paling besar.

Artinya, terdapat waktu-waktu tertentu di mana permintaan sepeda meningkat secara signifikan. 
Bagi pengelola layanan, kondisi ini penting karena dapat dimanfaatkan untuk:
- menambah jumlah sepeda yang tersedia  
- memastikan ketersediaan di lokasi strategis  
- memaksimalkan potensi pendapatan  
""")

# =========================
# PERTANYAAN 2
# =========================
st.subheader("📌 Hari Kerja vs Hari Libur")

workingday_avg = filtered_df.groupby('workingday')['cnt'].mean()

fig2, ax2 = plt.subplots()
sns.barplot(x=workingday_avg.index, y=workingday_avg.values, ax=ax2)
ax2.set_xticklabels(['Hari Libur','Hari Kerja'])
ax2.set_ylabel("Rata-rata Penyewaan")
st.pyplot(fig2)

libur = workingday_avg.get(0, 0)
kerja = workingday_avg.get(1, 0)

st.markdown("### ✅ Jawaban Pertanyaan 2")

if libur > 0:
    selisih = ((kerja - libur) / libur) * 100

    st.info(f"""
Rata-rata penyewaan sepeda pada **hari kerja** lebih tinggi sekitar **{selisih:.2f}%** dibandingkan hari libur.

Hal ini menunjukkan bahwa sepeda lebih sering digunakan untuk aktivitas rutin seperti bekerja atau sekolah. 
Pada hari kerja, pola penyewaan cenderung lebih stabil karena mengikuti aktivitas harian masyarakat.

Sebaliknya, pada hari libur, jumlah penyewaan lebih fluktuatif. Hal ini kemungkinan dipengaruhi oleh aktivitas rekreasi, 
cuaca, atau kebiasaan pengguna yang tidak tetap.

Dari sisi bisnis, hal ini bisa dimanfaatkan untuk:
- memastikan ketersediaan sepeda lebih banyak di hari kerja  
- membuat promo khusus di hari libur untuk meningkatkan penggunaan  
- mengatur strategi operasional berdasarkan pola permintaan  
""")

# LINE CHART
fig3, ax3 = plt.subplots(figsize=(10,5))
sns.lineplot(data=filtered_df, x='dteday', y='cnt', hue='workingday', ax=ax3)
ax3.set_title("Tren Penyewaan Sepeda dari Waktu ke Waktu")
st.pyplot(fig3)

# =========================
# ANALISIS MUSIM
# =========================
st.subheader("🚀 Pengaruh Musim terhadap Penyewaan")

season_avg = filtered_df.groupby('season_name')['cnt'].mean()

fig4, ax4 = plt.subplots()
sns.barplot(x=season_avg.index, y=season_avg.values, ax=ax4)
ax4.set_xlabel("Musim")
ax4.set_ylabel("Rata-rata Penyewaan")
st.pyplot(fig4)

st.markdown("""
**Insight:**

Jumlah penyewaan sepeda berbeda pada setiap musim, yang menunjukkan bahwa faktor lingkungan seperti cuaca 
memiliki pengaruh terhadap perilaku pengguna.

Pada musim dengan rata-rata penyewaan tinggi, kemungkinan kondisi cuaca lebih mendukung aktivitas bersepeda, 
misalnya tidak terlalu panas atau tidak hujan.

Sebaliknya, pada musim dengan penyewaan rendah, kemungkinan terdapat hambatan seperti cuaca ekstrem atau kondisi jalan yang kurang nyaman.

Informasi ini penting untuk:
- merencanakan jumlah sepeda yang tersedia  
- menentukan waktu yang tepat untuk promosi  
- mengantisipasi penurunan permintaan  
""")

# =========================
# KESIMPULAN
# =========================
st.subheader("📌 Kesimpulan")

st.markdown("""
Dari hasil analisis data penyewaan sepeda, dapat disimpulkan bahwa:

- Penggunaan sepeda memiliki pola tertentu dengan adanya kategori rendah, sedang, dan tinggi  
- Hari kerja menunjukkan tingkat penyewaan yang lebih tinggi dibanding hari libur  
- Faktor musim juga mempengaruhi jumlah penyewaan  

Secara keseluruhan, pola ini dapat dimanfaatkan untuk:
- mengoptimalkan distribusi sepeda  
- meningkatkan efisiensi operasional  
- menyusun strategi bisnis berbasis data  
""")

# =========================
# FOOTER
# =========================
st.markdown("---")
st.markdown("🚀 Sabrina Marliani - Proyek Analisis Data")