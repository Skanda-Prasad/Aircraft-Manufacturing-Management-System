import streamlit as st
from db import execute_query


def get_supplier_names():
    query = "SELECT name FROM supplier"
    df = execute_query(query)
    return df['name'].tolist() if not df.empty else []


def display_suppliers():
    st.subheader("Suppliers")
    suppliers = execute_query("SELECT * FROM supplier")
    if suppliers.empty:
        st.warning("No suppliers found.")
        return
    selected_supplier_id = st.selectbox("Select a Supplier", suppliers['supplier_id'].tolist())
    join_query = f"SELECT * FROM aircraft_component WHERE supplier_id = {selected_supplier_id}"
    supplier_components = execute_query(join_query)
    st.table(supplier_components)


def add_edit_remove_suppliers():
    st.subheader("Add/Edit/Remove Suppliers")
    with st.form(key='add_supplier_form'):
        name_add = st.text_input("Enter Supplier Name:")
        contact_info_add = st.text_input("Enter Contact Information:")
        add_supplier_button = st.form_submit_button("Add Supplier")
    if add_supplier_button:
        insert_query = "INSERT INTO supplier (name, contact_info) VALUES (%s, %s)"
        execute_query(insert_query, (name_add, contact_info_add), fetch=False)
        st.success("Supplier added successfully!")

    if st.button("Edit Supplier"):
        selected_supplier = st.selectbox("Select Supplier to Edit", get_supplier_names())
        if selected_supplier:
            edit_query = "SELECT * FROM supplier WHERE name = %s"
            selected_supplier_data = execute_query(edit_query, (selected_supplier,))
            if not selected_supplier_data.empty:
                with st.form(key=f'edit_supplier_form_{selected_supplier}'):
                    name_edit = st.text_input("Edit Supplier Name:", value=selected_supplier_data['name'].iloc[0])
                    contact_info_edit = st.text_input("Edit Contact Information:", value=selected_supplier_data['contact_info'].iloc[0])
                    submitted_edit_supplier = st.form_submit_button("Save Changes")
                if submitted_edit_supplier:
                    update_query = "UPDATE supplier SET name=%s, contact_info=%s WHERE name=%s"
                    execute_query(update_query, (name_edit, contact_info_edit, selected_supplier), fetch=False)
                    st.success("Supplier updated successfully!")

    with st.form(key='remove_supplier_form'):
        selected_supplier_name_remove = st.selectbox("Select Supplier to Remove", get_supplier_names())
        remove_supplier_button = st.form_submit_button("Remove Supplier")
    if 'remove_supplier_button' in locals() and remove_supplier_button:
        remove_query = "DELETE FROM supplier WHERE name = %s"
        execute_query(remove_query, (selected_supplier_name_remove,), fetch=False)
        st.success("Supplier removed successfully!")

    suppliers_df = execute_query("SELECT * FROM supplier")
    st.table(suppliers_df)


def add_edit_remove_supplier_components():
    st.subheader("Add/Edit/Remove Supplier Components")
    if st.button("Add Supplier Component"):
        component_name = st.text_input("Enter Component Name:")
        manufacturer = st.text_input("Enter Manufacturer:")
        weight = st.number_input("Enter Weight:")
        cost = st.number_input("Enter Cost:")
        supplier_id = st.number_input("Enter Supplier ID:")
        if st.button("Save"):
            insert_query = "INSERT INTO aircraft_component (component_name, manufacturer, weight, cost, supplier_id) VALUES (%s, %s, %s, %s, %s)"
            execute_query(insert_query, (component_name, manufacturer, weight, cost, supplier_id), fetch=False)
            st.success("Supplier Component added successfully!")
