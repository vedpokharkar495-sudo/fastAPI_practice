
# Import Streamlit library for creating the web interface
import streamlit as st
import requests  # Import requests library to communicate with FastAPI backend
import json  # Import json library to handle JSON responses

# --------------------------------------------------------------------------------------------

# Set the page configuration for Streamlit
# This sets the title and layout of the web page
st.set_page_config(page_title="Calculator App", layout="centered")

# Add a title to the web page
st.title("Calculator App")

# Add a brief description of the calculator
st.write("Perform basic arithmetic operations using this calculator")

# ----------------------------------------------------------------------------------------

# Create two input fields for numbers
# Using st.number_input with proper labels and default values
number1 = st.number_input("Enter first number:") #
number2 = st.number_input("Enter second number:") # , value=0.0, type="float"

#--------------------------------------------------------------------------------------------

# Create a select box for operation selection
# Add options for different arithmetic operations
operation = st.selectbox(
    "Select operation:",
    options=["add", "subtract", "multiply", "divide"],
    index=0,  # Default to first option (add)
    help="Choose the arithmetic operation you want to perform"
)

# Create a button to trigger the calculation
# When clicked, it will send a request to the backend
if st.button("Calculate"):
    # Define the base URL for the API
    # This should match the FastAPI server URL
    api_url = "http://localhost:8000"

    # Create a payload dictionary with the calculation data
    # This will be sent as JSON to the backend
    payload = {
        "number1": number1,
        "number2": number2,
        "operation": operation
    }

    # Select the appropriate endpoint based on the operation
    # This maps the operation string to the correct API endpoint
    endpoints = {
        "add": f"{api_url}/add",
        "subtract": f"{api_url}/subtract",
        "multiply": f"{api_url}/multiply",
        "divide": f"{api_url}/divide"
    }

    # Get the correct endpoint URL based on selected operation
    endpoint = endpoints[operation]

    # Send a POST request to the FastAPI backend
    # The payload is sent as JSON data
    try:
        response = requests.post(endpoint, json=payload)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON response from the backend
            data = response.json()

            # Check if the response contains an error (like division by zero)
            if "error" in data:
                st.error(f"Error: {data['error']}")
            else:
                # Display the successful result
                st.success(f"Result: {data['result']}")

                # Add a visual representation of the calculation
                st.write("---")
                st.write(f"{number1} ➜ {operation.upper()} ➜ {number2} = {data['result']}")
        else:
            # Handle cases where the request failed
            st.error(f"Failed to connect to server. Status code: {response.status_code}")
            st.write("Make sure the FastAPI server is running on http://localhost:8000")

    except requests.exceptions.RequestException as e:
        # Handle connection errors (like server not running)
        st.error(f"Connection error: {str(e)}")
        st.write("Please ensure the FastAPI server is running and accessible.")

# Add a section for displaying API documentation
with st.expander("API Documentation"):
    st.write("**Available Endpoints:**")
    st.write("- POST /add - Perform addition")
    st.write("- POST /subtract - Perform subtraction")
    st.write("- POST /multiply - Perform multiplication")
    st.write("- POST /divide - Perform division")
    st.write("- GET /health - Health check endpoint")
    st.write("\n**Example Request:**")
    st.json({
        "number1": 10,
        "number2": 5,
        "operation": "add"
    })

# Add a footer with instructions
st.markdown("---")
st.markdown("💡 **Tip:** Make sure the FastAPI server is running before using this calculator.")
st.markdown("🔗 **API Server:** http://localhost:8000")
