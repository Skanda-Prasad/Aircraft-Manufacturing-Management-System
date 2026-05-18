import streamlit as st
import pymysql
import pandas as pd
import warnings

connection = pymysql.connect(host="localhost", user="dbms", password="1234", database="dbms_project")

session_state = st.session_state
privileges = session_state.get('privileges')

# Create a Streamlit app
warnings.filterwarnings("ignore", category=UserWarning, module="numpy")

# Set the Streamlit option
st.set_option('deprecation.showfileUploaderEncoding', False)

# Create user table if it doesn't exist
def create_user_table():
    with connection.cursor() as cursor:
        create_table_query = """
        CREATE TABLE IF NOT EXISTS employee (
            employee_id INT NOT NULL AUTO_INCREMENT,
            username VARCHAR(255) NOT NULL,
            password VARCHAR(255) NOT NULL,
            PRIMARY KEY (employee_id)
        )
        """
        cursor.execute(create_table_query)
        connection.commit()

# Signup function
def signup(username, password):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM employee WHERE username = %s", (username,))
        result = cursor.fetchone()
        if result:
            st.error("Username already exists. Please choose a different username.")
            return
        cursor.execute("INSERT INTO employee (username, password) VALUES (%s, %s)", (username, password))
        connection.commit()
        st.success("Signup successful. You can now log in.")

# Login function
def login(username, password):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM employee WHERE username = %s AND password = %s", (username, password))
        result = cursor.fetchone()
        if result:
            st.session_state.authenticated = True
            st.success("Login successful!")
        else:
            st.error("Invalid username or password.")

# Check for user authentication
def check_authentication():
    if not st.session_state.get('authenticated'):
        st.error("Not authenticated. Please log in.")
        st.stop()

def get_aircraft_models():
    query = "SELECT DISTINCT aircraft_model FROM components"
    models = execute_query(query)
    return models['aircraft_model'].tolist()

def display_aircraft_models():
    st.subheader("Aircraft Models")
    
    # Fetch aircraft models from the database
    query = "SELECT * FROM aircraft_model"
    aircraft_models = execute_query(query)
    
    if aircraft_models.empty:
        st.warning("No Aircraft Models available.")
        return
    
    # Display aircraft models
    selected_model_name = st.selectbox("Select an Aircraft Model", aircraft_models['model_name'].tolist())
    
    # Get the model_id based on the selected model_name
    selected_model_id = aircraft_models.loc[aircraft_models['model_name'] == selected_model_name, 'model_id'].values[0]
    
    if selected_model_id is not None:
        # Display aircraft components for the selected model using a nested query
        nested_query = f"SELECT * FROM aircraft_component WHERE used_in_model = {selected_model_id}"
        aircraft_components = execute_query(nested_query)
    
        st.table(aircraft_components)
    else:
        st.warning("Please select an Aircraft Model.")

def get_aircraft_model_ids():
    query = "SELECT DISTINCT model_id FROM aircraft_model"
    model_ids = execute_query(query)
    return model_ids['model_id'].tolist()

def add_edit_remove_aircraft_model():
    st.subheader("Add/Edit/Remove Aircraft Model")

    # Display existing aircraft models
    query = "SELECT * FROM aircraft_model"
    aircraft_models = execute_query(query)
    st.table(aircraft_models)

    # Add functionality
    st.subheader("Add Aircraft Model")
    with st.form("add_aircraft_model_form"):
        model_name_add = st.text_input("Enter Model Name:")
        manufacturer_add = st.text_input("Enter Manufacturer:")
        capacity_add = st.number_input("Enter Capacity:")
        max_range_add = st.number_input("Enter Max Range:")
        mtow_add = st.number_input("Enter MTOW:")
        submitted_add = st.form_submit_button("Add Model")

    if submitted_add:
        # Insert data into the database
        insert_query = "INSERT INTO aircraft_model (model_name, manufacturer, capacity, max_range, mtow) " \
                       "VALUES (%s, %s, %s, %s, %s)"
        data_add = (model_name_add, manufacturer_add, capacity_add, max_range_add, mtow_add)
        execute_query(insert_query, data_add)
        st.success("Aircraft Model added successfully!")

    # Edit functionality
    st.subheader("Edit Aircraft Model")
    selected_model_name_edit = st.text_input("Enter Model Name for Editing:")
    edit_form = st.form("edit_aircraft_model_form")
    with edit_form:
        model_name_edit = st.text_input("Edit Model Name:")
        manufacturer_edit = st.text_input("Edit Manufacturer:")
        capacity_edit = st.number_input("Edit Capacity:")
        max_range_edit = st.number_input("Edit Max Range:")
        mtow_edit = st.number_input("Edit MTOW:")
        submitted_edit = st.form_submit_button("Save Changes")

    if submitted_edit:
        # Update data in the database
        update_query = f"UPDATE aircraft_model SET model_name = '{model_name_edit}', " \
                       f"manufacturer = '{manufacturer_edit}', capacity = {capacity_edit}, " \
                       f"max_range = {max_range_edit}, mtow = {mtow_edit} " \
                       f"WHERE model_name = '{selected_model_name_edit}'"
        execute_query(update_query)
        st.success("Aircraft Model updated successfully!")


    # Remove functionality
    st.subheader("Remove Aircraft Model")
    selected_model_name_remove = st.text_input("Enter Model Name for Removal:")
    if st.button("Remove Model"):
        # Remove data from the database
        remove_query = f"DELETE FROM aircraft_model WHERE model_name = '{selected_model_name_remove}'"
        execute_query(remove_query)
        st.success("Aircraft Model removed successfully!")
        
    # Dropdown for Aircraft Model
    selected_model_id = st.selectbox("Select Aircraft Model", get_aircraft_model_ids())

    # Display components for the selected aircraft model
    if selected_model_id:
        components_query = f"SELECT * FROM aircraft_component WHERE used_in_model = {selected_model_id}"
        components_df = execute_query(components_query)
        st.subheader(f"Components for Aircraft Model {selected_model_id}")
        st.table(components_df)

def add_edit_remove_aircraft_components():
    st.subheader("Add/Edit/Remove Aircraft Components")

    # Add Form
    add_form = st.form(key='add_form')
    with add_form:
        st.subheader("Add Aircraft Component")
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
        execute_query(insert_query, data)
        st.success("Aircraft Component added successfully!")

    # Edit Form
    edit_form = st.form(key='edit_form')
    with edit_form:
        st.subheader("Edit Aircraft Component")
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
        execute_query(update_query, data)
        st.success("Aircraft Component updated successfully!")

    # Remove Form
    remove_form = st.form(key='remove_form')
    with remove_form:
        st.subheader("Remove Aircraft Component")
        component_id_remove = st.selectbox("Select Component ID to Remove", get_aircraft_component_ids())
        remove_button = st.form_submit_button("Remove")

    if remove_button:
        delete_query = "DELETE FROM aircraft_component WHERE component_id=%s"
        data = (component_id_remove,)
        execute_query(delete_query, data)
        st.success("Aircraft Component removed successfully!")

    # Display current components
    display_query = "SELECT * FROM aircraft_component"
    components_df = execute_query(display_query)
    st.table(components_df)

def get_aircraft_component_ids():
    # Helper function to get a list of aircraft component IDs for dropdowns
    query = "SELECT component_id FROM aircraft_component"
    result = execute_query(query)
    return result['component_id'].tolist()


def display_suppliers():
    st.subheader("Suppliers")
    
    # Fetch suppliers from the database
    query = "SELECT * FROM supplier"
    suppliers = execute_query(query)
    
    # Display suppliers
    selected_supplier_id = st.selectbox("Select a Supplier", suppliers['supplier_id'].tolist())
    
    # Display components supplied by the selected supplier using a join
    join_query = f"SELECT * FROM aircraft_component WHERE supplier_id = {selected_supplier_id}"
    supplier_components = execute_query(join_query)
    
    st.table(supplier_components)

def add_edit_remove_suppliers():
    st.subheader("Add/Edit/Remove Suppliers")
    
    # Add Form
    add_supplier_form = st.form(key='add_supplier_form')
    with add_supplier_form:
        st.subheader("Add Supplier")
        name_add = st.text_input("Enter Supplier Name:")
        contact_info_add = st.text_input("Enter Contact Information:")
        add_supplier_button = st.form_submit_button("Add Supplier")

    if add_supplier_button:
        # Handle form submission outside the form block
        insert_query = "INSERT INTO supplier (name, contact_info) VALUES (%s, %s)"
        data = (name_add, contact_info_add)
        execute_query(insert_query, data)
        st.success("Supplier added successfully!")

    # Edit Form
    selected_supplier_name_edit = None

    if st.button("Edit Supplier"):
        # Select supplier for editing
        selected_supplier_name_edit = st.selectbox("Select Supplier to Edit", get_supplier_names())

    if selected_supplier_name_edit:
        # Fetch existing data for the selected supplier
        edit_query = f"SELECT * FROM supplier WHERE name = '{selected_supplier_name_edit}'"
        selected_supplier_data = execute_query(edit_query)

        if not selected_supplier_data.empty:
            # Display form with existing data for editing
            with st.form(key=f'edit_supplier_form_{selected_supplier_name_edit}'):
                st.subheader("Edit Supplier")
                # Existing data
                st.text_input("Existing Supplier Name:", value=selected_supplier_data['name'].iloc[0], key='old_name', disabled=True)
                st.text_input("Existing Contact Information:", value=selected_supplier_data['contact_info'].iloc[0], key='old_contact_info', disabled=True)
                # New data
                name_edit = st.text_input("Edit Supplier Name:", key='new_name', value=selected_supplier_data['name'].iloc[0])
                contact_info_edit = st.text_input("Edit Contact Information:", key='new_contact_info', value=selected_supplier_data['contact_info'].iloc[0])
                submitted_edit_supplier = st.form_submit_button("Save Changes")

            if submitted_edit_supplier:
                # Update data in the database
                update_query = f"UPDATE supplier SET name = '{name_edit}', contact_info = '{contact_info_edit}' WHERE name = '{selected_supplier_name_edit}'"
                execute_query(update_query)
                st.success("Supplier updated successfully!")

    # Remove Form
    remove_supplier_form = st.form(key='remove_supplier_form')
    with remove_supplier_form:
        st.subheader("Remove Supplier")
        selected_supplier_name_remove = st.selectbox("Select Supplier to Remove", get_supplier_names())
        remove_supplier_button = st.form_submit_button("Remove Supplier")

    if remove_supplier_button:
        # Handle remove form submission outside the form block
        remove_query = f"DELETE FROM supplier WHERE name = '{selected_supplier_name_remove}'"
        execute_query(remove_query)
        st.success("Supplier removed successfully!")

    # Display current suppliers
    display_query = "SELECT * FROM supplier"
    suppliers_df = execute_query(display_query)
    st.table(suppliers_df)

def get_supplier_names():
    # Helper function to get a list of supplier names for dropdowns
    query = "SELECT name FROM supplier"
    result = execute_query(query)
    return result['name'].tolist()


def add_edit_remove_supplier_components():
    st.subheader("Add/Edit/Remove Supplier Components")
    
    # Implement functionality to add, edit, and remove components supplied by a supplier
    # ...
    if st.button("Add Supplier Component"):
        # Add new component supplied by a supplier to the database
        component_name = st.text_input("Enter Component Name:")
        manufacturer = st.text_input("Enter Manufacturer:")
        weight = st.number_input("Enter Weight:")
        cost = st.number_input("Enter Cost:")
        supplier_id = st.number_input("Enter Supplier ID:")
        
        if st.button("Save"):
            insert_query = "INSERT INTO aircraft_component (component_name, manufacturer, weight, cost, supplier_id) VALUES (%s, %s, %s, %s, %s)"
            data = (component_name, manufacturer, weight, cost, supplier_id)
            execute_query(insert_query, data)
            st.success("Supplier Component added successfully!")

    if st.button("Edit Supplier Component"):
        # Edit existing component supplied by a supplier in the database
        # ...
        pass

    if st.button("Remove Supplier Component"):
        # Remove existing component supplied by a supplier from the database
        # ...
        pass

def display_customers():
    st.subheader("Customers")
    
    # Fetch customers from the database
    query = "SELECT * FROM customer"
    customers = execute_query(query)
    
    # Display customers
    selected_customer_id = st.selectbox("Select a Customer", customers['customer_id'].tolist())

    # Display orders placed by the selected customer using a join
    join_query = f"SELECT * FROM aircraft_order WHERE customer_id = {selected_customer_id}"
    customer_orders = execute_query(join_query)
    
    st.table(customer_orders)

def add_edit_remove_customers():
    st.subheader("Add/Edit/Remove Customers")
    
    # Add Form
    add_form = st.form(key='add_customer_form')
    with add_form:
        st.subheader("Add Customer")
        customer_name_add = st.text_input("Enter Customer Name:")
        contact_info_add = st.text_input("Enter Contact Information:")
        add_customer_button = st.form_submit_button("Save")

    if add_customer_button:
        insert_query = "INSERT INTO customer (customer_name, contact_info) VALUES (%s, %s)"
        data = (customer_name_add, contact_info_add)
        execute_query(insert_query, data)
        st.success("Customer added successfully!")

    # Edit Form
    edit_form = st.form(key='edit_customer_form')
    with edit_form:
        st.subheader("Edit Customer")
        customer_id_edit = st.selectbox("Select Customer ID to Edit", get_customer_ids())
        customer_name_edit = st.text_input("Enter Customer Name:")
        contact_info_edit = st.text_input("Enter Contact Information:")
        edit_customer_button = st.form_submit_button("Update")

    if edit_customer_button:
        update_query = "UPDATE customer SET customer_name=%s, contact_info=%s WHERE customer_id=%s"
        data = (customer_name_edit, contact_info_edit, customer_id_edit)
        execute_query(update_query, data)
        st.success("Customer updated successfully!")

    # Remove Form
    remove_form = st.form(key='remove_customer_form')
    with remove_form:
        st.subheader("Remove Customer")
        customer_id_remove = st.selectbox("Select Customer ID to Remove", get_customer_ids())
        remove_customer_button = st.form_submit_button("Remove")

    if remove_customer_button:
        delete_query = "DELETE FROM customer WHERE customer_id=%s"
        data = (customer_id_remove,)
        execute_query(delete_query, data)
        st.success("Customer removed successfully!")

    # Display current customers
    display_query = "SELECT * FROM customer"
    customers_df = execute_query(display_query)
    st.table(customers_df)

def get_customer_ids():
    # Helper function to get a list of customer IDs for dropdowns
    query = "SELECT customer_id FROM customer"
    result = execute_query(query)
    return result['customer_id'].tolist()


def display_orders():
    st.subheader("Orders")
    
    # Fetch orders from the database
    query = "SELECT * FROM aircraft_order"
    orders = execute_query(query)
    
    # Display orders
    selected_order_id = st.selectbox("Select an Order", orders['order_id'].tolist())
    
    # Implement functionality to edit and remove orders
    # ...
    if st.button("Edit Order"):
        # Edit existing order in the database
        # ...
        pass

    if st.button("Remove Order"):
        # Remove existing order from the database
        # ...
        pass

    # Dropdown for order_status
    new_status = st.selectbox("Select New Order Status", ['Order Placed', 'In Progress', 'Complete'])
    
    if st.button("Update Order Status"):
        # Update the order status in the database
        update_query = f"UPDATE aircraft_order SET order_status = '{new_status}' WHERE order_id = {selected_order_id}"
        execute_query(update_query)
        st.success(f"Order status updated to {new_status} for Order ID {selected_order_id}.")

def display_completed_orders():
    st.subheader("Completed Orders")
    
    # Fetch completed orders from the database
    query = "SELECT * FROM completed_orders"
    completed_orders = execute_query(query)
    
    # Display completed orders
    st.table(completed_orders)

def edit_order(order_id, new_status):
    # Edit existing order in the database
    update_query = f"UPDATE aircraft_order SET order_status = '{new_status}' WHERE order_id = {order_id}"
    execute_query(update_query)
    st.success(f"Order status updated to {new_status} for Order ID {order_id}.")

def remove_order(order_id):
    # Remove existing order from the database
    delete_query = f"DELETE FROM aircraft_order WHERE order_id = {order_id}"
    execute_query(delete_query)
    st.success(f"Order removed successfully.")

def move_to_completed_orders(order_id):
    # Move the selected order to the completed_orders table
    # Implement this based on your database schema and requirements
    move_query = f"INSERT INTO completed_orders SELECT * FROM aircraft_order WHERE order_id = {order_id}"
    execute_query(move_query)

def add_edit_remove_orders():
    st.subheader("Add/Edit/Remove Orders")
    
    # Add Form
    add_form = st.form(key='add_order_form')
    with add_form:
    	st.subheader("Add Order")
    	customer_id_add = st.number_input("Enter Customer ID:")
    	date_placed_add = st.date_input("Enter Date Placed:")
    	total_cost_add = st.number_input("Enter Total Cost:")
    	# Set default value for order status
    	order_status_add = "Order Placed"
    	st.text_input("Order Status:", value=order_status_add, disabled=True)
    	insert_query = "INSERT INTO aircraft_order (customer_id, date_placed, order_status, total_cost) VALUES (%s, %s, %s, %s)"
    	data = (customer_id_add, date_placed_add, order_status_add, total_cost_add)
    	execute_query(insert_query, data)
    	st.success("Order added successfully!")
    	add_button = st.form_submit_button("Add Order")

    # Edit Form
    edit_form = st.form(key='edit_order_form')
    with edit_form:
        st.subheader("Edit Order")
        order_id_edit = st.selectbox("Select Order ID to Edit", get_order_ids())
        new_status_edit = st.selectbox("Select New Order Status", ['Order Placed', 'In Progress', 'Complete'])
        edit_button = st.form_submit_button("Update Order")
        

    if edit_button:
        edit_order(order_id_edit, new_status_edit)
        if new_status_edit == 'Complete':
        	move_to_completed_orders(order_id_edit)
        
        

    remove_form = st.form(key='remove_order_form')
    with remove_form:
        st.subheader("Remove Order")
        order_id_remove = st.selectbox("Select Order ID to Remove", get_order_ids())
        remove_button = st.form_submit_button("Remove Order")

    if remove_button:
        remove_order(order_id_remove)

    # Display current orders
    display_query = "SELECT * FROM aircraft_order"
    orders_df = execute_query(display_query)
    st.table(orders_df)

def get_order_ids():
    # Helper function to get a list of order IDs for dropdowns
    query = "SELECT order_id FROM aircraft_order"
    result = execute_query(query)
    return result['order_id'].tolist()

def search_orders_by_date():
    st.subheader("Search Orders by Date")
    
    # Implement functionality to search orders by date_placed
    # ...
    date_to_search = st.date_input("Enter Date to Search:")
    
    if st.button("Search"):
        search_query = f"SELECT * FROM aircraft_order WHERE date_placed = '{date_to_search}'"
        search_result = execute_query(search_query)
        st.table(search_result)

def logout():
    st.subheader("Log Out")
    
    # Implement logout functionality
    if st.button("Log Out"):
        # Update authenticated state to False
        st.session_state.authenticated = False
        st.success("Logged out successfully.")

# Helper function to execute SQL queries and fetch data as a Pandas DataFrame
def execute_query(query, data=None, fetch=True):
    cursor = connection.cursor()
    try:
        if data:
            cursor.execute(query, data)
        else:
            cursor.execute(query)
        connection.commit()
        if fetch and cursor.description is not None:
            result = cursor.fetchall()
            df = pd.DataFrame(result, columns=[desc[0] for desc in cursor.description])
            return df
        else:
            return pd.DataFrame()
    except Exception as e:
        st.error(f"Error: {str(e)}")
        connection.rollback()
        return pd.DataFrame()

# ...

# Streamlit UI
def main():
    # Initialize session state
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False

    st.title("Aircraft Management System")
    create_user_table()

    # Conditionally display login and signup sections
    if not st.session_state.authenticated:
        # Login Section
        st.subheader("Login")
        login_username = st.text_input("Username:")
        login_password = st.text_input("Password:", type="password")
        if st.button("Login"):
            login(login_username, login_password)

            # Set authenticated to True and trigger a re-run of the app
            st.session_state.authenticated = True
            st.experimental_rerun()

        # Signup Section
        st.subheader("Signup")
        signup_username = st.text_input("Username:", key="signup_username")
        signup_password = st.text_input("Password:", type="password", key="signup_password")
        if st.button("Signup"):
            signup(signup_username, signup_password)

        check_authentication()  # Stop execution if not authenticated
    else:
        # Sidebar menu
        st.sidebar.subheader("Menu")
        selected_option = st.sidebar.selectbox("Select an Option", ["Aircraft Models", "Suppliers", "Customers", "Orders", "Log Out"])

        if selected_option == "Aircraft Models":
            add_edit_remove_aircraft_model()
            
            add_edit_remove_aircraft_components()
        elif selected_option == "Suppliers":
            display_suppliers()
            add_edit_remove_suppliers()
            #add_edit_remove_supplier_components()
        elif selected_option == "Customers":
            display_customers()
            add_edit_remove_customers()
        elif selected_option == "Orders":
            #display_orders()
            display_completed_orders()
            add_edit_remove_orders()
            search_orders_by_date()
        elif selected_option == "Log Out":
            # Reset authentication and trigger a re-run of the app
            st.session_state.authenticated = False
            st.experimental_rerun()

if __name__ == "__main__":
    main()
    connection.close()  # Close the database connection
