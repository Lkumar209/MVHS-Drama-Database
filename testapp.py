import streamlit as st
from PIL import Image
import os
import re

# Function to handle each rack's page
def handle_rack_page(rack_number):
    image_folder = f'rack{rack_number}'
    st.title(f"Rack {rack_number}")

    uploaded_file = st.file_uploader("Upload Image", type=['png', 'jpg', 'jpeg', 'gif', 'heic'], key=f'uploader{rack_number}')
    if uploaded_file is not None:
        if not os.path.exists(image_folder):
            os.makedirs(image_folder)
        with open(os.path.join(image_folder, uploaded_file.name), "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success(f"Image uploaded to Rack {rack_number} successfully!")

    if os.path.exists(image_folder):
        valid_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.heic']
        images = [f for f in os.listdir(image_folder) if os.path.splitext(f)[1].lower() in valid_extensions]

        # Sort images based on filename structure
        images.sort(key=lambda x: [int(part) if part.isdigit() else part for part in re.split('(\d+)', x)])

        cols_per_row = 3
        for i in range(0, len(images), cols_per_row):
            cols = st.columns(cols_per_row)
            for j in range(cols_per_row):
                if i + j < len(images):
                    image_file = images[i + j]
                    image_path = os.path.join(image_folder, image_file)
                    try:
                        image = Image.open(image_path)
                        with cols[j]:
                            st.image(image, caption=image_file, use_column_width=True)
                    except Exception as e:
                        st.error(f"Error loading image {image_file}: {e}")
    else:
        st.write(f"No images found in {image_folder}. Upload images to display them here.")

# Function to display search results
        

def display_search_results(search_query):

    st.title(f"Search results for '{search_query}'")
    search_keywords = [keyword.strip().lower() for keyword in search_query.split(',')]

    all_images = []
    for rack_number in range(1, 9):
        image_folder = f'rack{rack_number}'
        if os.path.exists(image_folder):
            valid_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.heic']
            images = [f for f in os.listdir(image_folder) if os.path.splitext(f)[1].lower() in valid_extensions]
            
            # Filter images that contain all search keywords
            searched_images = [img for img in images if all(keyword in img.lower() for keyword in search_keywords)]
            all_images.extend([(rack_number, img) for img in searched_images])


    if all_images:
        # Sort images based on filename structure
        all_images.sort(key=lambda x: [int(part) if part.isdigit() else part for part in re.split('(\d+)', x[1])])

        cols_per_row = 3
        for i in range(0, len(all_images), cols_per_row):
            cols = st.columns(cols_per_row)
            for j in range(cols_per_row):
                if i + j < len(all_images):
                    rack_number, image_file = all_images[i + j]
                    image_path = os.path.join(f'rack{rack_number}', image_file)
                    try:
                        image = Image.open(image_path)
                        with cols[j]:
                            st.image(image, caption=image_file, use_column_width=True)
                    except Exception as e:
                        st.error(f"Error loading image {image_file}: {e}")
    else:
        st.write(f"No images found with '{search_query}' in the filename.")

# Function to display the homepage with rack logos
def display_homepage():
    st.title("Drama Inventory")

    search_query = st.text_input("Search Racks", "")
    if search_query:
        display_search_results(search_query)
        return  # Do not display the racks if a search query is entered

    logo_path = 'rack.png'
    if os.path.exists(logo_path):
        logo = Image.open(logo_path)
    else:
        logo = None

    for index in range(1, 9):
        with st.container():
            col1, col2 = st.columns([1, 3])
            with col1:
                if logo:
                    st.image(logo, width=75)
            with col2:
                st.write(f'Rack {index}')
                if st.button(f'Go to Rack {index}', key=f'rack{index}'):
                    st.session_state.current_page = index

# Check if a rack button is pressed and set the current page
def main():
    st.sidebar.title('Navigation')
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'home'

    if st.sidebar.button('Go to Homepage'):
        st.session_state.current_page = 'home'

    if st.session_state.current_page == 'home':
        display_homepage()
    else:
        handle_rack_page(st.session_state.current_page)

if __name__ == "__main__":
    main()
