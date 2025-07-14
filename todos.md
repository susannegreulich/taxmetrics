# Todos: 

data:

queries:

# Data Source URLS

# GDP: https://data-explorer.oecd.org/vis?tm=annual%20gdp%20developer&pg=0&hc[Table%20identifier]=&snb=157&df[ds]=dsDisseminateFinalDMZ&df[id]=DSD_NAMAIN10%40DF_TABLE1&df[ag]=OECD.SDD.NAD&df[vs]=2.0&dq=A........PC%2BUSD_PPP_PS%2BUSD_PPP..G1.T0101&pd=1990%2C2024&to[TIME_PERIOD]=false
data: https://sdmx.oecd.org/public/rest/data/OECD.SDD.NAD,DSD_NAMAIN10@DF_TABLE1,2.0/A..S1...._T..PC+USD_PPP_PS+USD_PPP..G1.T0101?startPeriod=1990&endPeriod=2024&dimensionAtObservation=AllDimensions
structure: https://sdmx.oecd.org/public/rest/dataflow/OECD.SDD.NAD/DSD_NAMAIN10@DF_TABLE1/2.0?references=all

tax link: https://data-explorer.oecd.org/vis?fs[0]=Topic%2C1%7CTaxation%23TAX%23%7CGlobal%20tax%20revenues%23TAX_GTR%23&pg=0&fc=Topic&bp=true&snb=155&df[ds]=dsDisseminateFinalDMZ&df[id]=DSD_REV_COMP_GLOBAL%40DF_RSGLOBAL&df[ag]=OECD.CTP.TPS&df[vs]=2.1&dq=..S13._T..PT_B1GQ.A&lom=LASTNPERIODS&lo=10&to[TIME_PERIOD]=false
tax data: https://sdmx.oecd.org/public/rest/data/OECD.CTP.TPS,DSD_REV_COMP_GLOBAL@DF_RSGLOBAL,2.1/...T_5000+T_4000+T_2000+T_1000+_T..PT_B1GQ.A?startPeriod=1990&endPeriod=2023&dimensionAtObservation=AllDimensions
tax structure: https://sdmx.oecd.org/public/rest/dataflow/OECD.CTP.TPS/DSD_REV_COMP_GLOBAL@DF_RSGLOBAL/2.1?references=all

labor link: https://data-explorer.oecd.org/vis?tm=population%20labour&pg=0&snb=99&df[ds]=dsDisseminateFinalDMZ&df[id]=DSD_LFS%40DF_IALFS_LF_Q&df[ag]=OECD.SDD.TPS&df[vs]=1.0&dq=.LF.._Z.Y._T.Y15T64..Q&lom=LASTNPERIODS&lo=7&to[TIME_PERIOD]=false&vw=tb
labor data: https://sdmx.oecd.org/public/rest/data/OECD.SDD.TPS,DSD_LFS@DF_IALFS_LF_Q,1.0/.LF.._Z.Y._T.Y15T64..A?startPeriod=1990&endPeriod=2023&dimensionAtObservation=AllDimensions
labor structure: https://sdmx.oecd.org/public/rest/dataflow/OECD.SDD.TPS/DSD_LFS@DF_IALFS_LF_Q/1.0?references=all



gdp output table link: https://data-explorer.oecd.org/vis?tm=annual%20gdp&pg=0&fc=Measure&snb=317&df[ds]=dsDisseminateFinalDMZ&df[id]=DSD_NAMAIN10%40DF_TABLE1_OUTPUT&df[ag]=OECD.SDD.NAD&df[vs]=2.0&dq=A......_T..USD_EXC.V..&pd=1990%2C2023&to[TIME_PERIOD]=false&vw=tb
gdp data:  https://sdmx.oecd.org/public/rest/data/OECD.SDD.NAD,DSD_NAMAIN10@DF_TABLE1_OUTPUT,2.0/A......_T..USD_EXC.V..?startPeriod=1990&endPeriod=2023&dimensionAtObservation=AllDimensions
gdp structure: https://sdmx.oecd.org/public/rest/dataflow/OECD.SDD.NAD/DSD_NAMAIN10@DF_TABLE1_OUTPUT/2.0?references=all


make the unique values script output the unique values in csv, 1 table for each data set. ie exact same 'dimensions' as 
original datasets, but only with unique values. 



1. label ALL identifiers. still some left. 
2. get data for more countries. 

years correct
the right tax CATEGORies, RIGHT NOW, property and social securuity missing. 

Tax Revenues Labeled Data (18,439 rows, 9 columns)
Key Variables with All Unique Values:
TIME_PERIOD: 34 years (1990-2023) - complete time series
REF_AREA: 141 countries/regions (including country names like 'Australia', 'Austria', etc.)
MEASURE: 1 value - 'Tax revenue'
SECTOR: 1 value - 'General government'
STANDARD_REVENUE: 5 categories - 'Total tax revenue', 'Taxes on income, profits and capital gains', 'Taxes on goods and services', 'Taxes on payroll and workforce', 'Other taxes'
CTRY_SPECIFIC_REVENUE: 1 value - 'Total'
UNIT_MEASURE: 1 value - 'Percentage of GDP'
FREQ: 1 value - 'Annual'
value: 11,751 unique tax revenue percentages (0.0% to 146.8%)

GDP Labeled Data (19,749 rows, 14 columns)
Key Variables with All Unique Values:
TIME_PERIOD: 34 years (1990-2023)
REF_AREA: 64 countries/regions
TRANSACTION: 3 types - 'Gross domestic product', 'Gross national income', 'Gross national income per capita'
ACTIVITY: 13 categories including 'Total economy', 'Agriculture', 'Industry', 'Services', etc.
UNIT_MEASURE: 1 value - 'Percentage change'
value: 18,169 unique GDP growth rates (-7.4% to 24.0%)


Labor Force Labeled Data (1,106 rows, 11 columns)
Key Variables with All Unique Values:
TIME_PERIOD: 34 years (1990-2023)
REF_AREA: 47 countries/regions (full country names)
MEASURE: 1 value - 'Labour force'
UNIT_MEASURE: 1 value - 'PS' (Persons)
SEX: 1 value - 'Total'
AGE: 1 value - '15-64 years'
ACTIVITY: 1 value - 'Not applicable'
FREQ: 1 value - 'Annual'
value: 1,102 unique labor force values (153.8 to 649,174.9 thousand persons)


sanity check results. france's tax rate really low, can it be possible
add button options to interactive html. ie view by country, country averages, etc. 
add more data. fetch more data. more countries, more years. 
move the legend bar to bottom of html chart. EXPLAIN-UNDERSTAND THE CHART. 
add time series?;
check income distribution. which incomes is it? why total population only 1mio?
add SOURCES TO DATA. CURRENT URLS DON'T WORK. 

i'm going to have to collect the data and plan the analysis myself. 
first, find total revenues, then as percentage of GDP, then average GDP growth rate (to see relation
between taxation percentage and economic growth)
growth in revenues, vs growth in gdp
the optimal taxation regime maximizes ABSOLUTE REVENUES, but the absolute revenues must be compared RELATIVE TO POPULATION SIZE, since countries vary in size. 


total tax revenues
gdp
tax revenues/gdp
gdp growth rate
gdp per capita
tax revenue per capita
tax rev = tax base x rate. maximize base and rate. interactive effects. 
tax base = gdp

scatter plot tax base vs rate (gdp vs tax rate)
divided up in to tax TYPES, because it's that complicated. 

income tax rate vs gdp, vs tax revenues
corportae tax rate vs gdp, vs tax revenues
lever = tax rates. 
impact of tax rates on dependent variables tax revenue, gdp. 
tax revenue = a tax rate + b gdp multiple linear regression. 
interactive terms: various tax rates x gdp (because gdp function of tax rates)
evt draw a laffer curve


or import with identifiers as before, and just make a dictionary of labels. to be used in own python code, not necessary to import the data with labels. 


laffer curve: tax revenue as a function of tax rate. (revenues corresponding to rate of that particular tax type)

i need data for:
tax rates of various tax types
tax revenues for these various types, and total tax revenues
economic growth rate

scatter plots to see patterns. 


total tax revenues as percentage of gdp https://data-explorer.oecd.org/vis?fs[0]=Topic%2C1%7CTaxation%23TAX%23%7CGlobal%20tax%20revenues%23TAX_GTR%23&pg=0&fc=Topic&bp=true&snb=155&df[ds]=dsDisseminateFinalDMZ&df[id]=DSD_REV_COMP_GLOBAL%40DF_RSGLOBAL&df[ag]=OECD.CTP.TPS&df[vs]=2.1&dq=..S13._T..PT_B1GQ.A&lom=LASTNPERIODS&lo=10&to[TIME_PERIOD]=false&vw=ov


gdp https://data-explorer.oecd.org/vis?tm=gdp&pg=0&snb=364&df[ds]=dsDisseminateFinalDMZ&df[id]=DSD_NAMAIN10%40DF_TABLE1_OUTPUT&df[ag]=OECD.SDD.NAD&df[vs]=2.0&dq=A.AUS........V..&lom=LASTNPERIODS&lo=5&to[TIME_PERIOD]=false&vw=tb

find data for CAPITA, to divide gdp and tax revs per capita. labour force population. 
https://data-explorer.oecd.org/vis?tm=population&pg=0&snb=305&df[ds]=dsDisseminateFinalDMZ&df[id]=DSD_LFS%40DF_IALFS_LF_Q&df[ag]=OECD.SDD.TPS&df[vs]=1.0&dq=.LF.._Z.Y._T.Y15T64..A&lom=LASTNPERIODS&lo=7&to[TIME_PERIOD]=false


total tax revs per capita in absolute terms = tax rev pct gdp x gdp / capita

scatter plots, laffer curves patterns, for various tax revs PER CAPITA vs tax rates. 
scatter plot tax rates vs economic growth rate. 