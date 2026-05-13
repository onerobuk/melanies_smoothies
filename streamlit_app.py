import streamlit as st
import requests
from snowflake.snowpark.functions import col

st.title(f":cup_with_straw: Customize Your Smoothie! :cup_with_straw: ")
st.write(
  """Choose 5 fruits you want in your smoothie
  """
)

name_on_order = st.text_input("Name for your order: ")
st.write("The name for your order is ", name_on_order)

cnx = st.connection('snowflake')
session=cnx.session()
my_dataframe=session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    my_dataframe,
    max_selections=5
)
if ingredients_list:
    ingredients_string=''
    for fruit in ingredients_list:
        ingredients_string+=fruit + " "
        smoothiefruit_response = requests.get(f"https://my.smoothiefroot.com/api/fruit/{fruit}")
        sf_df = st.dataframe(data=smoothiefruit_response.json(),use_container_width=True)
  
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
                    values ('""" + ingredients_string + """ ',' """ +name_on_order+ """')"""
    time_to_insert = st.button('Submit Order')
    if ingredients_string and time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered, '+name_on_order+'!', icon="✅")

