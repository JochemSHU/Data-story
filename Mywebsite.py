#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 15 12:49:36 2023

@author: School
"""

import pandas as pd
import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap


#Figuur 1
# Titel
st.title("De rol van de voedselindustrie in overgewicht")

# Inleiding
st.write(" Uit cijfers blijkt dat er een stijgende trend is in zowel matig overwicht als ernstig overgewicht. De vraag is naar wie kan de vinger worden gewezen in dit verhaal. Zijn het de individuen die niet strikt genoeg zijn met hun eetpatroon of is het de schuld van de voedselindustrie?")

# Alle datasets
df1 = pd.read_csv("table__81565NED.csv")

st.markdown("<h1 style='font-size: 16px;'>Overgewicht Nederlandse bevolking, vanaf 1981</h2>", unsafe_allow_html=True)

# Kolommen voor de checkboxen
col1, col2, col3 = st.columns(3)
totaal_overgewicht = col1.checkbox("Totaal overgewicht", value=True)
matig_overgewicht = col2.checkbox("Matig overgewicht", value=True)
ernstig_overgewicht = col3.checkbox("Ernstig overgewicht", value=True)

# Hernoem de kolommen
D1 = df1.rename(columns={
    'Onder- en overgewicht, 4 jaar of ouder Overgewicht (%)': 'Totaal overgewicht',
    'Onder- en overgewicht, 4 jaar of ouder Mate van overgewicht\nMatig overgewicht (%)': 'Matig',
    'Mate van overgewicht Ernstig overgewicht (%)': 'Ernstig'
})

# Lijndiagram maken op basis van de checkboxen
selected_columns = []
if totaal_overgewicht:
    selected_columns.append('Totaal overgewicht')
if matig_overgewicht:
    selected_columns.append('Matig')
if ernstig_overgewicht:
    selected_columns.append('Ernstig')

# Pas de Y-as waarden aan
for column in selected_columns:
    D1[column] = D1[column].str.replace(',', '.').astype(float) / 1

fig1 = px.line(
    D1, x='Perioden', y=selected_columns,
    labels={'value': '% met overgewicht', 'variable': 'Soort overgewicht'},
    markers=True  # Voeg markers toe aan de lijnen
)

st.plotly_chart(fig1)

st.markdown("<h7 style='font-size: 15px; text-align: right;'>Bron: CBS (2023)</h1>", unsafe_allow_html=True)
    
#BRON https://opendata.cbs.nl/statline/#/CBS/nl/dataset/81565NED/line?ts=1697374154205&fromstatweb=true

st.write("In 2022 had 44,5% van de Nederlanders van 18 jaar en ouder matig of ernstig overgewicht. Matig of ernstig overgewicht wordt gedefinieerd als een Body Mass Index (BMI) van 25 kg/m² of hoger. Het is interessant om te weten dat overgewicht vaker voorkomt bij mannen dan bij vrouwen.")
st.write("Overgewicht is algemeen bekend als schadelijk voor de gezondheid.  Naast psychologische aandoeningen zoals depressie en angststoornissen, verhoogt obesitas het risico op aandoeningen zoals diabetes, een verhoogd cholesterolgehalte en hoge bloeddruk, wat het risico op hart- en vaatziekten, waaronder hartaanvallen en beroertes, vergroot. ")
st.subheader("Overgewicht verkort de levensverwachting minimaal 1 jaar en kan bij ernstige obesitas zelfs tot 10 jaar kosten.")
st.write("Ook is er een groter risico op bepaalde vormen van kanker. Bovendien veroorzaakt het extra gewicht druk op het lichaam, wat leidt tot gewrichtsklachten en slaapapneu, met ernstige vermoeidheid tot gevolg. Ernstig overgewicht kan ook leiden tot menstruatieproblemen, verminderde vruchtbaarheid en incontinentieproblemen")

#Figuur 2
st.subheader("Is overgewicht gekoppeld aan inkomen en opleidingsniveau?")
st.write("De relatie tussen overgewicht, inkomen en opleidingsniveau is een onderwerp dat herhaaldelijk in de schijnwerpers staat. Velen vragen zich af of er een duidelijk waarneembare trend is in hoe deze factoren met elkaar in verband staan.")


data = {
    'Inkomensklasse': ['Laagste', 'Midden', 'Hoogste'],
    'Man': [64.0, 65.9, 59.7],
    'Vrouw': [60.2, 55.0, 45.5]
}

# Maak een DataFrame van de data
df2 = pd.DataFrame(data)

# Herstructureer de data voor Plotly Express
df2 = pd.melt(df2, id_vars=['Inkomensklasse'], value_vars=['Man', 'Vrouw'],
              var_name='Geslacht', value_name='% met overgewicht')

# Maak drie kolommen om de checkboxen naast elkaar te plaatsen
col1, col2, col3 = st.columns(3)

# Checkboxen voor de inkomensklassen
with col1:
    laagste_inkomen = st.checkbox("Laagste Inkomensklasse", value=True)

with col2:
    midden_inkomen = st.checkbox("Midden Inkomensklasse", value=True)

with col3:
    hoogste_inkomen = st.checkbox("Hoogste Inkomensklasse", value=True)

# Filter de data op basis van de checkboxselectie
selected_inkomensklasse = []
if laagste_inkomen:
    selected_inkomensklasse.append('Laagste')

if midden_inkomen:
    selected_inkomensklasse.append('Midden')

if hoogste_inkomen:
    selected_inkomensklasse.append('Hoogste')

filtered_df2 = df2[df2['Inkomensklasse'].isin(selected_inkomensklasse)]

# Maak een figuur met Plotly Express
fig2 = px.bar(filtered_df2, x='Inkomensklasse', y='% met overgewicht', color='Geslacht',
             barmode='group',  # Hiermee worden de balken naast elkaar geplaatst
             title='Overgewicht naar geslacht en inkomen in Nederland 2020, 45 - 64 jaar')

# Toon het Plotly-figuur in Streamlit
st.plotly_chart(fig2)

st.markdown("<h7 style='font-size: 15px; text-align: right;'>Bron: RIVM (2022)</h1>", unsafe_allow_html=True)


#BRON https://www.vzinfo.nl/overgewicht/inkomen

st.write("Overgewicht komt minder vaak voor bij mensen in de hoogste inkomensklasse, zowel bij mannen als vrouwen. Naarmate het inkomen stijgt, neemt het percentage overgewicht af. Deze trend geldt voor zowel mannen als vrouwen, vanaf de midden-inkomensklasse tot de hoogste inkomensklasse. Opmerkelijk genoeg vertonen mannen in de laagste inkomensklasse een afwijkend patroon, waarbij ze minder vaak overgewicht hebben dan mannen in de inkomensklasse direct erboven.")


#st.subheader("Overgewicht per opleidingsniveau")

df4 = pd.read_excel("Trendovergewicht.xlsx")

# Creëer checkboxen voor opleidingsniveaus
col1, col2, col3 = st.columns(3)
laag_checkbox = col1.checkbox("Laag", value=True)
middel_checkbox = col2.checkbox("Middel", value=True)
hoog_checkbox = col3.checkbox("Hoog", value=True)

# Filter de gegevens op basis van de checkboxselectie
selected_columns = ['Datum']
if laag_checkbox:
    selected_columns.append('Laag')
if middel_checkbox:
    selected_columns.append('Middel')
if hoog_checkbox:
    selected_columns.append('Hoog')

# Zorg ervoor dat de dataset alleen de geselecteerde kolommen bevat
filtered_df = df4[selected_columns]

# Maak een lijndiagram met Plotly Express
fig = px.line(filtered_df, x='Datum', y=selected_columns[1:],
              labels={'value': '% met overgewicht', 'variable': 'Opleidingsniveau'})

# Pas de layout van de grafiek aan
fig.update_layout(
    title='Overgewicht over de jaren per opleidingsniveau in Nederland, 25 jaar en ouder',
    xaxis_title='Perioden',
    yaxis_title='% met overgewicht',
    showlegend=True  # Toon de legenda
)

# Toon het lijndiagram in Streamlit
st.plotly_chart(fig)

st.markdown("<h7 style='font-size: 15px; text-align: right;'>Bron: RIVM (2022)</h1>", unsafe_allow_html=True)


#Bron hhttps://www.vzinfo.nl/overgewicht/opleiding, de tabel met naam "trend in overgewicht naar opleiding 1999-2022"

st.write("Het deel van de bevolking met overgewicht is tussen 1999 en 2021 toegenomen in alle opleidingsgroepen. Opvallend is dat de stijging sterker was onder mensen met een middelbare opleiding dan onder degenen met een hogere opleiding. Zelfs wanneer we rekening houden met de relatieve opleidingspositie, wat rekening houdt met generatie- en geslachtsverschillen, blijkt dat het percentage overgewicht minder snel toeneemt naarmate mensen hoger opgeleid zijn.")
st.subheader("Correlatie overgewicht, inkomen en opleidingsniveau")
st.write("Samenvattend kan er gesteld worden dat er over het algemeen een verband bestaat tussen opleidingsniveau, inkomsten en overgewicht. Mensen met hogere opleidingsniveaus en inkomsten vertonen een lagere mate van overgewicht en obesitas. Deze relatie kan worden verklaard door verschillende factoren, zoals toegang tot gezondere voeding, gezondere levensstijlgewoonten en betere gezondheidszorg. Het is echter van cruciaal belang om te onthouden dat deze correlaties niet betekenen dat er een direct oorzakelijk bestaat, aangezien individuele omstandigheden en keuzes van invloed zijn op gewichtsbeheersing.")


#Stuk schijf van 5
st.subheader("Schijf van 5")

st.write(" ")

# Plaats de afbeelding in het midden
st.image("Sv5.jpeg", use_column_width="always")

st.markdown("<h7 style='font-size: 15px; text-align: center;'>Afbeelding: Getty Images</h1>", unsafe_allow_html=True)


st.write("De Schijf van Vijf, ontwikkeld door het Voedingscentrum, is een wetenschappelijk onderbouwd model voor voedingsvoorlichting dat de kern van gezonde voeding belicht. Dit model combineert zorgvuldig geselecteerde voedingsmiddelen om de gezondheid te bevorderen en tegelijkertijd te voorzien in voldoende energie en essentiële voedingsstoffen. De Schijf van Vijf bestaat uit vijf sectoren, elk met specifieke soorten voedsel. Het Voedingscentrum heeft de Schijf van Vijf samengesteld op basis van wetenschappelijke richtlijnen van de Gezondheidsraad, berekeningen van het Rijksinstituut voor Volksgezondheid en Milieu (RIVM) en advies van deskundigen op het gebied van voeding en gezondheid (Voedingscentrum, 2023.).")

st.subheader("Marketingbestedingen via massamedia voor voedings- en genotmiddelen")


data = {
    'Perioden': ['2017', '2018', '2019', '2020', '2021'],
    'Wel in Schijf van 5': [11, 13, 11, 12, 12],
    'Niet in Schijf van 5': [79, 75, 79, 75, 76],
    'Gemengd': [8, 9, 9, 11, 11],
    'Onbekend': [2, 2, 1, 2, 1]
}

# Maak een DataFrame van de gegevens
df = pd.DataFrame(data)

# Maak checkboxen voor elke categorie
col1, col2, col3, col4 = st.columns(4)
checkbox_wel = col1.checkbox("Wel in Schijf van 5", value=True)
checkbox_niet = col2.checkbox("Niet in Schijf van 5", value=True)
checkbox_gemengd = col3.checkbox("Gemengd", value=True)
checkbox_onbekend = col4.checkbox("Onbekend", value=True)

# Filter de DataFrame op basis van de checkboxselectie
selected_columns = ['Perioden']
if checkbox_wel:
    selected_columns.append('Wel in Schijf van 5')
if checkbox_niet:
    selected_columns.append('Niet in Schijf van 5')
if checkbox_gemengd:
    selected_columns.append('Gemengd')
if checkbox_onbekend:
    selected_columns.append('Onbekend')

filtered_df = df[selected_columns]

# Maak een gestapeld staafdiagram met Plotly Express
fig = px.bar(filtered_df, x='Perioden', y=filtered_df.columns[1:],
             title='Marketingbestedingen producten wel en niet in de Schijf van Vijf',
             labels={'value': '% marketingbesteding', 'variable': 'Categorie'},
             barmode='stack')

# Pas de y-as aan om percentages van 0 tot 100 weer te geven
fig.update_yaxes(range=[0, 100])

# Toon het Plotly-figuur in Streamlit
st.plotly_chart(fig)

st.markdown("<h7 style='font-size: 15px; text-align: right;'>Bron: Faun, Slimmens, Clark, en Van Tiel (2022)</h1>", unsafe_allow_html=True)


#Bron https://edepot.wur.nl/629202 Pagina 23

st.write("Een aanzienlijk deel van de marketinguitgaven door voedings- en drankfabrikanten is gericht op producten die niet voldoen aan de criteria van de Schijf van Vijf. In de afgelopen vijf jaar bedroeg het aandeel van (bruto) reclame-uitgaven voor producten die buiten de Schijf van Vijf vallen tussen de 75% en 79%. Tegelijkertijd werd ongeveer 11% tot 13% van de marketingbudgetten besteed aan de promotie van producten die wel in de Schijf van Vijf passen, zoals koffie, thee, groenten, fruit en spijsvetten. Ongeveer 10% van de bestedingen was gericht op combinaties van producten die deels wel en deels niet in de Schijf van Vijf passen, zoals zuivel- of broodproducten. Een klein deel van de marketinguitgaven (2%) kon niet worden beoordeeld aan de hand van de Schijf van Vijf, omdat ze betrekking hadden op producten die niet waren beoordeeld door het Voedingscentrum, zoals baby- en peutervoeding, of omdat de producten niet meer op de markt waren.")

st.write("Voedingsmarketing speelt een cruciale rol in de keuzes die consumenten maken als het gaat om voeding en drank. De manier waarop voedingsproducten gepromoot worden, heeft een aanzienlijke impact op onze eetgewoonten en uiteindelijk op onze gezondheid. Er is onderzocht welke producten het meest geadverteerd worden, welke categorieën het grootste aandeel in deze marketinguitgaven hebben en of deze advertenties in lijn zijn met gezonde voedingsrichtlijnen.")

st.markdown("<h1 style='font-size: 16px;'>Marketingbestedingen via massamedia voor voedings- en genotmiddelen met aandeel Schijf van Vijf per productcategorie</h2>", unsafe_allow_html=True)


# Lees het Excel-bestand in
dfH = pd.read_excel("Heatmap.xlsx")

# Stel de rij- en kolomindex in voor de heatmap
dfH.set_index(' ', inplace=True)

# Definieer de kleuren en bijbehorende posities voor het kleurverloop
colors = ["#93c7fa", "#2b66c2", "#eb4339"]
positions = [0, 0.5, 1]

# Maak een colormap met het aangepaste kleurverloop
cmap = LinearSegmentedColormap.from_list("custom", list(zip(positions, colors)), N=256)

# Genereer een heatmap met Seaborn zonder standaard annotaties en met aangepaste kleurcodes
plt.figure(figsize=(10, 6))
ax = sns.heatmap(dfH, annot=False, fmt='', cmap=cmap, cbar_kws={})

# Voeg "%" toe aan elk vakje met witte tekst
for i in range(len(dfH.index)):
    for j in range(len(dfH.columns)):
        value = dfH.iloc[i, j]
        ax.text(j + 0.5, i + 0.5, f"{value}%", ha='center', va='center', color='white')

# Toon de heatmap
st.pyplot(plt)

st.markdown("<h7 style='font-size: 15px; text-align: right;'>Bron: Faun, Slimmens, Clark, en Van Tiel (2022)</h1>", unsafe_allow_html=True)


st.write("In de uitgaven voor marketing van voedingsproducten blinken categorieën als non-alcoholische dranken (gemiddeld 149 miljoen euro), zuivel (gemiddeld 139 miljoen euro), chocolade en snoep (gemiddeld 128 miljoen euro), en zwakalcoholische dranken (gemiddeld 101 miljoen euro) uit. Intrigerend is dat drie van deze categorieën voornamelijk producten omvatten die niet passen binnen de Schijf van Vijf. Dit geldt voor non-alcoholische dranken (met uitzondering van mineraalwater), chocolade en snoep, en zwakalcoholische dranken. Zuivelproducten vallen deels binnen de Schijf van Vijf, afhankelijk van het type zuivel.")

st.write("Tegelijkertijd vertonen productcategorieën als koffie en thee, spijsvetten, aardappelen, groenten en fruit een sterke focus op producten die wel binnen de Schijf van Vijf passen. Echter, ongeveer 35% van de advertenties in deze categorieën bevordert nog steeds producten met te veel zout of suiker. Dit geldt ook voor de categorie vlees, vis, wild en gevogelte, waar reclame vaak gericht is op bewerkte varianten met overmatige hoeveelheden vet of zout.")

#Figuur 4
#st.subheader("Marketing besteding voedings- en genotmiddelen")
#st.write("")

st.set_option('deprecation.showPyplotGlobalUse', False)

# Gegevens in de dataset
data = {
    'Categorie': ['Categorie 1'],
    'Non-alcoholische dranken': [149],
    'Zuivel': [139],
    'Chocolade, Snoepgoed': [128],
    'Zwak alcoholische dranken': [101],
    'Koffie, Thee': [79],
    'Voedingsmiddelen overig': [76],
    'Suiker, Kruiden, Specerijen': [63],
    'Snacks': [47],
    'Broodproducten, Banket': [45],
    'Aardappelen, groenten, fruit': [26],
    'Sterk alcoholische dranken': [23],
    'Spijsvetten': [23],
    'Maaltijden': [22],
    'Vlees, Vis, Wild en Gevogelte': [17],
    'Ontbijtproducten': [11],
    'Bakproducten': [8],
    'Baby-, Kindervoeding': [8],
    'Soep, -producten': [7],
    'Deegwaren': [8],
}

# Maak een DataFrame van de gegevens
df = pd.DataFrame(data)

# Verwijder de kolom 'Categorie' omdat deze niet nodig is
df = df.drop(columns=['Categorie'])

# Hervorm de gegevens om ze klaar te maken voor het staafdiagram
df = df.T.reset_index()
df = df.rename(columns={'index': 'Categorie', 0: 'Uitgaven (in miljoen €)'})

# Maak een staafdiagram met Plotly Express
fig = px.bar(df, x='Categorie', y='Uitgaven (in miljoen €)', title='Marketingbestedingen via massamedia voor voedings- en genotmiddelen (in miljoen €)',
             color='Categorie', text='Uitgaven (in miljoen €)')

# De volgende regel code verbergt de tekst "Categorie"
fig.update_xaxes(title_text='')

# Toon het staafdiagram in Streamlit
st.plotly_chart(fig, use_container_width=True)

st.markdown("<h7 style='font-size: 15px; text-align: right;'>Bron: Faun, Slimmens, Clark, en Van Tiel (2022)</h1>", unsafe_allow_html=True)

st.write("De grafiek toont gedetailleerde gegevens over marketinguitgaven voor verschillende voedingscategorieën. Zo zijn non-alcoholische dranken met 149 miljoen euro de hoogst bestede categorie, gevolgd door zuivel met 139 miljoen euro en chocolade en snoepgoed met 128 miljoen euro. Deegwaren vallen met 8 miljoen euro op de laatste plaats.")

st.subheader("Gevolgen stijgende trend overgewicht")
st.write("Overgewicht heeft aanzienlijke gevolgen voor de samenleving en individuen, zowel op fysiek als psychisch gebied. Het leidt tot een verhoogd risico op diverse gezondheidsproblemen, waaronder hart- en vaatziekten, diabetes en gewrichtsaandoeningen, waardoor de kwaliteit van leven aanzienlijk kan verslechteren. Daarnaast brengt overgewicht aanzienlijke financiële lasten met zich mee, zowel op individueel als maatschappelijk niveau. De hoge zorgkosten om gezondheidsproblemen als gevolg van overgewicht te behandelen, zetten de zorgsector onder druk en hebben indirecte maatschappelijke kosten, zoals ziekteverzuim en arbeidsongeschiktheid tot gevolg. Het aanpakken van overgewicht is niet alleen van belang voor individuele gezondheid, maar ook voor de duurzaamheid van onze gezondheidszorg en economie als geheel.")

st.subheader("Conclusie")
st.write("Uit de cijfers blijkt een zorgwekkende stijgende trend in zowel matig overgewicht als ernstig overgewicht in Nederland. Hierbij ontstaat de vraag naar de verantwoordelijkheid voor deze trend. Zijn individuen verantwoordelijk voor hun eetpatroon, of moet een deel van de schuld worden toegeschreven aan de voedselindustrie?")
st.write("In 2022 had bijna de helft (44,5%) van de Nederlandse volwassenen matig of ernstig overgewicht,  mannen vaker dan vrouwen. Overgewicht heeft aantoonbare negatieve gevolgen voor de gezondheid, waaronder psychologische aandoeningen en een verhoogd risico op aandoeningen zoals diabetes, hoog cholesterol en hoge bloeddruk. Dit verhoogt het risico op ernstige aandoeningen zoals hart- en vaatziekten en kanker. Het verkort ook de levensverwachting en leidt tot lichamelijke problemen zoals gewrichtsklachten en slaapapneu.")
st.write("Onderzoek toont aan dat er een verband is tussen overgewicht, inkomen en opleidingsniveau. Mensen met hogere inkomens en opleidingsniveaus hebben over het algemeen minder kans op overgewicht. Deze relatie is complex en wordt beïnvloed door factoren zoals toegang tot gezonder voedsel en gezondheidsgewoonten.")
st.write("De Schijf van Vijf is een model voor gezonde voeding en onderzoek wijst erop dat veel marketingbudgetten worden besteed aan producten die niet voldoen aan deze criteria. Dit roept vragen op over de rol van de voedselindustrie bij het bevorderen van ongezonde voeding.")
st.write("Kortom, de stijgende trend in overgewicht in Nederland is een complex probleem met verschillende oorzaken en gevolgen, en er is geen eenvoudige schuldige aan te wijzen. Het vereist een benadering op individueel, maatschappelijk en industrieel niveau.")