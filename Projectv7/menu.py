import streamlit as st
from home_page import home_page
from add_data_page import data_page
from presentation import about_page


def render_menu():
    """Render the sidebar menu and handle page navigation."""
    st.sidebar.title("Navigation")
    menu_options = {
        "Home": home_page,
        "Add New Data": data_page,
        "About The App": about_page,
    }
    selected_page = st.sidebar.radio("Select a Page", list(menu_options.keys()))
    menu_options[selected_page]()
