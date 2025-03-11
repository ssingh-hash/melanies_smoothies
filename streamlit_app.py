# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

import requests


from snowflake.snowpark.context import get_active_session

st.title(":cup_with_straw: Customise your Smooothie :cup_with_straw:")
st.write(
    f""" Choose the fruits you want in your custom smoothie """ 
)

import streamlit as st

name_on_order = st.text_input("name on smoothie")
st.write(f"The name on your smoothie will be :, {name_on_order}")

cnx = st.connection ("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('fruit_name'),col('search_on'))
#st.dataframe(data=my_dataframe, use_container_width=True)
#st.stop()
#converting snowflake dataframe in to pandas dataframe
pd_df=my_dataframe.to_pandas()
#st.dataframe(pd_df)
#st.stop()

ingredients_list = st.multiselect (
      'Choseup to 5 ingredients:'
       ,my_dataframe
       ,max_selections=5
    
)

ingredients_string = ''

if ingredients_list:

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        #st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
        st.subheader(fruit_chosen + 'Nutrition Information')
        
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + search_on)
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
        
        #st.write(ingredients_string) 
    
    my_insert_stmt = """ insert into smoothies.public.orders(name, ingredients)
        values ('""" + ingredients_string + """', '""" + name_on_order + """')"""

time_to_insert = st.button('submit order')

# my_insert_stmt = """ insert into smoothies.public.orders(ingredients)
#     values ('""" + ingredients_string + """', '""" + name_on_order + """')"""

if ingredients_string:
    session.sql(my_insert_stmt).collect()
    st.success('Your Smoothie is ordered!', icon="✅")




