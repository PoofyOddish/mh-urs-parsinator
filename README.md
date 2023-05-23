# MH URS Parsinator 
## Overview
Scripting to extract mental health-related data from [SAMHSA's URS tables](https://www.samhsa.gov/data/data-we-collect/urs-uniform-reporting-system).
## About
This project uses [Tabula-py](https://github.com/chezou/tabula-py) to parse Uniform Reporting System (URS) data stored in PDF format. Extracted data is validated using [Pydantic](https://github.com/pydantic/pydantic) and pushed into a GraphQL API (coming soon).