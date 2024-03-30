import streamlit as st
import requests
from periodictable import elements

# Fungsi untuk mendapatkan deskripsi unsur dari WebElements API
def get_element_description(symbol):
    url = f"https://www.webelements.com/{symbol.lower()}/"
    response = requests.get(url)
    if response.status_code == 200:
        start_index = response.text.find('<div class="summary">') + len('<div class="summary">')
        end_index = response.text.find('</div>', start_index)
        description = response.text[start_index:end_index]
        return description.strip()
    else:
        return "Deskripsi tidak tersedia."

# Fungsi untuk mendapatkan kategori unsur berdasarkan posisi dalam tabel periodik
def get_category(element):
    if element.number <= 92:
        return 'Logam'
    else:
        return 'Non-logam'

# Fungsi untuk styling
def set_style():
    st.markdown(
        """
        <style>
        .post-container {
            background-color: #e0e0e0;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
        }
        .post-header {
            display: flex;
            align-items: center;
            margin-bottom: 10px;
        }
        .post-avatar {
            width: 40px;
            height: 40px;
            border-radius: 50%;
            margin-right: 10px;
        }
        .post-username {
            font-weight: bold;
            color: #333333;
            margin-right: 5px;
        }
        .post-timestamp {
            color: #666666;
            font-size: 12px;
        }
        .post-content {
            color: #333333;
            font-size: 16px;
            line-height: 1.5;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# Streamlit app
def main():
    set_style()
    st.title("TABEL PERIODIK")

    # Pilihan untuk melihat informasi unsur
    element_choice = st.selectbox("Pilih Unsur", [element.symbol for element in elements])

    # Cari unsur berdasarkan simbol yang dipilih
    selected_element = elements.symbol(element_choice)

    # Mendapatkan deskripsi unsur dari API
    description = get_element_description(selected_element.symbol)

    # Tampilkan informasi unsur jika dipilih
    with st.container():
        st.markdown(
            f"""
            <div class="post-container">
                <div class="post-header">
                    <img src="https://avatars.githubusercontent.com/u/45109972?s=200&v=4" class="post-avatar">
                    <div>
                        <span class="post-username">Streamlit</span>
                        <span class="post-timestamp">• 31 Maret</span>
                    </div>
                </div>
                <div class="post-content">
                    <p style="font-size: 20px; font-weight: bold;">{selected_element.name} ({selected_element.symbol})</p>
                    <p><strong>Nomor Atom:</strong> {selected_element.number}</p>
                    <p><strong>Massa Atom:</strong> {selected_element.mass}</p>
                    <p><strong>Kategori:</strong> {get_category(selected_element)}</p>
                    <p><strong>Deskripsi:</strong> {description}</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

if __name__ == "__main__":
    main()
