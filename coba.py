import streamlit as st
import requests
import math
from periodictable import elements
import periodictable

def get_category(element):
    if element.number <= 92:
        return 'Logam'
    else:
        return 'Non-logam'

def hitung_normalitas(bobot_ditimbang, faktor_pengali, hasil_titrasi, BE_senyawa):
    normalitas = (bobot_ditimbang) / (faktor_pengali * hasil_titrasi * BE_senyawa)
    return normalitas

def hitung_rata_rata(normalitas_list):
    if len(normalitas_list) == 0:
        return None
    else:
        rata_rata = sum(normalitas_list) / len(normalitas_list)
        return rata_rata

def hitung_persen_rsd(SD, rata_rata):
    if rata_rata == 0:
        st.error("Rata-rata konsentrasi tidak boleh nol.")
        return None
    else:
        rsd = (SD / rata_rata) * 100
        return rsd

def page_about():
    st.title("🧪Tentang Aplikasi Kimia:male-scientist:")
    st.write("""
    Aplikasi kimia ini dapat :
    - Melihat informasi unsur dari tabel periodik.
    - Menghitung normalitas larutan.
    - Menghitung standar deviasi.
    - Menghitung persentase RSD.
    
             
    PENYUSUN APLIKASI:
    - Dhafa Aulia Rachman        (2360104)
    - Hamna Nurfitria            (2360133)
    - Marini Badlina             (2360167)
    - Salsabila Aulia Widodo     (2360255)
    - Shafira Yasmina Cahyanti   (2360260)
    
    
    Aplikasi ini dibangun menggunakan Streamlit dan Python.
    """)

def page_normalitas_dan_molaritas():
    st.title('KALKULATOR PERHITUNGAN NORMALITAS DAN MOLARITAS:male-technologist:')
    st.write('Gunakan kalkulator ini untuk menghitung normalitas dasn molaritas larutan.')
    st.write('''
            - Normalitas (N), atau dikenal sebagai konsentrasi normal, adalah ukuran konsentrasi zat terlarut dalam gram ekuivalen per volume larutan .
            Untuk larutan dengan 'x' gram zat terlarut, persamaan normalitasnya adalah:
            (𝑁=Massa zat terlarut/berat ekuivalen × volume titran)
            - molaritas (M) adalah jumlah mol zat per volume larutan, sedangkan normalitas adalah berat ekuivalen zat per liter larutan.
            (M= Massa zat terlarut/BM x Volume titran)''')
    st.write('Sekarang Anda tahu apa itu normalitas! Mari kita hitung normalitas 🤗')

    jumlah_titrasi = st.number_input('Masukkan jumlah titrasi', min_value=1, value=1)
    normalitas_list = []
    
    for i in range(jumlah_titrasi):
        st.write(f"Titrasi ke-{i+1}")
        bobot_ditimbang = st.number_input(f'Masukkan bobot yang ditimbang untuk Titrasi ke-{i+1} (mg)', min_value=0.0, key=f"bobot_{i}")
        faktor_pengali = st.number_input(f'Masukkan faktor pengali untuk Titrasi ke-{i+1}', min_value=0.0, key=f"faktor_{i}")
        hasil_titrasi = st.number_input(f'Masukkan hasil titrasi untuk Titrasi ke-{i+1} (ml)', min_value=0.00, key=f"hasil_{i}")
        BE_senyawa = st.number_input(f'Masukkan BE/BM senyawa untuk Titrasi ke-{i+1}', min_value=0.00, key=f"BE_{i}")

        if st.button(f'Hitung Titrasi ke-{i+1}'):
            if bobot_ditimbang == 0 or faktor_pengali == 0 or hasil_titrasi == 0 or BE_senyawa == 0:
                st.error("Input semua data.")
            else:
                normalitas = hitung_normalitas(bobot_ditimbang, faktor_pengali, hasil_titrasi, BE_senyawa)
                normalitas_list.append(normalitas)
                st.write(f'Normalitas untuk Titrasi ke-{i+1} = {normalitas:.4f} N')

    if len(normalitas_list) > 0:
        rata_rata_normalitas = hitung_rata_rata(normalitas_list)
        st.write(f'Hasil rata-rata normalitas dari semua titrasi = {rata_rata_normalitas:.4f} N')

def page_unsur():
    st.title("⚗️INFORMASI UNSUR:sparkles:")
    st.write('''
             Unsur kimia bisa berarti dua hal:
            - Kesatu, unsur sama artinya dengan atom misal mengatakan unsur oksigen sama dengan mengatakan atom oksigen.
            - Kedua,unsur berarti zat yaitu kumpulan sangat banyak atom hingga sampai 
            pada tingkat yang bisa kita rasakan, bisa dilihat, dicium, 
            dan berdampak pada tubuh makhluk hidup, benda padat, cair, dan gas. Unsur jika lebih dirinci
            termasuk sebagai zat murni bersama dengan senyawa. ''')

    sorted_elements = sorted(periodictable.elements, key=lambda x: x.number)
    logam = []
    non_logam = []
    for element in sorted_elements:
        if element.number <= 92:
            if element.symbol in ["Li", "Na", "K", "Rb", "Cs", "Fr", "Be", "Mg", "Ca", "Sr", "Ba", "Ra",
                                   "Sc", "Y", "La", "Ac", "Ti", "Zr", "Hf", "Rf", "V", "Nb", "Ta", "Db",
                                   "Cr", "Mo", "W", "Sg", "Mn", "Tc", "Re", "Bh", "Fe", "Ru", "Os", "Hs",
                                   "Co", "Rh", "Ir", "Mt", "Ni", "Pd", "Pt", "Ds", "Cu", "Ag", "Au", "Rg",
                                   "Zn", "Cd", "Hg", "Cn", "B", "Al", "Ga", "In", "Tl", "Nh", "C", "Si", "Ge",
                                   "Sn", "Pb", "Fl", "N", "P", "As", "Sb", "Bi", "Mc"]:
                logam.append(element)
            else:
                non_logam.append(element)

    element_choice = st.selectbox("", [element.symbol for element in sorted_elements], format_func=lambda x: x.upper())
    pilih_elemen = None
    for element in sorted_elements:
        if element.symbol == element_choice:
            pilih_elemen = element
            break

    if pilih_elemen:
        st.markdown(f"## {pilih_elemen.name} ({pilih_elemen.symbol})")
        st.write(f"Nomor Atom: {pilih_elemen.number}")
        st.write(f"Massa Atom: {pilih_elemen.mass}")
        if pilih_elemen in logam:
            st.write("Kategori: Logam")
        elif pilih_elemen in non_logam:
            st.write("Kategori: Non-logam")
        else:
            st.write("Kategori: Tidak Diketahui")
        st.write(f"Kepadatan: {pilih_elemen.density if hasattr(pilih_elemen, 'density') else 'Tidak Tersedia'}")
        st.write(f"Jumlah Isotop: {len(pilih_elemen.isotopes)}")
    else:
        st.write("Unsur tidak ditemukan.")

if __name__ == "__page_unsur__":
    page_unsur()


def page_rsd():
    st.title('Kalkulator Persentase RSD:male-technologist:')
    st.write('''
            %RSD (deviasi standar relatif) adalah pengukuran statistik yang menggambarkan 
            penyebaran data terhadap mean dan hasilnya dinyatakan dalam persentase.
            Fungsi %RSD populer di kalangan non-ahli statistik karena interpretasinya
            didasarkan pada hasil persen dan bukan nilai abstrak. Kegunaan utama %RSD adalah dalam kimia 
            analitik dan secara rutin digunakan untuk menilai variasi kumpulan data.''')
    SD = st.number_input('Masukkan jumlah SD', min_value=0.00)
    rata_rata = st.number_input('Masukkan rata rata konsentrasi (N)', min_value=0.01)

    if st.button('Hitung'):
        rsd = hitung_persen_rsd(SD, rata_rata)
        if rsd is not None:
            st.write(f'RSD = {rsd:.2f}%')

def page_standar_deviasi():
    st.title("KALKULATOR PERHITUNGAN STANDAR DEVIASI")
    st.write('''Untuk menggunakan kalkulator ini, pengguna hanya memasukkan kumpulan angka yang ingin mereka hitung deviasi standarnya, 
             dengan setiap angka dipisahkan oleh titik. Titik harus digunakan untuk memisahkan nilai, 
             atau kalkulator tidak akan berfungsi. Pembatas lain, termasuk spasi di antara angka, 
             akan menyebabkan kalkulator tidak berfungsi. Hanya titik yang dikenali untuk memisahkan nilai.''')
    st.write('mari kita hitung standar deviasi')
    data_input = []
    num_columns = st.number_input("Jumlah Kolom Input Data", min_value=3, max_value=10, value=3)

    for i in range(num_columns):
        input_data = st.text_input(f"Masukkan data kolom {i+1}")
        if input_data:
            data_input.append([float(x.strip()) for x in input_data.split(',') if x.strip()])

    merged_data = [item for sublist in data_input for item in sublist]

    if merged_data:
        hasil_standar_deviasi = page_standar_deviasi_calc(merged_data)
        st.write("Standar Deviasi:", hasil_standar_deviasi)
    else:
        st.error("Input semua data.")

def page_standar_deviasi_calc(data):
    try:
        rata_rata = sum(data) / len(data)
        selisih_kuadrat = sum((x - rata_rata) ** 2 for x in data)
        standar_deviasi = math.sqrt((selisih_kuadrat) / (len(data) - 1))
        return standar_deviasi
    except:
        return "Masukkan semua hasil konsentrasi"

def main():
    page = st.sidebar.radio("Pilih Halaman", ["Tentang Aplikasi", "Informasi Unsur", "Kalkulator Konsentrasi", "Kalkulator Standar Deviasi", "Kalkulator Persentase RSD"])

    if page == "Tentang Aplikasi":
        page_about()
    elif page == "Informasi Unsur":
        page_unsur()
    elif page == "Kalkulator Konsentrasi":
        page_normalitas_dan_molaritas()
    elif page == "Kalkulator Standar Deviasi":
        page_standar_deviasi()
    elif page == "Kalkulator Persentase RSD":
        page_rsd()

if __name__ == '__main__':
    main()
