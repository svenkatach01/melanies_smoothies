# Import python packages
import streamlit as st
import requests


from snowflake.snowpark.functions import col

#session = get_active_session()
cnx = st.connection("snowflake")
session = cnx.session()
# Write directly to the app
st.title(f":cup_with_straw: Customize Your Smoothie!:cup_with_straw:")
st.write(
  """
    Choose the fruits you want in your custom Smoothie!
  """
)

smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
#st.text(smoothiefroot_response.json())
sf_df = st.dataframe(data=smoothifroot_response.json(), use_container_width=True)

name_on_order = st.text_input('Name for the order')
st.write('The name on your Smoothie will be :', name_on_order)
#my_dataframeFruit = session.table("smoothies.public.fruit_options").select(col('fruit_name'))
#my_dataframe = session.table("smoothies.public.orders").filter(col("ORDER_FILLED")==0).collect()
#editable_df = st.data_editor(my_dataframe)


my_dataframe = session.table("smoothies.public.fruit_options").select(col("fruit_name"))
#editable_df = st.data_editor(my_dataframe)
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect('Choose upto to 5 ingredients ',
                                    my_dataframe,
                                    max_selections=5)
if ingredients_list:
    st.write(ingredients_list)
    st.text(ingredients_list)
    ingredients_string=''
    for fruit_selected in ingredients_list:
        ingredients_string += fruit_selected + ' '
    st.write(ingredients_string)
    my_insert_string = """
        insert into smoothies.public.orders(ingredients,name_on_order) 
        values ('""" + ingredients_string + """','""" + name_on_order + """')
    """
    
    st.write(my_insert_string)

    time_to_insert = st.button('Submit Order')
   # st.write(my_insert_string)
    if time_to_insert:
        session.sql(my_insert_string).collect()
        st.success(" Your smoothiee is ordered :" +  name_on_order)
