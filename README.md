# DamagedLoggingAnalyzer

<img src="logo/logo.jpeg" width="200">

A project about of analyzing a statistic of damaged logging wood in Germany using Python.

This is my individual project for the module **Research Software Engineering** in SS24.
The task was to analyze a dataset from [genesis.destatis](https://www-genesis.destatis.de/genesis/online?operation=abruftabelleBearbeiten&levelindex=1&levelid=1713202276894&auswahloperation=abruftabelleAuspraegungAuswaehlen&auswahlverzeichnis=ordnungsstruktur&auswahlziel=werteabruf&code=41261-0003&auswahltext=&werteabruf=starten)
using Python and to find interesting aspects and potential questions that could be explored using this data.

If you are only interested in the results, please jump to the section [Damaged Logging](#damaged-logging).

# Installation

```bash
git clone git@github.com:HokageM/DamagedLoggingAnalyzer.git
cd DamagedLoggingAnalyzer
pip install .
```

# Usage

## Commandline

```bash
usage: damaged_logg_analyzer [-h] [--version] [--calculate-most-dangerous-reasons] [--plot-reason-dependencies] [--plot-owner-dependencies] [--plot-temporal-dependencies-all] [--predict]
                             [--out-dir OUT_DIR]
                             CSV

Analyzes the data about damaged wood from the CSV file.

positional arguments:
  CSV                   Path to the CSV containing the statistic.

options:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  --calculate-most-dangerous-reasons
                        Calculates the most dangerous reasons for each specie.
  --plot-reason-dependencies
                        Create combined plots for each specie and owner combinations for all reasons. Plots will be saved in: output-path/Specie/all_reasons/Owner/plot.png.
  --plot-owner-dependencies
                        Create combined plots for each specie and reason combinations for all owners. Plots will be saved in: output-path/Specie/Reason/all_owners/plot.png.
  --plot-temporal-dependencies-all
                        Create plots for temporal dependencies for each specie, reason and owner combination. Plots will be saved in: output-path/Specie/Reason/Owner/plot.png. Note: use --plot-
                        owner-dependencies and --plot-reason-dependencies.
  --predict             Estimates a death count function using Polynomial Regression with K-Fold Cross Validation to predict the numbers for the year 2024. Plots will be saved in: output-
                        path/Prediction_2024/Specie/Reasons/Owner/plot.png.Note: will created a new model for every specie, reason and owner combination.
  --out-dir OUT_DIR     Output directory for the plots.
```

## Library

The following classes are available:

```python
from damagedlogginganalyzer.DamagedLoggingAnalyzer import DamagedLoggingAnalyzer
from damagedlogginganalyzer.CSVAnalyzer import CSVAnalyzer
from damagedlogginganalyzer.Plotter import Plotter
from damagedlogginganalyzer.WoodOracle import WoodOracle
from damagedlogginganalyzer.Oracle import Oracle
```

The classes `CSVAnalyzer` and `Oracle` are independent of this project and can be used for other projects.
Moreover, the classes `DamagedLoggingAnalyzer`, `WoodOracle` and `Plotter` are specific for this project / data set.

# Damaged Logging

**Note:** You can optionally read the notebook [story_of_this_project.ipynb](https://github.com/HokageM/DamagedLoggingAnalyzer/tree/main/notebooks/story_of_this_project.ipynb) to have an interactive experience with the project.

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
How will the year 2024 look like in terms of the volume of wood harvested due to different causes?

**Damage Types**: 
Which type of damage causes the most wood harvesting? 
How do different types of forests compare in their vulnerability to specific damage types?

**Forest Management**: 
Are there noticeable differences in wood harvesting due to damage across different forest ownership types 
(e.g., state-owned vs. privately-owned forests)? This could reflect different management practices and their effectiveness.

### Potential Questions (will not be answered in this project):

**Impact of Extreme Weather**: 
Are there particular years with exceptionally high damage that could be correlated to extreme weather events or climate anomalies?

**Economic and Ecological Impact**: 
What might be the economic impact of these losses? 
How might these harvesting activities due to damages impact the ecological balance and biodiversity in these forests?

## Temporal Trends
**Question**:
How has the damage-caused wood harvesting changed over the years? 

I created individual plots for the total volume of wood harvested due to different reasons (drought, wind/storm, snow, insects, miscellaneous, total) and different owners over the years for different types of wood species.
Here are some examples (the other plots can be found in the [plots](https://github.com/HokageM/DamagedLoggingAnalyzer/tree/main/plots)/specie/reason/owner/plot.png directory or can be generated with the following command:

```bash
damaged_logg_analyzer data/DamagedLoggingWoodFixTable.csv --plot-temporal-dependencies-all --out-dir plots
```

Deaths of Oak and Red Oak caused by insects and owned by `Insgesamt` over the years in Germany:

<img src="plots/Eiche_und_Roteiche/Insekten/Insgesamt/plot.png" width="500">


Deaths of Pine caused by insects and owned by `Insgesamt` over the years in Germany:

<img src="plots/Kiefer_und_L�rche/Insekten/Insgesamt/plot.png" width="500">


Additionally, I created combined plots for the different types of wood species.
**Note:** In the following, I will only show the combined plots for the different types of wood species and owned by `Insgesamt`. The other plots can be found in the [plots](https://github.com/HokageM/DamagedLoggingAnalyzer/tree/main/plots)/specie/all_reasons/owner/plot.png directory or can be generated with the following command:

```bash
damaged_logg_analyzer data/DamagedLoggingWoodFixTable.csv --plot-reason-dependencies --out-dir plots
```

Total Oak and Red Oak deaths over the years in Germany:

<img src="plots/Eiche_und_Roteiche/all_reasons/Insgesamt/plot.png" width="500">

Total Beech and Hardwood deaths over the years in Germany:

<img src="plots/Buche_und_sonstiges_Laubholz/all_reasons/Insgesamt/plot.png" width="500">

Total Spruce deaths over the years in Germany:

<img src="plots/Fichte_und_Tanne_und_Douglasie_und_sonstiges_Nadelholz/all_reasons/Insgesamt/plot.png" width="500">

Total Pine deaths over the years in Germany:

<img src="plots/Kiefer_und_L�rche/all_reasons/Insgesamt/plot.png" width="500">

Total tree deaths over the years in Germany:

<img src="plots/Insgesamt/all_reasons/Insgesamt/plot.png" width="500">

All in all, one can see that the deaths of all species due to the most reasons depend on the year and fluctuate between high and low values.
However, the total deaths of all species are increasing over the years especially for the reasons `Sonstiges` (miscellaneous), which could be caused by fires, diseases, or other reasons.
The definition of `Sonstiges` is not clear in the dataset.

**Question**:
Are there increasing trends in certain types of damage like drought or insects, possibly linked to climate change?

All in all, the death of all species due to drought, snow, and insects can be modeled as linear (near constant) functions.
Please look in [Prediction_2024](https://github.com/HokageM/DamagedLoggingAnalyzer/tree/main/plots/Prediction_2024) for the function estimations.

The deaths of all species due to wind/storm depends on the year and fluctuate between high and low values.
But one can see a very high number of deaths due to wind/storm in the year 2006 and 2018.

The deaths of all species due to `Sonstiges` (miscellaneous) can be modeled quit good with a polynomial function and are increasing over the years.

The total deaths of all species are increasing over the years.

**Question**:
How will the year 2024 look like in terms of the volume of wood harvested due to different causes?

I used polynomial regression with k-fold cross validation to predict the volume of wood harvested due to different causes in the year 2024.
**Note:** The prediction is based on the data from 2006 to 2023. All plots can be found in the [Prediction_2024](https://github.com/HokageM/DamagedLoggingAnalyzer/tree/main/plots/Prediction_2024) directory or can be generated with the following command:

```bash
damaged_logg_analyzer data/DamagedLoggingWoodFixTable.csv --predict --out-dir path/to/output
```

The death of all species due to "Sonsitges" (miscellaneous) can be modeled quit good with a polynomial function, e.g. for the Beech and Hardwood species group:

<img src="plots/Prediction_2024/Buche_und_sonstiges_Laubholz/Sonstiges/Insgesamt/plot.png" width="500">

**In some cases prediction does not make sense**, because the death do not follow a polynomial function and depend on other factors, e.g. death causes by insects:

<img src="plots/Prediction_2024/Buche_und_sonstiges_Laubholz/Insekten/Insgesamt/plot.png" width="500">


Deaths due to nature like wind/storm, snow, and drought can be modeled as linear functions, e.g. for the Beech and Hardwood species group.
**Note**: One need to handle the outliers in the data, e.g. the death of the year 2018 for the Beech and Hardwood species group due to wind/storm, 
this can be done by using a Ridge Regression model.
Those outliers come from special events like storms, which are not predictable with the current model.

<img src="plots/Prediction_2024/Eiche_und_Roteiche/Wind__Sturm/Insgesamt/plot.png" width="500">

## Damage Types 
**Question**:
Which type of damage causes the most wood harvesting? 

This is solved by calculating the maximum damage for each type of wood species group, which can be done with the following command:

```bash
damaged_logg_analyzer data/DamagedLoggingWoodFixTable.csv --calculate-most-dangerous-reasons
```

The maximum damage for each type of wood species group is:

| Specie                                                 | Reason      | Amount |
|--------------------------------------------------------|-------------|--------|
| Eiche und Roteiche                                     | Wind/ Sturm | 2048   |
| Buche und sonstiges Laubholz                           | Wind/ Sturm | 9124   |
| Kiefer und L�rche                                      | Wind/ Sturm | 19806  |
| Fichte und Tanne und Douglasie und sonstiges Nadelholz | Sonstiges   | 208725 |
| Insgesamt                                              | Sonstiges   | 218181 |

**Question**:
How do different types of forests compare in their vulnerability to specific damage types?

This is also solved by the following command:

```bash
damaged_logg_analyzer data/DamagedLoggingWoodFixTable.csv --calculate-most-dangerous-reasons --plot-temporal-dependencies-all
```

Analyzing the plots show that `Buche und sonstiges Laubholz` and `Eiche und Roteiche` have fewer deaths in any reason 
compared to `Kiefer und L�rche` and `Fichte und Tanne und Douglasie und sonstiges Nadelholz`.
The death counts are up to 10 times higher for `Kiefer und L�rche` and `Fichte und Tanne und Douglasie und sonstiges Nadelholz`
compared to `Buche und sonstiges Laubholz` and `Eiche und Roteiche`.

## Forest Management
**Question**:
Are there noticeable differences in wood harvesting due to damage across different forest ownership types 
(e.g., state-owned vs. privately-owned forests)? This could reflect different management practices and their effectiveness.

This is solved by the following command:

```bash
damaged_logg_analyzer data/DamagedLoggingWoodFixTable.csv --plot-owner-dependencies
```

Analyzing the plots show that the deaths due to different reasons are similar for the different owners. So it seems that the owner does not have a big impact on the death count.
Here are some examples and the other plots can be found in the [plots](https://github.com/HokageM/DamagedLoggingAnalyzer/tree/main/plots)/specie/reason/all_owners/plot.png:

Deaths of Oak and Red Oak caused by insects and owned by `Insgesamt` over the years in Germany:

<img src="plots/Eiche_und_Roteiche/Insekten/all_owners/plot.png" width="500">

Deaths of Pine caused by insects and owned by `Insgesamt` over the years in Germany:

<img src="plots/Kiefer_und_L�rche/Insekten/all_owners/plot.png" width="500">

# Contact Information

If you have any questions, suggestions, or concerns about this project, feel free to contact me:

- **LinkedIn:** [Mike Trzaska](https://de.linkedin.com/in/mike-trzaska-b576a6201)
- **GitHub:** [HokageM](https://github.com/HokageM)

# Statistic about Damaged Logging

From: [genesis.destatis](https://www-genesis.destatis.de/genesis/online?operation=abruftabelleBearbeiten&levelindex=1&levelid=1713202276894&auswahloperation=abruftabelleAuspraegungAuswaehlen&auswahlverzeichnis=ordnungsstruktur&auswahlziel=werteabruf&code=41261-0003&auswahltext=&werteabruf=starten)

Statistic Number: 41261-0003

# Citation

If you use this software, please cite it as described in the [CITATION.cff](CITATION.cff) file.


# License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.