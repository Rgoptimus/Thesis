import streamlit as st

def main():
    st.title("Formulir Data Pengguna")

    # Pertanyaan Usia
    usia = st.slider("Berapa usia Anda?", min_value=0, max_value=100, value=25)

    # Pertanyaan Jenis Kelamin
    jenis_kelamin_options = ["Laki-laki", "Perempuan"]
    jenis_kelamin = st.selectbox("Jenis kelamin Anda apa?", jenis_kelamin_options)

    # Menampilkan hasil
    st.write(f"Usia: {usia} tahun")
    st.write(f"Jenis Kelamin: {jenis_kelamin}")

if __name__ == "__main__":
    main()
