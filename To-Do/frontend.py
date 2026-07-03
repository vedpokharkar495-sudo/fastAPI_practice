# Import necessary libraries
import streamlit as st
import requests
import json
import time

# Set page configuration
# This controls the title and layout of our Streamlit app
st.set_page_config(page_title="Todo CRUD App", layout="wide", initial_sidebar_state="expanded")

# Add title and styling
st.title("Todo CRUD Application")
st.markdown("---")

# Sidebar for adding new todos
st.sidebar.header("Add New Todo")

# Input fields in sidebar
new_title = st.sidebar.text_input("Title:", help="Enter todo title")
new_description = st.sidebar.text_area("Description:", help="Enter todo description", height=80)
is_completed = st.sidebar.checkbox("Mark as completed", value=False)

# Button to submit new todo
if st.sidebar.button("Add Todo"):
    # Prepare the data to send to the backend
    todo_data = {
        "title": new_title,
        "description": new_description,
        "completed": is_completed
    }

    # API URL for creating todos
    api_url = "http://localhost:8000/todos"

    try:
        # Send POST request to create new todo
        response = requests.post(api_url, json=todo_data)

        if response.status_code == 200:
            # On success, show success message
            st.success(f"'{new_title}' added successfully!")
            # Clear the input fields
            new_title = ""
            new_description = ""
            is_completed = False
        else:
            # On failure, show error message
            st.error(f"Failed to add todo: {response.text}")
    except requests.exceptions.RequestException as e:
        # Handle connection errors
        st.error(f"Connection error: {str(e)}")
        st.info("Make sure FastAPI server is running on http://localhost:8000")

# Main content area for displaying todos
st.markdown("## Todo List")


# Function to fetch todos from backend
def fetch_todos():
    try:
        response = requests.get("http://localhost:8000/todos")
        if response.status_code == 200:
            return response.json()
        return []
    except requests.exceptions.RequestException:
        return []


# Function to fetch a specific todo
def fetch_todo_by_id(todo_id):
    try:
        response = requests.get(f"http://localhost:8000/todos/{todo_id}")
        if response.status_code == 200:
            return response.json()
        return None
    except requests.exceptions.RequestException:
        return None


# Function to update a todo
def update_todo(todo_id, updated_data):
    try:
        response = requests.put(f"http://localhost:8000/todos/{todo_id}", json=updated_data)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False


# Function to delete a todo
def delete_todo(todo_id):
    try:
        response = requests.delete(f"http://localhost:8000/todos/{todo_id}")
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False


# Fetch todos from backend
todos = fetch_todos()

# Display todos in columns
if todos:
    # Filter todos by status using session state
    if 'filter_by' not in st.session_state:
        st.session_state.filter_by = "all"

    filter_option = st.selectbox(
        "Filter todos:",
        ["all", "active", "completed"],
        key="filter_option"
    )

    # Apply filter
    if filter_option == "active":
        filtered_todos = [todo for todo in todos if not todo['completed']]
    elif filter_option == "completed":
        filtered_todos = [todo for todo in todos if todo['completed']]
    else:
        filtered_todos = todos

    # Display filtered todos
    for todo in filtered_todos:
        # Create a container for each todo
        with st.container():
            # Display todo details
            col1, col2, col3 = st.columns([2, 1, 1])

            with col1:
                st.markdown(f"### {todo['id']}. {todo['title']}")
                if todo['description']:
                    st.write(f"📝 *{todo['description']}*")

                # Status indicator
                if todo['completed']:
                    st.success("✅ Completed")
                else:
                    st.warning("⏳ Pending")

            with col2:
                # Edit button
                if st.button("Edit", key=f"edit_{todo['id']}", help="Click to edit this todo"):
                    st.session_state.editing_id = todo['id']
                    st.session_state.editing_title = todo['title']
                    st.session_state.editing_description = todo['description']
                    st.session_state.editing_completed = todo['completed']
                    st.rerun()

            with col3:
                # Delete button
                if st.button("Delete", key=f"delete_{todo['id']}", help="Click to delete this todo"):
                    if st.checkbox(f"Confirm delete {todo['id']}"):
                        if delete_todo(todo['id']):
                            st.success(f"Deleted: {todo['title']}")
                            # Refresh todos after deletion
                            time.sleep(0.5)
                            todos.clear()
                            todos.extend(fetch_todos())
                        else:
                            st.error("Failed to delete todo")

            # Separator between todos
            st.markdown("---")
else:
    # Message when no todos exist
    st.info("📭 No todos yet! Add your first todo in the sidebar.")

# Modal for editing todos
if 'editing_id' in st.session_state:
    st.markdown("---")
    st.subheader("✏️ Edit Todo")

    # Input fields for editing
    edited_title = st.text_input("Title:", value=st.session_state.editing_title)
    edited_description = st.text_area("Description:", value=st.session_state.editing_description, height=80)
    edited_completed = st.checkbox("Completed", value=st.session_state.editing_completed)

    # Submit button for edit
    if st.button("💾 Update Todo"):
        # Prepare the updated data
        updated_data = {
            "title": edited_title,
            "description": edited_description,
            "completed": edited_completed
        }

        # Send update request
        if update_todo(st.session_state.editing_id, updated_data):
            st.success("✅ Todo updated successfully!")
            # Clear session state
            st.session_state.editing_id = None
            st.rerun()
        else:
            st.error("❌ Failed to update todo")

    # Cancel button
    if st.button("❌ Cancel"):
        st.session_state.editing_id = None
        st.rerun()

# Sidebar for statistics
with st.sidebar:
    st.markdown("### 📊 Statistics")
    if todos:
        total_todos = len(todos)
        completed_todos = len([t for t in todos if t['completed']])
        active_todos = total_todos - completed_todos

        st.write(f"**Total:** {total_todos}")
        st.write(f"**Active:** {active_todos}")
        st.write(f"**Completed:** {completed_todos}")

        # Progress bar
        progress = completed_todos / total_todos
        st.progress(progress)
    else:
        st.write("**No todos yet**")

# Footer with API status
with st.expander("🔗 API Status"):
    try:
        response = requests.get("http://localhost:8000/health")
        if response.status_code == 200:
            st.success("✅ API is running")
            st.json(response.json())
        else:
            st.error("❌ API not responding")
    except requests.exceptions.RequestException:
        st.error("❌ Cannot connect to API")
        st.info("Make sure FastAPI server is running on http://localhost:8000")

# Instructions
st.markdown("---")
st.markdown("💡 **How to use:**")
st.markdown("1. Add new todos in the sidebar")
st.markdown("2. Edit existing todos with the edit button")
st.markdown("3. Delete todos with the delete button")
st.markdown("4. Filter todos by status")
st.markdown("5. API runs on http://localhost:8000")
