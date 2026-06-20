import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

st.title("Sales Dashboard")

# 1. Load Data & Clean Spaces
df = pd.read_csv("/Users/harshitvmehta/Desktop/EDA/Product Sales/product_sales_dataset_final.csv")
df.columns = df.columns.str.strip()
df['Order_Date'] = pd.to_datetime(df['Order_Date'], format='%m-%d-%y')

# 2. Add Sidebar Filter
chosen_regions = st.sidebar.multiselect("Select Regions:", df['Region'].unique(), default=df['Region'].unique())
filtered_df = df[df['Region'].isin(chosen_regions)]

# 3. Process Numbers
monthly = filtered_df.set_index('Order_Date').resample('ME')['Revenue'].sum() / 1e6
subcat = filtered_df.groupby('Sub_Category')[['Revenue', 'Profit']].sum() / 1e6
margin = (subcat['Profit'] / subcat['Revenue']) * 100

# 4. Create Side-by-Side Graph Layout
left_box, right_box = st.columns(2)

with left_box:
    st.subheader("Monthly Revenue Track")
    fig1, ax1 = plt.subplots()
    monthly.plot(marker='o', ax=ax1)
    st.pyplot(fig1)

with right_box:
    st.subheader("Strategic Portfolio Matrix")
    fig2, ax2 = plt.subplots()
    sns.scatterplot(x=margin, y=subcat['Revenue'], size=subcat['Profit'], hue=subcat.index, sizes=(40, 300), ax=ax2)
    ax2.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    st.pyplot(fig2)