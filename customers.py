import streamlit as st
from db import execute_query


def get_customer_ids():
    query = "SELECT customer_id FROM customer"
    df = execute_query(query)
    return df['customer_id'].tolist() if not df.empty else []


def display_customers():
    st.subheader("Customers")
    customers = execute_query("SELECT * FROM customer")
    if customers.empty:
        st.warning("No customers found.")
        return
    selected_customer_id = st.selectbox("Select a Customer", customers['customer_id'].tolist())
    join_query = f"SELECT * FROM aircraft_order WHERE customer_id = {selected_customer_id}"
    customer_orders = execute_query(join_query)
    st.table(customer_orders)


def add_edit_remove_customers():
    st.subheader("Add/Edit/Remove Customers")
    with st.form(key='add_customer_form'):
        customer_name_add = st.text_input("Enter Customer Name:")
        contact_info_add = st.text_input("Enter Contact Information:")
        add_customer_button = st.form_submit_button("Save")
    if add_customer_button:
        insert_query = "INSERT INTO customer (customer_name, contact_info) VALUES (%s, %s)"
        execute_query(insert_query, (customer_name_add, contact_info_add), fetch=False)
        st.success("Customer added successfully!")

    with st.form(key='edit_customer_form'):
        customer_id_edit = st.selectbox("Select Customer ID to Edit", get_customer_ids())
        customer_name_edit = st.text_input("Enter Customer Name:")
        contact_info_edit = st.text_input("Enter Contact Information:")
        edit_customer_button = st.form_submit_button("Update")
    if 'edit_customer_button' in locals() and edit_customer_button:
        update_query = "UPDATE customer SET customer_name=%s, contact_info=%s WHERE customer_id=%s"
        execute_query(update_query, (customer_name_edit, contact_info_edit, customer_id_edit), fetch=False)
        st.success("Customer updated successfully!")

    with st.form(key='remove_customer_form'):
        customer_id_remove = st.selectbox("Select Customer ID to Remove", get_customer_ids())
        remove_customer_button = st.form_submit_button("Remove")
    if 'remove_customer_button' in locals() and remove_customer_button:
        delete_query = "DELETE FROM customer WHERE customer_id=%s"
        execute_query(delete_query, (customer_id_remove,), fetch=False)
        st.success("Customer removed successfully!")

    customers_df = execute_query("SELECT * FROM customer")
    st.table(customers_df)
