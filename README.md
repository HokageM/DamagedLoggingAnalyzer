# DamagedLoggingAnalyzer

<img src="logo/logo.jpeg" width="200">

A project about of analyzing a statistic of damaged logging (wood) in Germany using Python.

This my individual project for the module **Research Software Engineering** in SS24.

# Damaged Logging

## What is the dataset about?

The dataset contains statistics on forest wood harvesting due to various damages in Germany,
listed by year, type of wood species groups, and ownership types of forests. 

Each entry specifies the volume of wood harvested (in cubic meters) due to different causes
such as wind/storm, snow/ice damage, insects, drought, and other reasons.

## Why is this dataset interesting?

Here are some interesting aspects and potential questions, which could explore using this data:

**Temporal Trends**: 
How has the damage-caused wood harvesting changed over the years? 
Are there increasing trends in certain types of damage like drought or insects, possibly linked to climate change?

**Damage Types**: 
Which type of damage causes the most wood harvesting? 
How do different regions or types of forests compare in their vulnerability to specific damage types?

**Forest Management**: 
Are there noticeable differences in wood harvesting due to damage across different forest ownership types 
(e.g., state-owned vs. privately-owned forests)? This could reflect different management practices and their effectiveness.

**Impact of Extreme Weather**: 
Are there particular years with exceptionally high damage that could be correlated to extreme weather events or climate anomalies?

**Preventive Measures**: 
Can we identify patterns or correlations that suggest effective preventive or mitigation strategies against certain types of damage?

**Economic and Ecological Impact**: 
What might be the economic impact of these losses? 
How might these harvesting activities due to damages impact the ecological balance and biodiversity in these forests?

## Temporal Trends

Total Oak and Red Oak deaths due to wind or storm over in Germany:

<img src="plots/Eiche_und_Roteiche/Wind__Sturm/Insgesamt/plot.png">

Total Oak and Red Oak deaths in Germany:

<img src="plots/Eiche_und_Roteiche/all_reasons/Insgesamt/plot.png">

Total Beech and Hardwood deaths due to wind or storm over in Germany:

<img src="plots/Buche_und_sonstiges_Laubholz/Wind__Sturm/Insgesamt/plot.png">

Total Beech and Hardwood deaths in Germany:

<img src="plots/Buche_und_sonstiges_Laubholz/all_reasons/Insgesamt/plot.png">

Total Spruce deaths due to wind or storm over in Germany:

<img src="plots/Fichte_und_Tanne_und_Douglasie_und_sonstiges_Nadelholz/Wind__Sturm/Insgesamt/plot.png">

Total Spruce deaths in Germany:

<img src="plots/Fichte_und_Tanne_und_Douglasie_und_sonstiges_Nadelholz/all_reasons/Insgesamt/plot.png">

Total Pine deaths due to wind or storm over in Germany:

<img src="plots/Kiefer_und_L�rche/Wind__Sturm/Insgesamt/plot.png">

Total Pine deaths in Germany:

<img src="plots/Kiefer_und_L�rche/all_reasons/Insgesamt/plot.png">

**Warning**: The dataset value for 'Insgesamt' seams incorrect.
Total tree deaths due to wind or storm over in Germany:

<img src="plots/Insgesamt/Wind__Sturm/Insgesamt/plot.png">

**Warning**: The dataset value for 'Insgesamt' seams incorrect.
Total tree deaths in Germany:

<img src="plots/Insgesamt/all_reasons/Insgesamt/plot.png">

# Usage

## Commandline

```bash
usage: damaged_logg_analyzer [-h] [--version] CSV

Just a Fibonacci demonstration

positional arguments:
  CSV         Path to the CSV containing the statistic.

options:
  -h, --help  show this help message and exit
  --version   show program's version number and exit

```

## Library

```python
from damagedlogginganalyzer.DamagedLoggingAnalyzer
```

# Statistic about Damaged Logging

From: [genesis.destatis](https://www-genesis.destatis.de/genesis/online?operation=abruftabelleBearbeiten&levelindex=1&levelid=1713202276894&auswahloperation=abruftabelleAuspraegungAuswaehlen&auswahlverzeichnis=ordnungsstruktur&auswahlziel=werteabruf&code=41261-0003&auswahltext=&werteabruf=starten)

Statistic Number: 41261-0003