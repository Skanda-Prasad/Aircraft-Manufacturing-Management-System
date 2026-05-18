import streamlit as st
from db import execute_query


def get_order_ids():
    query = "SELECT order_id FROM aircraft_order"
    df = execute_query(query)
    return df['order_id'].tolist() if not df.empty else []


def display_orders():
    st.subheader("Orders")
    orders = execute_query("SELECT * FROM aircraft_order")
    if orders.empty:
        st.warning("No orders found.")
        return
    selected_order_id = st.selectbox("Select an Order", orders['order_id'].tolist())
    new_status = st.selectbox("Select New Order Status", ['Order Placed', 'In Progress', 'Complete'])
    if st.button("Update Order Status"):
        update_query = "UPDATE aircraft_order SET order_status = %s WHERE order_id = %s"
        execute_query(update_query, (new_status, selected_order_id), fetch=False)
        st.success(f"Order status updated to {new_status} for Order ID {selected_order_id}.")


def display_completed_orders():
    st.subheader("Completed Orders")
    completed_orders = execute_query("SELECT * FROM completed_orders")
    st.table(completed_orders)


def edit_order(order_id, new_status):
    update_query = "UPDATE aircraft_order SET order_status = %s WHERE order_id = %s"
    execute_query(update_query, (new_status, order_id), fetch=False)
    st.success(f"Order status updated to {new_status} for Order ID {order_id}.")


def remove_order(order_id):
    delete_query = "DELETE FROM aircraft_order WHERE order_id = %s"
    execute_query(delete_query, (order_id,), fetch=False)
    st.success("Order removed successfully.")


def move_to_completed_orders(order_id):
    move_query = f"INSERT INTO completed_orders SELECT * FROM aircraft_order WHERE order_id = {order_id}"
    execute_query(move_query, fetch=False)


def add_edit_remove_orders():
    st.subheader("Add/Edit/Remove Orders")
    with st.form(key='add_order_form'):
        customer_id_add = st.number_input("Enter Customer ID:")
        date_placed_add = st.date_input("Enter Date Placed:")
        total_cost_add = st.number_input("Enter Total Cost:")
        order_status_add = "Order Placed"
        st.text_input("Order Status:", value=order_status_add, disabled=True)
        add_button = st.form_submit_button("Add Order")
    if add_button:
        insert_query = "INSERT INTO aircraft_order (customer_id, date_placed, order_status, total_cost) VALUES (%s, %s, %s, %s)"
        execute_query(insert_query, (customer_id_add, date_placed_add, order_status_add, total_cost_add), fetch=False)
        st.success("Order added successfully!")

    with st.form(key='edit_order_form'):
        order_id_edit = st.selectbox("Select Order ID to Edit", get_order_ids())
        new_status_edit = st.selectbox("Select New Order Status", ['Order Placed', 'In Progress', 'Complete'])
        edit_button = st.form_submit_button("Update Order")
    if 'edit_button' in locals() and edit_button:
        edit_order(order_id_edit, new_status_edit)
        if new_status_edit == 'Complete':
            move_to_completed_orders(order_id_edit)

    with st.form(key='remove_order_form'):
        order_id_remove = st.selectbox("Select Order ID to Remove", get_order_ids())
        remove_button = st.form_submit_button("Remove Order")
    if 'remove_button' in locals() and remove_button:
        remove_order(order_id_remove)

    orders_df = execute_query("SELECT * FROM aircraft_order")
    st.table(orders_df)


def search_orders_by_date():
    st.subheader("Search Orders by Date")
    date_to_search = st.date_input("Enter Date to Search:")
    if st.button("Search"):
        search_query = "SELECT * FROM aircraft_order WHERE date_placed = %s"
        search_result = execute_query(search_query, (date_to_search,))
        st.table(search_result)


def logout():
    st.subheader("Log Out")
    if st.button("Log Out"):
        st.session_state.authenticated = False
        st.success("Logged out successfully.")
