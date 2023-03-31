import streamlit as st

def main():
    st.title("Chat App")

    # Get user's name
    name = st.text_input("Name")

    # Create empty list to store messages
    messages = []

    # Get user's message
    message = st.text_input("Message")

    # Add message to list if user presses enter
    if st.button("Send"):
        messages.append({"name": name, "message": message})

    # Display all messages
    for msg in messages:
        st.write(f"{msg['name']}: {msg['message']}")

if __name__ == "__main__":
    main()
