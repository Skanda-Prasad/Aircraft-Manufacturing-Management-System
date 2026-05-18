import streamlit as st
from db import execute_query


def get_aircraft_models():
    query = "SELECT * FROM aircraft_model"
    df = execute_query(query)
    return df['model_name'].tolist() if not df.empty else []


def get_aircraft_model_ids():
    query = "SELECT DISTINCT model_id FROM aircraft_model"
    df = execute_query(query)
    return df['model_id'].tolist() if not df.empty else []


def display_aircraft_models():
    st.subheader("Aircraft Models")
    aircraft_models = execute_query("SELECT * FROM aircraft_model")
    if aircraft_models.empty:
        st.warning("No Aircraft Models available.")
        return
    selected_model_name = st.selectbox("Select an Aircraft Model", aircraft_models['model_name'].tolist())
    selected_model_id = aircraft_models.loc[aircraft_models['model_name'] == selected_model_name, 'model_id'].values[0]
    if selected_model_id is not None:
        nested_query = f"SELECT * FROM aircraft_component WHERE used_in_model = {selected_model_id}"
        aircraft_components = execute_query(nested_query)
        st.table(aircraft_components)
    else:
        st.warning("Please select an Aircraft Model.")


def add_edit_remove_aircraft_model():
    st.subheader("Add/Edit/Remove Aircraft Model")
    aircraft_models = execute_query("SELECT * FROM aircraft_model")
    st.table(aircraft_models)

    with st.form("add_aircraft_model_form"):
        model_name_add = st.text_input("Enter Model Name:")
        manufacturer_add = st.text_input("Enter Manufacturer:")
        capacity_add = st.number_input("Enter Capacity:")
        max_range_add = st.number_input("Enter Max Range:")
        mtow_add = st.number_input("Enter MTOW:")
        submitted_add = st.form_submit_button("Add Model")
    if submitted_add:
        insert_query = "INSERT INTO aircraft_model (model_name, manufacturer, capacity, max_range, mtow) VALUES (%s, %s, %s, %s, %s)"
        data_add = (model_name_add, manufacturer_add, capacity_add, max_range_add, mtow_add)
        execute_query(insert_query, data_add, fetch=False)
        st.success("Aircraft Model added successfully!")

    selected_model_name_edit = st.text_input("Enter Model Name for Editing:")
    with st.form("edit_aircraft_model_form"):
        model_name_edit = st.text_input("Edit Model Name:")
        manufacturer_edit = st.text_input("Edit Manufacturer:")
        capacity_edit = st.number_input("Edit Capacity:")
        max_range_edit = st.number_input("Edit Max Range:")
        mtow_edit = st.number_input("Edit MTOW:")
        submitted_edit = st.form_submit_button("Save Changes")
    if submitted_edit:
        update_query = """
        UPDATE aircraft_model SET model_name=%s, manufacturer=%s, capacity=%s, max_range=%s, mtow=%s
        WHERE model_name=%s
        """
        execute_query(update_query, (model_name_edit, manufacturer_edit, capacity_edit, max_range_edit, mtow_edit, selected_model_name_edit), fetch=False)
        st.success("Aircraft Model updated successfully!")

    selected_model_name_remove = st.text_input("Enter Model Name for Removal:")
    if st.button("Remove Model"):
        remove_query = "DELETE FROM aircraft_model WHERE model_name = %s"
        execute_query(remove_query, (selected_model_name_remove,), fetch=False)
        st.success("Aircraft Model removed successfully!")


def get_aircraft_component_ids():
    query = "SELECT component_id FROM aircraft_component"
    df = execute_query(query)
    return df['component_id'].tolist() if not df.empty else []


def add_edit_remove_aircraft_components():
    st.subheader("Add/Edit/Remove Aircraft Components")
    with st.form(key='add_form'):
        component_name_add = st.text_input("Enter Component Name:")
        manufacturer_add = st.text_input("Enter Manufacturer:")
        weight_add = st.number_input("Enter Weight:")
        cost_add = st.number_input("Enter Cost:")
        supplier_id_add = st.number_input("Enter Supplier ID:")
        used_in_model_add = st.number_input("Enter Used in Model ID:")
        add_button = st.form_submit_button("Save")
    if add_button:
        insert_query = "INSERT INTO aircraft_component (component_name, manufacturer, weight, cost, supplier_id, used_in_model) VALUES (%s, %s, %s, %s, %s, %s)"
        data = (component_name_add, manufacturer_add, weight_add, cost_add, supplier_id_add, used_in_model_add)
        execute_query(insert_query, data, fetch=False)
        st.success("Aircraft Component added successfully!")

    with st.form(key='edit_form'):
        component_id_edit = st.selectbox("Select Component ID to Edit", get_aircraft_component_ids())
        component_name_edit = st.text_input("Enter Component Name:", key='component_name_edit')
        manufacturer_edit = st.text_input("Enter Manufacturer:", key='manufacturer_edit')
        weight_edit = st.number_input("Enter Weight:", key='weight_edit')
        cost_edit = st.number_input("Enter Cost:", key='cost_edit')
        supplier_id_edit = st.number_input("Enter Supplier ID:", key='supplier_id_edit')
        used_in_model_edit = st.number_input("Enter Used in Model ID:", key='used_in_model_edit')
        edit_button = st.form_submit_button("Update")
    if edit_button:
        update_query = "UPDATE aircraft_component SET component_name=%s, manufacturer=%s, weight=%s, cost=%s, supplier_id=%s, used_in_model=%s WHERE component_id=%s"
        data = (component_name_edit, manufacturer_edit, weight_edit, cost_edit, supplier_id_edit, used_in_model_edit, component_id_edit)
        execute_query(update_query, data, fetch=False)
        st.success("Aircraft Component updated successfully!")

    with st.form(key='remove_form'):
        component_id_remove = st.selectbox("Select Component ID to Remove", get_aircraft_component_ids())
        remove_button = st.form_submit_button("Remove")
    if remove_button:
        delete_query = "DELETE FROM aircraft_component WHERE component_id=%s"
        execute_query(delete_query, (component_id_remove,), fetch=False)
        st.success("Aircraft Component removed successfully!")

    components_df = execute_query("SELECT * FROM aircraft_component")
    st.table(components_df)
