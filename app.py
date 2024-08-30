import streamlit as st
import os
from PIL import Image
from classify_soil import classify_image
from lookup_table import lookup_table
from co2_sort import sort_by_co2
from weather import get_annual_weather_data
from location import get_location_from_ip

st.set_page_config(
    page_title="AgriGuide", 
    page_icon="🌾",
)


def reccomend_crop():
    st.title("Tarım Ürün Önerisi")

    uploaded_file = st.file_uploader("Toprak Görselini Yükleyin", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption='Yüklenen Görsel', use_column_width=True)

        image_path = os.path.join("uploads", uploaded_file.name)
        image.save(image_path)

        use_manual_input = st.checkbox("Sıcaklık ve Yağış Bilgilerini Manuel Gir")

        if use_manual_input:
            temp = st.number_input("Sıcaklık (°C)", value=25)
            rainfall = st.number_input("Yıllık Yağış (mm)", value=1000)
        else:
            latitude, longitude = get_location_from_ip()

            if latitude and longitude:
                temp, rainfall = get_annual_weather_data(latitude, longitude, 2023)
                if temp is not None and rainfall is not None:
                    st.write(f"Otomatik Alınan Maksimum Sıcaklık: {temp}°C, Yıllık Yağış: {rainfall} mm")
                else:
                    st.error("Hava durumu verileri alınamadı. Lütfen manuel olarak girin.")
                    return
            else:
                st.error("Enlem ve boylam alınamadı. Lütfen manuel olarak girin.")
                return

        if st.button("Ürün Öner"):
            with st.spinner('Toprak türü sınıflandırılıyor, lütfen bekleyin...'):
                try:
                    soil_type = classify_image(image_path)
                    st.write(f"Toprak Türü: {soil_type}")

                    recommended_crops = lookup_table(temp, rainfall, soil_type.lower())

                    sorted_crops = sort_by_co2(recommended_crops)

                    st.write("Önerilen Ürünler:")
                    st.table(sorted_crops)

                except Exception as e:
                    st.error(f"Bir hata oluştu: {str(e)}")

if __name__ == "__main__":
    reccomend_crop()
