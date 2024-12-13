import streamlit as st
import os
import pandas as pd
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

soil_translation = {
    'Alluvial': 'Alüvyon',
    'Black': 'Kara',
    'Clay': 'Kil',
    'Laterite': 'Laterit',
    'Red': 'Kırmızı',
    'Sandy': 'Kumlu'
}

product_translation = {
    "bugday": "Buğday",
    "arpa": "Arpa",
    "misir": "Mısır",
    "pirinc": "Pirinç",
    "tutun": "Tütün",
    "pamuk": "Pamuk",
    "cay": "Çay",
    "aycicegi": "Ayçiçeği",
    "soya": "Soya",
    "yer_fistigi": "Yer Fıstığı",
    "nohut": "Nohut",
    "bezelye": "Bezelye",
    "portakal": "Portakal",
    "limon": "Limon",
    "greyfurt": "Greyfurt"
}

co2_emissions = {
    "bugday": 0.20,
    "arpa": 0.18,
    "misir": 0.15,
    "pirinc": 0.30,
    "tutun": 0.25,
    "pamuk": 0.27,
    "cay": 0.22,
    "aycicegi": 0.17,
    "soya": 0.24,
    "yer_fistigi": 0.21,
    "nohut": 0.12,
    "bezelye": 0.14,
    "portakal": 0.10,
    "limon": 0.11,
    "greyfurt": 0.13
}

def sort_by_co2(recommended_crops):
    sorted_data = []

    for crop in recommended_crops:
        co2_value = co2_emissions.get(crop, None)
        if co2_value is not None:
            sorted_data.append((crop, co2_value))
    
    df = pd.DataFrame(sorted_data, columns=['Ürün', 'Karbon Emisyonu'])
    df = df.sort_values('Karbon Emisyonu', ascending=True).reset_index(drop=True)  
    
    return df

def reccomend_crop():
    st.title("Tarım Ürün Önerisi")

    uploaded_file = st.file_uploader("Toprak Görselini Yükleyin", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption='Yüklenen Görsel', use_column_width=True)

        image_path = os.path.join("uploads", uploaded_file.name)
        image.save(image_path)
        st.success(f"Dosya '{uploaded_file.name}' başarıyla yüklendi!")

        use_manual_input = st.checkbox("Sıcaklık ve Yağış Bilgilerini Manuel Gir")

        if use_manual_input:
            temp = st.number_input("Sıcaklık (°C)", value=25)
            rainfall = st.number_input("Yıllık Yağış (mm)", value=1000)
        else:
            latitude, longitude = get_location_from_ip()

            if latitude and longitude:
                temp, rainfall = get_annual_weather_data(latitude, longitude, 2023)
                if temp is not None and rainfall is not None:
                    st.info(f"Otomatik Alınan Maksimum Sıcaklık: {temp}°C, Yıllık Yağış: {rainfall} mm")
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
                    st.subheader(f"Toprak Türü: {soil_translation.get(soil_type, soil_type)}")

                    recommended_crops = lookup_table(temp, rainfall, soil_type.lower())
                    sorted_crops_df = sort_by_co2(recommended_crops)

                    st.subheader("Önerilen Ürünler:")

                    sorted_crops_df['Ürün'] = sorted_crops_df['Ürün'].map(product_translation)

                    st.markdown("""
                        <style>
                        .dataframe-container {
                            display: flex;
                            justify-content: center;
                            align-items: center;
                            margin-top: 20px;
                        }
                        .dataframe-style {
                            width: 80%;
                            text-align: center;
                        }
                        </style>
                    """, unsafe_allow_html=True)
                    
                    st.markdown('<div class="dataframe-container">', unsafe_allow_html=True)
                    st.table(sorted_crops_df)
                    st.markdown('</div>', unsafe_allow_html=True)

                except Exception as e:
                    st.error(f"Bir hata oluştu: {str(e)}")

if __name__ == "__main__":
    reccomend_crop()
