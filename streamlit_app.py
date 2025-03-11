
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


session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('fruit_name'))
st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect (
      'Choseup to 5 ingredients:'
       ,my_dataframe
       ,max_selections=5
    
)

if ingredients_list:
  
    
   ingredients_string = ''
    
   for fruit_chosen in ingredients_list:
       ingredients_string += fruit_chosen + ' '
   #st.write(ingredients_string) 

   my_insert_stmt = """ insert into smoothies.public.orders(ingredients)
            values ('""" + ingredients_string + """')"""



   #st.write(my_insert_stmt)
 
  
   time_to_insert = st.button('submit order')

   if ingredients_string:
    session.sql(my_insert_stmt).collect()
    st.success('Your Smoothie is ordered!', icon="✅")




