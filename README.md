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
- Valuator
- GUI
## Requirements
- Python 3.7.0 or higher
- Pip
- Network connection
  
## Installation
1. Download the files either using **git** or manual download.
2. Run `pip install -r requirements.txt` on the machine.

## Getting Started
1. Go to /data/ and unzip the prop.rar. Important to keep the name prop.json
1. Open the create.ipynb jupyter file and run the steps. Some steps should not be run. This might also take a while
2. Start the valuator:  `python vm.py`
3. Go to 127.0.0.1:5000 in your webbrowser

## Configuration
The jupyter file create.ipynb can be modified to create different approaches to the problem.

## Usage
1. Go to 127.0.0.1:5000 in your webbrowser
2. Enter the criterias needed (all are needed, enter 0 if there is no criteria)
3. Wait for 10 seconds
4. See results
   
## Known Issues
Sometimes Nomatim gives SSL certificate error. I do not know why but this has resolved for me in the latest issue. Might need to refresh the SSL certificates in python requests to fix the issue

Thank you

