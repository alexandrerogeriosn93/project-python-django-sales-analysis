import pandas as pd
import requests
import streamlit as st
import matplotlib.pyplot as plt

def load_data(start_date=None, end_date=None, product=None):
    url = 'http://localhost:8000/api/sales'
    params = {}

    if start_date:
        params['start_date'] = start_date

    if end_date:
        params['end_date'] = end_date

    if product:
        params['product'] = product

    response = requests.get(url, params=params)
    data = response.json()

    if not isinstance(data, list):
        st.error('Formato inesperado dos dados retornados na API.')
        return pd.DataFrame()

    return pd.DataFrame(data)


st.sidebar.header('Filtros')

start_date = st.sidebar.date_input('Data inicial', pd.to_datetime('2024-01-01'))
end_date = st.sidebar.date_input('Data final', pd.to_datetime('2024-12-31'))
product = st.sidebar.text_input('Produto', '')

data = load_data(start_date=start_date, end_date=end_date, product=product)

st.title('Análise de vendas')
st.subheader('Dataset de vendas')
st.dataframe(data, use_container_width=True)
st.subheader('Gráfico de vendas')

fig, ax = plt.subplots()

data['date'] = pd.to_datetime(data['date'])
data.groupby('date')['quantity'].sum().plot(ax=ax)

ax.set_xlabel('Data')
ax.set_ylabel('Quantidade vendida')

st.pyplot(fig)
