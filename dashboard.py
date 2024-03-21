import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import plotly.graph_objects as go
from babel.numbers import format_currency

st.header('Analisis Data E-Commerce Public Dataset')
st.write('source: https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce')

sns.set(style='whitegrid')

tab1, tab2, tab3 = st.tabs(["Rekap", "Trend", "RFM Analysis"])

with tab1:
    # Load dataset yang digunakan
    orders_join_order_items_join_products_df = pd.read_csv("orders_join_order_items_join_products_df.csv")

    def product_count(df):
        product_count = df.groupby(by="product_category_name").product_id.count().sort_values(ascending=False)
        return product_count

    top_categories = product_count(orders_join_order_items_join_products_df).head(5)
    bottom_categories = product_count(orders_join_order_items_join_products_df).tail(5).sort_values()

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))

    st.subheader('Top 5 Kategori Produk Berdasarkan Total Order')

    # Visualisasi Bar Chart untuk Top 5 Kategori Produk Total Order Tertinggi
    top_categories.plot(kind='barh', color=['#90CAF9' if cat == top_categories.index[0] else '#D3D3D3' for cat in top_categories.index], ax=ax1)
    ax1.set_title('Total Order Tertinggi')
    ax1.set_xlabel('Jumlah Order')
    ax1.set_ylabel('Kategori Produk')
    ax1.invert_yaxis()
    ax1.yaxis.grid(True, linestyle='--', linewidth=0.1)
    ax1.tick_params(axis='y', which='major', pad=2)

    # Visualisasi Bar Chart untuk Top 5 Kategori Produk Total Order Terendah
    bottom_categories.plot(kind='barh', color=['#90CAF9' if cat == top_categories.index[0] else '#D3D3D3' for cat in top_categories.index], ax=ax2)
    ax2.set_title('Total Order Terendah')
    ax2.set_xlabel('Jumlah Order')
    ax2.set_ylabel('Kategori Produk')
    ax2.yaxis.set_label_position("right")
    ax2.yaxis.tick_right()
    ax2.invert_xaxis()
    ax2.invert_yaxis()
    ax2.yaxis.grid(True, linestyle='--', linewidth=0.1)
    ax2.tick_params(axis='y', which='major', pad=2)

    plt.tight_layout()
    st.pyplot(fig)

    def product_price_sum(df):
        delivered_orders_df = df[
        (df['order_status'] != 'canceled') &
        (df['order_status'] != 'unavailable')]
        product_price_sum = delivered_orders_df.groupby('product_category_name')['total'].sum().sort_values(ascending=False)
        return product_price_sum
    
    #Total Nilai Order
    top_categories = product_price_sum(orders_join_order_items_join_products_df).head(5)
    bottom_categories = product_price_sum(orders_join_order_items_join_products_df).tail(5).sort_values()

    st.subheader('Top 5 Kategori Produk Berdasarkan Total Nilai Order')
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))

    # Visualisasi Bar Chart untuk Top 5 Kategori Produk Total Nilai Order Tertinggi
    top_categories.plot(kind='barh', color=['#90CAF9' if cat == top_categories.index[0] else '#D3D3D3' for cat in top_categories.index], ax=ax1)
    ax1.set_title('Total nilai order tertinggi')
    ax1.set_xlabel('Total Nilai Order (Real Brazil)')
    max_revenue = top_categories.max()
    xticks_values = range(0, int(max_revenue) + 100000, 300000)
    xticks_labels = [f'{value/1e6:.2f}M' for value in xticks_values]
    ax1.set_xticks(xticks_values)
    ax1.set_xticklabels(xticks_labels)
    ax1.set_ylabel('Kategori Produk')
    ax1.invert_yaxis()

    # Visualisasi Bar Chart untuk Top 5 Kategori Produk Total Nilai Order Terendah
    bottom_categories.plot(kind='barh', color=['#90CAF9' if cat == bottom_categories.index[0] else '#D3D3D3' for cat in bottom_categories.index], ax=ax2)
    ax2.set_title('Total nilai order terendah')
    ax2.set_xlabel('Total Nilai Order (Real Brazil)')
    max_revenue = bottom_categories.max()
    xticks_values = range(0, int(max_revenue) + 200, 300)
    xticks_labels = [f'{value/1:.1f}' for value in xticks_values]
    ax2.set_xticks(xticks_values)
    ax2.set_xticklabels(xticks_labels)
    ax2.set_ylabel('Kategori Produk')
    ax2.yaxis.set_label_position("right")
    ax2.yaxis.tick_right()
    ax2.invert_xaxis()
    ax2.invert_yaxis()

    plt.tight_layout()
    st.pyplot(fig)

with tab2:
    # Load dataset yang digunakan
    order_reviews_df = pd.read_csv("order_reviews_df.csv")
    orders_df = pd.read_csv("orders_df.csv")

    def monthly_customers_count(df):
        df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])
        monthly_customers_count = df.groupby(
            df['order_purchase_timestamp'].dt.strftime('%Y-%m')
        )['product_id'].count()
        return monthly_customers_count

    def monthly_revenue_trend(df):
        df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])
        delivered_orders_df = df[
        (df['order_status'] != 'canceled') &
        (df['order_status'] != 'unavailable')]
        monthly_revenue_trend = delivered_orders_df.groupby(delivered_orders_df['order_purchase_timestamp'].dt.strftime('%Y-%m'))['total'].sum()
        return monthly_revenue_trend
    
    def monthly_review_percentages(df):
        df['review_creation_date'] = pd.to_datetime(df['review_creation_date'])
        df['year_month'] = df['review_creation_date'].dt.strftime('%Y-%m')
        monthly_review_counts = df.groupby(['year_month', 'review_score']).size().unstack(fill_value=0)
        monthly_review_totals = monthly_review_counts.sum(axis=1)
        monthly_review_percentages = monthly_review_counts.div(monthly_review_totals, axis=0) * 100
        return monthly_review_percentages

    def monthly_review_avg(df):
        df['review_creation_date'] = pd.to_datetime(df['review_creation_date'])
        df['year_month'] = df['review_creation_date'].dt.strftime('%Y-%m')
        monthly_review_avg = df.groupby('year_month')['review_score'].mean()
        return monthly_review_avg
    
    def order_status_percentages_year(df):
        df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])
        df['order_year'] = df['order_purchase_timestamp'].dt.strftime('%Y-%m')
        order_status_counts_year = df.groupby(['order_year', 'order_status'])['order_id'].nunique().unstack(fill_value=0)
        total_orders_per_year = order_status_counts_year.sum(axis=1)
        order_status_percentages_year = order_status_counts_year.divide(total_orders_per_year, axis=0) * 100
        return order_status_percentages_year
    
    col1, col2 = st.columns(2)

    with col1:
        # Total Order Keseluruhan
        total_orders = len(orders_join_order_items_join_products_df)
        st.metric("Total Order Keseluruhan", value=total_orders)

        st.markdown("<h4 style='text-align: center;'>Trend Total Order Bulanan</h4>", unsafe_allow_html=True)
        st.line_chart(monthly_customers_count(orders_join_order_items_join_products_df), use_container_width=True)
    with col2:    
        # Total Nilai Order Keseluruhan
        total_order_value = orders_join_order_items_join_products_df['total'].sum()
        formatted_total_order_value = format_currency(total_order_value, 'BRL', locale='pt_BR')
        st.metric("Total Nilai Order Keseluruhan:", value=formatted_total_order_value)

        st.markdown("<h4 style='text-align: center;'>Trend Total Nilai Order Bulanan</h4>", unsafe_allow_html=True)
        st.line_chart(monthly_revenue_trend(orders_join_order_items_join_products_df), use_container_width=True)

    # Review Score Keseluruhan
    avg_review_score = round(order_reviews_df['review_score'].mean(), 2)
    st.metric("Review Score Keseluruhan:", value=avg_review_score)

    col1, col2 = st.columns(2)

    with col1: 
        st.markdown("<h4 style='text-align: center;'>Trend Persentase Review Score Bulanan</h4>", unsafe_allow_html=True)
        st.line_chart(monthly_review_percentages(order_reviews_df), use_container_width=True)
    with col2:
        st.markdown("<h4 style='text-align: center;'>Trend Rata-rata Review Score Bulanan</h4>", unsafe_allow_html=True)
        st.line_chart(monthly_review_avg(order_reviews_df), use_container_width=True)

    ### Menampilkan visualisasi line chart masing-masing order status
    st.header("Line Chart Persentase Status Order Bulanan")

    # Menentukan jumlah bar chart per baris
    max_cols_per_row = 2

    # Menghitung jumlah baris dan kolom untuk subplot
    num_status = len(order_status_percentages_year(orders_df).columns)
    num_rows = (num_status + max_cols_per_row - 1) // max_cols_per_row
    num_cols = min(num_status, max_cols_per_row)

    # Membuat subplot untuk setiap jenis status order
    figs = []

    for i, status in enumerate(order_status_percentages_year(orders_df).columns):
        fig = go.Figure()
        x = order_status_percentages_year(orders_df).index
        y = order_status_percentages_year(orders_df)[status]
        fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name=f'Order Status: {status}'))
        fig.update_layout(
            title=f"Persentase Status Order: {status}",
            xaxis_title="Waktu",
            yaxis_title="Persentase Order Status",
        )
        figs.append(fig)

    # Menampilkan plot dalam dua kolom per baris
    for i in range(0, num_status, 2):
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(figs[i], use_container_width=True)
        with col2:
            if i + 1 < num_status:
                st.plotly_chart(figs[i + 1], use_container_width=True)

with tab3:
    customers_join_orders_join_order_items_df = pd.read_csv("customers_join_orders_join_order_items_df.csv")

    st.header('RFM Analysis')

    def calculate_rfm(df):
        # Ubah kolom tanggal menjadi tipe data datetime
        df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])

        rec_df = df.groupby(by="customer_unique_id", as_index=False).agg(
            recency=("order_purchase_timestamp", lambda x: (df['order_purchase_timestamp'].max() - x.max()).days)
        )

        freq_df = df.groupby(by="customer_unique_id", as_index=False).agg(
            frequency=("order_id", "nunique")  # menghitung jumlah order
        )

        monetary_df = df.groupby(by="customer_unique_id", as_index=False).agg(
            monetary=("total", "sum")  # menghitung total jumlah uang untuk pemesanan
        )

        return rec_df, freq_df, monetary_df
    
    rec_df, freq_df, monetary_df = calculate_rfm(customers_join_orders_join_order_items_df)

    col1, col2, col3 = st.columns(3)

    with col1:
        avg_recency = round(rec_df['recency'].mean(), 2)
        st.metric("Average Recency", value=avg_recency)
        rec_df = rec_df.sort_values(by='recency', ascending=False).head(5)
        st.bar_chart(rec_df.set_index('customer_unique_id')['recency'])

    with col2:
        avg_frequenct = round(freq_df['frequency'].mean(), 2)
        st.metric("Average Frequency", value=avg_frequenct)
        freq_df = freq_df.sort_values(by='frequency', ascending=False).head(5)
        st.bar_chart(freq_df.set_index('customer_unique_id')['frequency'])

    with col3:
        avg_monetary = format_currency(monetary_df['monetary'].mean(), "BRL", locale='pt_BR') 
        st.metric("Average Monetary", value=avg_monetary)
        monetary_df = monetary_df.sort_values(by='monetary', ascending=False).head(5)
        st.bar_chart(monetary_df.set_index('customer_unique_id')['monetary'])