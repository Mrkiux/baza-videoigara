import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection


st.set_page_config(
    page_title="Baza videoigara",
    page_icon="🎮",
    layout="wide"
)

st.title("🎮 Baza videoigara")
st.write("Seminarski rad - Streamlit aplikacija")


conn = st.connection(
    "gsheets",
    type=GSheetsConnection
)

spreadsheet_url = st.secrets["connections"]["gsheets"]["spreadsheet"]


def ucitaj_podatke():
    df = conn.read(
        spreadsheet=spreadsheet_url,
        worksheet="Sheet1",
        ttl=0
    )

    if not df.empty:
        df["ID"] = pd.to_numeric(df["ID"], errors="coerce")
        df["Godina"] = pd.to_numeric(df["Godina"], errors="coerce")
        df["Ocjena"] = pd.to_numeric(df["Ocjena"], errors="coerce")
        df["Cijena"] = pd.to_numeric(df["Cijena"], errors="coerce")

    return df

def spremi_podatke(df):
    conn.update(
        spreadsheet=spreadsheet_url,
        worksheet="Sheet1",
        data=df
    )


df = ucitaj_podatke()



st.header("📊 Baza podataka")

st.dataframe(
    df,
    use_container_width=True,
    hide_index=True
)

st.divider()



st.header("➕ Dodaj novu igru")

with st.form("dodavanje_igre"):

    col1, col2 = st.columns(2)

    with col1:
        naziv = st.text_input(
            "Naziv igre",
            placeholder="npr. Cyberpunk 2077"
        )

        zanr = st.selectbox(
            "Žanr",
            [
                "Akcija",
                "Avantura",
                "RPG",
                "Sport",
                "Simulacija",
                "Sandbox",
                "Strategija",
                "Horor",
                "Trkaća igra"
            ]
        )

        platforma = st.selectbox(
            "Platforma",
            [
                "PC",
                "PlayStation",
                "Xbox",
                "Nintendo Switch"
            ]
        )

    with col2:
        godina = st.number_input(
            "Godina izlaska",
            min_value=1970,
            max_value=2030,
            value=2026,
            step=1
        )

        ocjena = st.number_input(
            "Ocjena",
            min_value=0.0,
            max_value=10.0,
            value=8.0,
            step=0.1
        )

        cijena = st.number_input(
            "Cijena (€)",
            min_value=0.0,
            max_value=1000.0,
            value=59.99,
            step=0.01
        )

    dodaj = st.form_submit_button(
        "➕ Dodaj igru"
    )

    if dodaj:

        if naziv.strip() == "":
            st.error("❌ Morate upisati naziv igre.")

        else:

            if df.empty:
                novi_id = 1
            else:
                novi_id = int(df["ID"].max()) + 1

            novi_red = pd.DataFrame(
                [{
                    "ID": novi_id,
                    "Naziv igre": naziv,
                    "Žanr": zanr,
                    "Platforma": platforma,
                    "Godina": int(godina),
                    "Ocjena": float(ocjena),
                    "Cijena": float(cijena)
                }]
            )

            novi_df = pd.concat(
                [df, novi_red],
                ignore_index=True
            )

            spremi_podatke(novi_df)

            st.success(
                f"✅ Igra '{naziv}' je uspješno dodana!"
            )

            st.rerun()


st.divider()



st.header("🔎 Pretraživanje i filtriranje")

col1, col2, col3 = st.columns(3)

with col1:

    pretraga = st.text_input(
        "🔎 Pretraži po nazivu",
        placeholder="Upiši naziv igre..."
    )

with col2:

    dostupni_zanrovi = sorted(
        df["Žanr"].dropna().unique().tolist()
    )

    odabrani_zanrovi = st.multiselect(
        "🎭 Filtriraj po žanru",
        dostupni_zanrovi
    )

with col3:

    dostupne_platforme = sorted(
        df["Platforma"].dropna().unique().tolist()
    )

    odabrane_platforme = st.multiselect(
        "🖥️ Filtriraj po platformi",
        dostupne_platforme
    )


filtrirani_df = df.copy()

if pretraga:
    filtrirani_df = filtrirani_df[
        filtrirani_df["Naziv igre"]
        .astype(str)
        .str.contains(
            pretraga,
            case=False,
            na=False
        )
    ]

if odabrani_zanrovi:
    filtrirani_df = filtrirani_df[
        filtrirani_df["Žanr"].isin(odabrani_zanrovi)
    ]

if odabrane_platforme:
    filtrirani_df = filtrirani_df[
        filtrirani_df["Platforma"].isin(odabrane_platforme)
    ]


st.subheader(
    f"Rezultati pretraživanja: {len(filtrirani_df)}"
)

st.dataframe(
    filtrirani_df,
    use_container_width=True,
    hide_index=True
)


st.divider()



st.header("↕️ Sortiranje podataka")

col1, col2 = st.columns(2)

with col1:

    stupac_za_sortiranje = st.selectbox(
        "Sortiraj prema",
        [
            "ID",
            "Naziv igre",
            "Godina",
            "Ocjena",
            "Cijena"
        ]
    )

with col2:

    smjer = st.selectbox(
        "Smjer sortiranja",
        [
            "Uzlazno ↑",
            "Silazno ↓"
        ]
    )


sortirano = df.sort_values(
    by=stupac_za_sortiranje,
    ascending=(smjer == "Uzlazno ↑")
)

st.dataframe(
    sortirano,
    use_container_width=True,
    hide_index=True
)


st.divider()



st.header("🏆 Najbolje i najlošije vrijednosti")

if not df.empty:

    najbolja = df.loc[df["Ocjena"].idxmax()]
    najlosija = df.loc[df["Ocjena"].idxmin()]

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("🏆 Najbolje ocijenjena igra")

        st.metric(
            "Naziv",
            najbolja["Naziv igre"]
        )

        st.write(
            f"⭐ Ocjena: **{najbolja['Ocjena']:.1f}/10**"
        )

        st.write(
            f"💰 Cijena: **{najbolja['Cijena']:.2f} €**"
        )

    with col2:

        st.subheader("💀 Najlošije ocijenjena igra")

        st.metric(
            "Naziv",
            najlosija["Naziv igre"]
        )

        st.write(
            f"⭐ Ocjena: **{najlosija['Ocjena']:.1f}/10**"
        )

        st.write(
            f"💰 Cijena: **{najlosija['Cijena']:.2f} €**"
        )


st.divider()



st.header("🗑️ Brisanje igre")

if not df.empty:

    opcije_za_brisanje = {
        f"{row['ID']} - {row['Naziv igre']}": row["ID"]
        for _, row in df.iterrows()
    }

    odabrana_igra = st.selectbox(
        "Odaberi igru koju želiš obrisati",
        list(opcije_za_brisanje.keys())
    )

    if st.button(
        "🗑️ Obriši odabranu igru",
        type="primary"
    ):

        odabrani_id = opcije_za_brisanje[
            odabrana_igra
        ]

        novi_df = df[
            df["ID"] != odabrani_id
        ].copy()

        spremi_podatke(novi_df)

        st.success(
            f"✅ Igra '{odabrana_igra}' je obrisana."
        )

        st.rerun()



st.divider()

st.caption(
    "Seminarski rad • Streamlit + Google Sheets"
)