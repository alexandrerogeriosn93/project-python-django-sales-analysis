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

tab = st.selectbox('Escolha uma aba',
    [
        "Tabela com dados",
        "Gráfico de vendas",
        "Análise acumulada e tendências"
    ]
)

match tab:
    case "Tabela com dados":
        st.title('Análise de vendas')
        st.subheader('Dataset de vendas')
        st.dataframe(data, use_container_width=True)
        st.subheader('Exportar dados para CSV')

        csv = data.to_csv(index=False)

        st.download_button(
            label='Baixar dados com CSV',
            data=csv,
            file_name='dados_vendas.csv',
            mime='text/csv'
        )
    case "Gráfico de vendas":
        st.subheader('Gráfico de vendas por data')
        
        fig, ax = plt.subplots()
        data['date'] = pd.to_datetime(data['date'])
        
        data.groupby('date')['quantity'].sum().plot(ax=ax)
        
        ax.set_xlabel('Data')
        ax.set_ylabel('Quantidade vendida')
        
        st.pyplot(fig)

        st.subheader('Gráfico de vendas por produto')

        product_sales = data.groupby('product')['quantity'].sum().reset_index()
        fig_sales, ax_sales = plt.subplots()

        product_sales.plot(kind='bar', x='product', y='quantity', ax=ax_sales)

        ax_sales.set_xlabel('Produto')
        ax_sales.set_ylabel('Quantidade vendida')
        ax_sales.set_title('Vendas por produto')

        st.pyplot(fig_sales)
    case "Análise acumulada e tendências":
        st.subheader('Tendência de vendas mensais')

        data['date'] = pd.to_datetime(data['date'])
        monthly_sales = data.resample('M', on='date')['quantity'].sum().reset_index()
        fig_monthly_sales, ax_monthly_sales = plt.subplots()

        monthly_sales.plot(kind='line', x='date', y='quantity', ax=ax_monthly_sales, marker='o')

        ax_monthly_sales.set_xlabel('Data')
        ax_monthly_sales.set_ylabel('Quantidade vendida')
        ax_monthly_sales.set_title('Tendência de vendas mensais')

        st.pyplot(fig_monthly_sales)

        st.subheader('Vendas acumuladas')

        data['cumulative_quantity'] = data.groupby('date')['quantity'].cumsum()
        fig_cumulative, ax_cumulative = plt.subplots()

        data.groupby('date')['cumulative_quantity'].max().plot(ax=ax_cumulative)

        ax_cumulative.set_xlabel('Data')
        ax_cumulative.set_ylabel('Quantidade vendida acumulada')
        ax_cumulative.set_title('Vendas acumuladas ao longo do tempo')

        st.pyplot(fig_cumulative)
