import streamlit as st
import warnings
from auth import create_user_table, signup, login, check_authentication
from aircraft_models import (
    display_aircraft_models,
    add_edit_remove_aircraft_model,
    add_edit_remove_aircraft_components,
)
from suppliers import display_suppliers, add_edit_remove_suppliers
from customers import display_customers, add_edit_remove_customers
from orders import (
    display_orders,
    display_completed_orders,
    add_edit_remove_orders,
    search_orders_by_date,
    logout,
)


warnings.filterwarnings("ignore", category=UserWarning, module="numpy")
st.set_option('deprecation.showfileUploaderEncoding', False)


def main():
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False

    st.title("Aircraft Management System")
    create_user_table()

    if not st.session_state.authenticated:
        st.subheader("Login")
        login_username = st.text_input("Username:")
        login_password = st.text_input("Password:", type="password")
        if st.button("Login"):
            login(login_username, login_password)
            st.session_state.authenticated = True
            st.experimental_rerun()

        st.subheader("Signup")
        signup_username = st.text_input("Username:", key="signup_username")
        signup_password = st.text_input("Password:", type="password", key="signup_password")
        if st.button("Signup"):
            signup(signup_username, signup_password)

        check_authentication()
    else:
        st.sidebar.subheader("Menu")
        selected_option = st.sidebar.selectbox("Select an Option", ["Aircraft Models", "Suppliers", "Customers", "Orders", "Log Out"])
        if selected_option == "Aircraft Models":
            add_edit_remove_aircraft_model()
            add_edit_remove_aircraft_components()
        elif selected_option == "Suppliers":
            display_suppliers()
            add_edit_remove_suppliers()
        elif selected_option == "Customers":
            display_customers()
            add_edit_remove_customers()
        elif selected_option == "Orders":
            display_completed_orders()
            add_edit_remove_orders()
            search_orders_by_date()
        elif selected_option == "Log Out":
            st.session_state.authenticated = False
            st.experimental_rerun()


if __name__ == "__main__":
    main()
