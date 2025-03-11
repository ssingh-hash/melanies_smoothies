# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

import requests


from snowflake.snowpark.context import get_active_session

helpful_links = [
    "https://docs.streamlit.io",
    "https://docs.snowflake.com/en/developer-guide/streamlit/about-streamlit",
    "https://github.com/Snowflake-Labs/snowflake-demo-streamlit",
    "https://docs.snowflake.com/en/release-notes/streamlit-in-snowflake"
]

# Write directly to the app
st.title("Example Streamlit App :balloon:")
st.write(
    f"""Replace the code in this example app with your own code! And if you're new to Streamlit, here are some helpful links:

    • :page_with_curl: [Streamlit open source documentation]({helpful_links[0]})
    • :snow: [Streamlit in Snowflake documentation]({helpful_links[1]}) 
    • :books: [Demo repo with templates]({helpful_links[2]})
    • :memo: [Streamlit in Snowflake release notes]({helpful_links[3]})
    """
)

st.title(":cup_with_straw: Customise your Smooothie :cup_with_straw:")
st.write(
    f""" Choose the fruits you want in your custom smoothie """ 
)

import streamlit as st

name_on_order = st.text_input("name on smoothie")
st.write("The name on your smoothie will be :", name_on_order)

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

if ingredients_list:
  
    
   ingredients_string = ''
    
   for fruit_chosen in ingredients_list:
       ingredients_string += fruit_chosen + ' '

       search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
       st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
       smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
       sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

   #st.write(ingredients_string) 

   my_insert_stmt = """ insert into smoothies.public.orders(ingredients)
            values ('""" + ingredients_string + """')"""



 
  
   time_to_insert = st.button('submit order')

   if ingredients_string:
    session.sql(my_insert_stmt).collect()
    st.success('Your Smoothie is ordered!', icon="✅")




