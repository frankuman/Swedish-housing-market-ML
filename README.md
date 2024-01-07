![image](https://github.com/frankuman/Swedish-housing-market-ML/assets/57047010/c7d51d4d-6136-40be-9212-ff37ff4dd0d3)

# VärderingsMaskinen - A machine learned valuator for the swedish housing market




## Project Overview
The housing market has always been a challenge to predict.
In 2023 house prices decreased by 6%, but in general apart-
ment prices increased. Housing in Sweden in the last 12 years
alone has risen an astounding 85% (adjusted to inflation) to
the top of 2021, but fallen a bit since then. With housing prices
of a median in 2.3 million Swedish krona, buying residency
is often the biggest investment a person does in their life.
The best way to sell a house has always, through out
time, been to evaluate it with a broker. The broker checks
the price similarity in the region, area, and street. Calculates
the average price per square meter and then takes the sellers
apartments size and calculates accordingly. The amount of
rooms, balcony, and the age of the apartment may vary the
listing price, but it is usually the bidding price that is harder
to predict, since the time, economy many other factors can
change it alot. 

That is why VarderingsMaskingen (The Valuation Machine)
will evaluate the housing of your choice, even if the sort of
housing doesn’t even exist. It uses Random Forest Regressor
to learn from a database including 600,000 different listings,
and gets a mean error of 9% of the mean price

## Table of Contents
- [Project Overview](#project-overview)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Getting Started](#getting-started)
- [Configuration](#configuration)
- [Usage](#usage)
- [Known Issues](#known-issues)
  
## Features
- **Valuator**: Uses a 600k large database of swedish housing market and random forest regressor to predict it.
- **GUI**: Python flask GUI for easier usage.

## Requirements
- Python 3.7.0 or higher
- Pip
- Network connection

## Installation
1. Download the project files using either **git** or manual download.
2. Open a terminal and navigate to the project directory.
3. Run the following command to install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Getting Started
1. Navigate to the `/data/` directory and unzip the `prop.rar`. Ensure the extracted file is named `prop.json`.
2. (**Auto creation**). Execute the following command for automatic creation, note that is usually trains within 10 minutes:
   ```bash
   python autocreate.py
   ```
   -OR-
3. (**Manual creation / Teacher variant**). Open the `create.ipynb` Jupyter notebook file and execute the provided steps. Note: Some steps may not be necessary, follow the instructions in the notebook. This process may take a maximum of 10 minutes.
4. Start the valuator by running:
   ```bash
   python vm.py
   ```
5. Open your web browser and go to `127.0.0.1:5000`.


## Configuration
The `create.ipynb` Jupyter notebook file can be modified to implement different approaches to the problem.

## Usage
1. Visit `127.0.0.1:5000` in your web browser.
2. Enter the required criteria (all are mandatory; enter 0 if there is no specific value).
3. Wait for approximately 10 seconds.
4. Review the results.

## Known Issues
- Occasionally, Nominatim may encounter SSL certificate errors. This issue seems to have been resolved in the latest release. If encountered, try refreshing the SSL certificates in Python requests to resolve the problem.
To fix the issue for me, i used these commands
```bash
python -m pip install python-certifi-win32
```
```bash
pip install  --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org python-certifi-win32
```

Thank you

