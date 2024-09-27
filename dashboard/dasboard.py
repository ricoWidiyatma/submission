import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')


def get_total_hour_df(df):
    # Menghitung total sepeda yang dipinjam per jam
    hour_count_df = df.groupby("hr").agg({"cnt": "sum"}).reset_index()
    return hour_count_df

def count_by_day_df(df):
    # Mengambil data rentang waktu yang sesuai
    day_df_count = df[(df['dteday'] >= "2011-01-01") & (df['dteday'] < "2012-12-31")]
    return day_df_count

def total_registered_df(df):
    # Menghitung total sepeda yang terdaftar setiap hari
    reg_df = df.groupby(by="dteday").agg({"registered": "sum"}).reset_index()
    reg_df.rename(columns={"registered": "register_sum"}, inplace=True)
    return reg_df

def total_casual_df(df):
    # Menghitung total sepeda yang disewa oleh pengguna kasual
    cas_df = df.groupby(by="dteday").agg({"casual": "sum"}).reset_index()
    cas_df.rename(columns={"casual": "casual_sum"}, inplace=True)
    return cas_df

def create_season_df(df):
    # Menghitung total penyewaan berdasarkan musim
    season_df = df.groupby("season").agg({'cnt': 'sum'}).reset_index()
    season_df.rename(columns={"cnt": "total_rides"}, inplace=True)
    return season_df

def create_working_df(df):
    # Menghitung total penyewaan berdasarkan hari kerja atau libur
    working_df = df.groupby("workingday").agg({'cnt': 'sum'}).reset_index()
    working_df.rename(columns={"cnt": "total_rides"}, inplace=True)
    return working_df

def create_hour_df(df):
    # Menghitung total penyewaan berdasarkan jam
    hour_df = df.groupby("hr").agg({'cnt': 'sum'}).reset_index()
    hour_df.rename(columns={"cnt": "total_rides"}, inplace=True)
    return hour_df


# Load and preprocess data
main_data = pd.read_csv('https://github.com/ricoWidiyatma/submission1/raw/refs/heads/main/dashboard/main_data.csv')
main_data['dteday'] = pd.to_datetime(main_data['dteday'])
main_data.sort_values(by='dteday', inplace=True)

# Date range selection
min_date = main_data['dteday'].min()
max_date = main_data['dteday'].max()

with st.sidebar:
    st.image("submission1/dashboard/logo_bike.png")
    start_date, end_date = st.date_input(
        label='Rentang Waktu', min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = main_data[(main_data['dteday'] >= pd.Timestamp(start_date)) & 
                    (main_data['dteday'] <= pd.Timestamp(end_date))]

# Create dataframes for visualizations
hour_count_df = get_total_hour_df(main_df)
day_df_count_df = count_by_day_df(main_df)
reg_df = total_registered_df(main_df)
cas_df = total_casual_df(main_df)
season_df = create_season_df(main_df)
working_df = create_working_df(main_df)
hour_df = create_hour_df(main_df)

# Streamlit dashboard layout
st.header('Bike Sharing Dashboard :bike:')
st.subheader('Daily Sharing')
col1, col2, col3 = st.columns(3)

with col1:
    total_orders = main_df['cnt'].sum()
    st.metric("Total Sharing Bike", value=total_orders)

with col2:
    total_sum = reg_df['register_sum'].sum()
    st.metric("Total Registered", value=total_sum)

with col3:
    total_sum = cas_df['casual_sum'].sum()
    st.metric("Total Casual", value=total_sum)

st.subheader('Total Penyewaan Sepeda Harian')


st.subheader("Penyewaan Sepeda Berdasarkan Musim")

fig, ax = plt.subplots(figsize=(10, 6))

sns.barplot(x='mnth', y='cnt', data=main_df, hue='yr', palette='viridis', ax=ax)
ax.set_title('Rental Sepeda Berdasarkan Bulan dan Tahun', fontsize=20)
ax.set_xlabel('Bulan', fontsize=14)
ax.set_ylabel('Jumlah Rental', fontsize=14)
ax.legend(title='Tahun', loc='upper right')

st.pyplot(fig)

st.subheader("Penyewaan Berdasarkan Hari Kerja dan Libur")

fig, ax = plt.subplots(figsize=(10, 6))


sns.barplot(x='workingday', y='cnt', data=main_df, hue='season', palette='coolwarm', ax=ax)
ax.set_title('Rental Sepeda Berdasarkan Hari Kerja dan Musim', fontsize=20)
ax.set_xlabel('Hari Kerja (1 = Ya, 0 = Tidak)', fontsize=14)
ax.set_ylabel('Jumlah Rental', fontsize=14)
ax.legend(title='Musim', loc='upper right')

st.pyplot(fig)

st.subheader("Penyewaan Berdasarkan Jam")
fig, ax = plt.subplots(figsize=(10, 6))

sns.barplot(x="hr", y="cnt", data=main_df, hue='yr', palette="viridis", ax=ax)
ax.set_title("Penyewaan Berdasarkan Jam", fontsize=20)
ax.set_xlabel("Jam", fontsize=14)
ax.set_ylabel("Jumlah Rental", fontsize=14)

ax.legend(title='Tahun', loc='upper right')

st.pyplot(fig)

st.caption('Copyright (c) Dicoding 2024 Rico Widiyatma ID')
