import pandas
import requests
import snowflake.connector
import streamlit

from urllib.error import URLError

streamlit.title("Restaurant")

streamlit.header('Breakfast Favorites')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
streamlit.dataframe(fruits_to_show)

streamlit.header("Fruityvice Fruit Advice!")


def fruityvice(fruit_choice):
    fruityvice_response = requests.get(f"https://fruityvice.com/api/fruit/{fruit_choice}")
    # transform to dataframe
    return pandas.json_normalize(fruityvice_response.json())


try:
    fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
    if not fruit_choice:
        streamlit.error("Please choose a fruit")
    else:
        fruityvice_normalized = fruityvice(fruit_choice)
        # show contents
        streamlit.dataframe(fruityvice_normalized)
except URLError as e:
    streamlit.error()
    
    
def fruit_load_list():
    with my_cnx.cursor() as cursor:
        cursor.execute("SELECT * FROM fruit_load_list")
        return cursor.fetchall()


if streamlit.button("Get fruit load list"):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    streamlit.dataframe(fruit_load_list())

add_my_fruit = streamlit.text_input('What fruit would you like to add?', 'jackfruit')
streamlit.write("Thanks for adding ", add_my_fruit)

streamlit.stop()

my_cur.execute("insert into PC_RIVERY_DB.PUBLIC.FRUIT_LOAD_LISTvalues ('test')");
