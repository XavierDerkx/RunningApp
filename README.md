# RunningApp

## Description

RunningApp is a small project to build a stand-alone desktop app and a micro-SaaS to analyse and visualise running sessions.

## Getting Started

### Dependencies

* Pandas, Dash

* coverage (to run the unit tests) 
  
  ### Installing
  
  ```
  # using pip
  pip install -r requirements.txt
  
  # using Conda
  conda create --name <env_name> --file requirements.txt
  ```
  
  ### Executing
  
  ```
  # running the code
  python src/main.py 
  
  # running the test
  # ./run_tests.sh
  ```

## Version History

* v. 0.1 : Prototype
  
  ## License
  
  N/A

## QA

- [ ] Unit tests

- [ ] Test coverage

- [x] PEP8-compliant

- [ ] Documentation

## Road Map

### Data

* Improve the OMH/OMD to binary script and incorporate it into the OnMove data source class.

* Add support for GPX format (including XML validation).

* Define and enforce a common format for data once cleaned, common to all input formats.

### Analysis

* Add summary analysis for a given run.

* Add comparison between several runs.

* Decide which KPI to calculate (speed VS distance, pace VS distance etc)

* Add graphs for these KPI.

* Improve the display of the maps. Add options for GoogleMap / OpenStreetMap (APIS?)

### Desktop app

- Make UI with Dash.

- Store runs with SQL (sqlite).

- Dockerise.

### Web app

- Migrate to Flask + Dash within Flask.

- Use SQL (Postgre).

- Add User management.

- Add Admin panel.

- Dockerise.

- REST API as an exercice.
