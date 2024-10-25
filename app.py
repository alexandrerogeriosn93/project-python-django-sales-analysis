import pandas as pd
import requests
import streamlit as st
import matplotlib.pyplot as plt

def load_data():
    response = requests.get('http://localhost:8000/api/sales')
    data = response.json()
    return pd.DataFrame(data)


data = load_data()

st.title('Análise de vendas')
st.subheader('Dataset de vendas')
st.dataframe(data)
st.subheader('Gráfico de vendas')

fig, ax = plt.subplots()

data['date'] = pd.to_datetime(data['date'])
data.groupby('date')['quantity'].sum().plot(ax=ax)

ax.set_xlabel('Data')
ax.set_ylabel('Quantidade vendida')

st.pyplot(fig)
