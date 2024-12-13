## Kurulum

### 1. GitHub'dan Projeyi Klonlayın

```bash
git clone https://github.com/AgriGuide/AgriGuideApp.git
cd AgriGuideApp
```

### 2. Sanal Ortam Oluşturun ve Aktifleştirin

```bash
python -m venv venv
```

#### Windows için:
```bash
venv\Scripts\activate
```

#### Linux/Mac için:
```bash
source venv/bin/activate
```

### 3. Gereksinimleri Yükleyin
```bash
pip install -r requirements.txt
```

## Kullanım
```bash
streamlit run app.py
```