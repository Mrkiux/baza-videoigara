# 🎮 Baza videoigara

Web aplikacija izrađena u sklopu seminarskog rada.

Aplikacija služi za pregled, pretraživanje, filtriranje, dodavanje i brisanje videoigara. Podaci se pohranjuju u Google Sheets koji služi kao baza podataka.

## 🛠️ Korištene tehnologije

- Python
- Streamlit
- Pandas
- Google Sheets
- Google Sheets Connection
- GitHub
- Streamlit Community Cloud

## 📊 Baza podataka

Google Sheets koristi se kao baza podataka aplikacije.

Svaki zapis sadrži sljedeće podatke:

- ID
- Naziv igre
- Žanr
- Platforma
- Godina izlaska
- Ocjena
- Cijena

## ⚙️ Funkcionalnosti

Aplikacija omogućuje:

- prikaz svih videoigara u tablici
- dodavanje novih videoigara
- pretraživanje prema nazivu
- filtriranje prema žanru
- filtriranje prema platformi
- brisanje odabranih videoigara
- sortiranje podataka
- prikaz najbolje ocijenjene igre
- prikaz najlošije ocijenjene igre

## 🌐 Pokretanje aplikacije

Aplikacija je objavljena putem Streamlit Community Clouda.

Poveznica na aplikaciju:

https://baza-videoigara-7rypkwd3l9dmvbjekhmgiv.streamlit.app

## 📁 Struktura projekta

```text
baza-videoigara/
│
├── app.py
├── requirements.txt
├── .gitignore
└── README.md
