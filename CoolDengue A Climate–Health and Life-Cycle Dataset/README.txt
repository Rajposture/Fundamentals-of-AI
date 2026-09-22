========================================================================
DATASET README
========================================================================
Title:   Eco-efficiency of Room Air Conditioner Units in a Dengue-Prone
         Climate: A Comprehensive Life Cycle Analysis Integrating
         Epidemiological Perspectives

Authors: Venkata K.K. Upadhyayula, Etienne Z. Gnimpieba, Shiva Aryal,
         Mats Tysklind, Debraj Bhattacharyya, Jose E. Pietri,
         Venkataramana Gadhamshetty

Journal: npj Sustainable and Built Environment (under review)

Code repository: https://github.com/bicbioeng/dengue-prediction-ml

========================================================================
DATASET OVERVIEW
========================================================================
This dataset supports a physics-informed machine learning (ML) framework
that estimates indoor dengue transmission risk (indoor basic reproduction
number, R_indoor) across eight dengue-endemic cities in tropical Asia,
and integrates those estimates into a life cycle assessment (LCA) based
eco-efficiency analysis of room air conditioner (RAC) units.

Eight study cities: Bangkok (Thailand), Cebu (Philippines),
Chennai (India), Colombo (Sri Lanka), Dhaka (Bangladesh),
Ho Chi Minh City (Vietnam), Jakarta (Indonesia), Yangon (Myanmar).

ML training cities: Dhaka (2024-2025, n=24 months),
Jakarta (2011-2015, n=60 months), Cebu (2019-2023, n=33 months,
COVID-affected years excluded).

========================================================================
FOLDER STRUCTURE
========================================================================

1_Epidemiological_Data/
  Monthly dengue case counts used for ML model training and context.

  Dengue_Cases_Eight_Cities.xlsx
      Compiled monthly dengue cases for Dhaka, Jakarta, Colombo,
      Cebu, and Chennai. Each city on a separate sheet.

  cases_Dhaka_2024_2025.csv
      Weekly/monthly dengue dashboard data for Dhaka, Bangladesh
      (2024-2025). Used as ML training data (n=24 months).

  cases_Jakarta_2011_2015.csv
      Daily weather-matched dengue case data for Jakarta, Indonesia
      (2011-2015). Used as ML training data (n=60 months).

  cases_Cebu_2019_2023.csv
      Monthly dengue case data for Cebu, Philippines (2019-2023,
      COVID-affected years excluded). Used as ML training data (n=33).

  cases_Chennai.csv
      Monthly dengue case data for Chennai, India. Used for
      simulation/prediction (not ML training).

  Dengue_Cases_TamilNadu_Source.pdf
      Source document: month-wise distribution of dengue cases in
      Tamil Nadu (includes Chennai), from official health records.


2_Weather_Data/
  Climate inputs used for physics simulations and ML feature engineering.

  Training_Cities_Historical/
    Daily and monthly weather data for the three ML training cities
    covering their respective dengue case periods.

    weather_Jakarta_2011_2015.csv    -- Daily (Meteostat), Jakarta
    Weather_Jakarta_2011_2015.xlsx   -- Same data in Excel format
    weather_Cebu_historical.csv      -- Daily weather near Cebu
    Weather_Near_Cebu_2011_2015.xlsx -- Same data in Excel format
    weather_Dhaka_2024.csv           -- Daily weather, Dhaka 2024
    weather_Dhaka_2025.csv           -- Daily weather, Dhaka 2025
    Chennai_Weather_1951_2024.xlsx   -- Long-term monthly record,
                                        Chennai (1951-2024)
    Chennai_Weather_detailed_2023.xlsx -- Detailed daily data, 2023

  All_Eight_Cities_2022_2025/
    Daily weather data (Open-Meteo format) for all eight study cities,
    years 2022-2025 (32 files, one per city per year).
    Variables: temperature (mean/min/max), precipitation,
    relative humidity, and related parameters.
    Used to drive the physics-based indoor R_indoor simulations.


3_Physics_Simulation_Data/
  Inputs and outputs of the mechanistic dengue transmission model
  (Index P / R0 model) used to estimate indoor basic reproduction
  numbers across temperature scenarios.

  indoor_physics_inputs.csv
      Indoor temperature and humidity scenario grid fed into the
      physics model (AC and non-AC spaces, 1 degree C resolution).

  final_simulation_results.csv
      Predicted dengue case counts from the integrated physics-
      informed ML framework for each city and temperature scenario,
      with Monte Carlo uncertainty bounds (2.5th-97.5th percentile).

  R0_Calculations_Data.xlsx
      Detailed R0 calculation workbook (all months, outdoor,
      indoor non-AC, and indoor AC at various setpoints, Dhaka).
      Used for model validation (Pearson r = 0.997, MAE = 2.48%).

  Indoor_R0_Calculations.xlsx
      Comprehensive indoor basic reproduction number calculations
      for all cities and temperature/intervention scenarios.


4_LCA_Eco_efficiency_Data/
  Life cycle assessment (LCA) and eco-efficiency calculation workbooks
  for the 1.5-ton split AC unit and standing fan.

  LCA_Final_Results_and_Calculations.xlsx
      Full LCA results and eco-efficiency calculations, including
      Annual Environmental Externality Costs (AEEC), consumer costs,
      standalone and integrated eco-efficiency ratios, and Monte Carlo
      uncertainty outputs. Covers all eight cities and temperature
      setpoint scenarios.

  VCDD_Energy_Consumption_Calculations.xlsx
      Variable Cooling Degree Days (VCDD) and annual electricity
      consumption calculations for the AC unit, disaggregated by
      city, building envelope type (insulated/uninsulated), and
      temperature setpoint.


5_Code/
  Python (Jupyter Notebook) implementations of the ML model and
  physics-informed simulation framework.

  DengueML_Model.ipynb
      Original notebook: data harmonization, Random Forest model
      training on Dhaka/Jakarta/Cebu data, and application to
      indoor_physics scenario grid.

  ML_Framework_v3.3_Revised.ipynb
      Revised and extended ML framework (April 2026) incorporating
      HistGradientBoosting, cross-validation, and full eight-city
      simulation pipeline.

  Full code also available at:
  https://github.com/bicbioeng/dengue-prediction-ml

========================================================================
NOTES ON DATA SOURCES
========================================================================
- Weather data sourced from Open-Meteo (open-meteo.com) and Meteostat.
- Dengue case data sourced from national health surveillance dashboards:
    Dhaka:          Directorate General of Health Services (DGHS), Bangladesh
    Jakarta:        Indonesian Ministry of Health / Kemenkes
    Cebu:           Department of Health (DOH), Philippines
    Chennai/TN:     Directorate of Public Health, Tamil Nadu
- LCA inventory modeled per ISO 14040/14044 standards.
- Monte Carlo uncertainty propagation: N = 5,000 iterations.

========================================================================
CONTACT
========================================================================
Venkata K.K. Upadhyayula: krishna.upadhyayula@umu.se
Venkataramana Gadhamshetty: venkataramana.gadhamshetty@sdsmt.edu
Etienne Z. Gnimpieba: etienne.gnimpieba@usd.edu
========================================================================
