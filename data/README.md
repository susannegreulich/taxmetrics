# Data Source URLS

I used the OECD data explorer, went to the respective tables given by the URLs below, chose the settings/configs, and then 
used the Developer API links for the data query and structure query. Below is a list of all the table links and queries.


tax link: https://data-explorer.oecd.org/vis?fs[0]=Topic%2C1%7CTaxation%23TAX%23%7CGlobal%20tax%20revenues%23TAX_GTR%23&pg=0&fc=Topic&bp=true&snb=155&df[ds]=dsDisseminateFinalDMZ&df[id]=DSD_REV_COMP_GLOBAL%40DF_RSGLOBAL&df[ag]=OECD.CTP.TPS&df[vs]=2.1&dq=..S13.T_5000%2BT_4000%2BT_2000%2BT_1000%2B_T..PT_B1GQ.A&to[TIME_PERIOD]=false&pd=1990%2C2023
tax data query: https://sdmx.oecd.org/public/rest/data/OECD.CTP.TPS,DSD_REV_COMP_GLOBAL@DF_RSGLOBAL,2.1/..S13.T_5000+T_4000+T_2000+T_1000+_T..PT_B1GQ.A?startPeriod=1990&endPeriod=2023&dimensionAtObservation=AllDimensions
tax structure query: https://sdmx.oecd.org/public/rest/dataflow/OECD.CTP.TPS/DSD_REV_COMP_GLOBAL@DF_RSGLOBAL/2.1?references=all

unit: percentage of GDP

# GDP link: https://data-explorer.oecd.org/vis?tm=annual%20gdp%20developer&pg=0&hc[Table%20identifier]=&snb=157&df[ds]=dsDisseminateFinalDMZ&df[id]=DSD_NAMAIN10%40DF_TABLE1&df[ag]=OECD.SDD.NAD&df[vs]=2.0&dq=A..S1..B1GQ._Z._Z._Z.USD_PPP.V.N.T0102&pd=1990%2C2023&to[TIME_PERIOD]=false
data "https://sdmx.oecd.org/public/rest/data/OECD.SDD.NAD,DSD_NAMAIN10@DF_TABLE1,2.0/A..S1..B1GQ._Z._Z._Z.USD_PPP.V.N.T0102?startPeriod=1990&endPeriod=2023&dimensionAtObservation=AllDimensions"
structure: 'https://sdmx.oecd.org/public/rest/dataflow/OECD.SDD.NAD/DSD_NAMAIN10@DF_TABLE1/2.0?references=all',
Combined transaction: 

Gross domestic product
Combined unit of measure: 

US dollars, PPP converted, Current prices, Millions


population: https://data-explorer.oecd.org/vis?tm=population&pg=0&hc[Transaction]=&snb=305&df[ds]=dsDisseminateFinalDMZ&df[id]=DSD_NAMAIN10%40DF_TABLE3&df[ag]=OECD.SDD.NAD&df[vs]=2.0&dq=A..S1.S1.POP.._Z..PS...&pd=1990%2C2023&to[TIME_PERIOD]=false
data query: https://sdmx.oecd.org/public/rest/data/OECD.SDD.NAD,DSD_NAMAIN10@DF_TABLE3,2.0/A..S1.S1.POP.._Z..PS...?startPeriod=1990&endPeriod=2023&dimensionAtObservation=AllDimensions
structure query: https://sdmx.oecd.org/public/rest/dataflow/OECD.SDD.NAD/DSD_NAMAIN10@DF_TABLE3/2.0?references=all

unit: persons THOUSAND
Institutional sector: 

Total economy
Counterpart institutional sector: 

Total economy
Transaction: 

Total population
Combined unit of measure: 

Persons, Thousands