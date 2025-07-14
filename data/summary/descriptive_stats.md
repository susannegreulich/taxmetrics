# Descriptive Statistics Report

**Generated on:** 2025-07-14 15:51:33

## Overview

This report provides comprehensive descriptive statistics for the VALUE column in the three labeled datasets:

1. **GDP** - Economic growth indicators (US dollars, PPP converted)
2. **Population** - Population counts (persons)
3. **Tax Revenues** - Government tax revenue data (percentage of GDP)

## Summary Table

| Dataset      | Total Rows | Valid Values | Missing Values (%) | Mean         | Median      | Std Dev      | Min       | Max           |
|--------------|------------|--------------|--------------------|--------------|-------------|--------------|-----------|---------------|
| GDP          | 1,737      | 1,737        | 0.0              % | 1175905.8143 | 292449.4170 | 3033677.4022 | 2762.1750 | 35520435.3970 |
| Population   | 1,740      | 1,740        | 0.0              % | 60859.2145   | 10589.2950  | 185765.6605  | 254.7880  | 1412600.0000  |
| Tax Revenues | 8,614      | 8,614        | 0.0              % | 11.7579      | 9.5885      | 10.9832      | 0.0000    | 50.2860       |

## GDP

**File:** `data/labeled/gdp_labeled.csv`

### Data Quality

- **Total Observations:** 1,737
- **Valid Values:** 1,737
- **Missing Values:** 0 (0.0%)

### Central Tendency

- **Mean:** 1175905.8143
- **Median:** 292449.417

### Dispersion

- **Standard Deviation:** 3033677.4022
- **Range:** 35517673.222
- **Interquartile Range (IQR):** 917835.708
- **Coefficient of Variation:** 257.99%

### Percentiles

- **25th Percentile (Q1):** 94163.689
- **75th Percentile (Q3):** 1011999.397

### Distribution Shape

- **Skewness:** 6.0517
  - *Interpretation: Right-skewed (positive skew)*

- **Kurtosis:** 44.0815
  - *Interpretation: Heavy-tailed (leptokurtic)*

### Extreme Values

- **Minimum:** 2762.175
- **Maximum:** 35520435.397

## Population

**File:** `data/labeled/population_labeled.csv`

### Data Quality

- **Total Observations:** 1,740
- **Valid Values:** 1,740
- **Missing Values:** 0 (0.0%)

### Central Tendency

- **Mean:** 60859.2145
- **Median:** 10589.295

### Dispersion

- **Standard Deviation:** 185765.6605
- **Range:** 1412345.212
- **Interquartile Range (IQR):** 41109.828
- **Coefficient of Variation:** 305.24%

### Percentiles

- **25th Percentile (Q1):** 5197.3095
- **75th Percentile (Q3):** 46307.1375

### Distribution Shape

- **Skewness:** 6.0535
  - *Interpretation: Right-skewed (positive skew)*

- **Kurtosis:** 38.0018
  - *Interpretation: Heavy-tailed (leptokurtic)*

### Extreme Values

- **Minimum:** 254.788
- **Maximum:** 1412600.0

## Tax Revenues

**File:** `data/labeled/tax_revenues_labeled.csv`

### Data Quality

- **Total Observations:** 8,614
- **Valid Values:** 8,614
- **Missing Values:** 0 (0.0%)

### Central Tendency

- **Mean:** 11.7579
- **Median:** 9.5885

### Dispersion

- **Standard Deviation:** 10.9832
- **Range:** 50.286
- **Interquartile Range (IQR):** 11.2862
- **Coefficient of Variation:** 93.41%

### Percentiles

- **25th Percentile (Q1):** 3.2082
- **75th Percentile (Q3):** 14.4945

### Distribution Shape

- **Skewness:** 1.3208
  - *Interpretation: Right-skewed (positive skew)*

- **Kurtosis:** 1.0865
  - *Interpretation: Light-tailed (platykurtic)*

### Extreme Values

- **Minimum:** 0.0
- **Maximum:** 50.286

## Comparative Analysis

### Scale Comparison

The datasets operate on different scales:

- **GDP:** Very large scale (millions+) (mean: 1175905.8143)
- **Population:** Large scale (tens of thousands+) (mean: 60859.2145)
- **Tax Revenues:** Small scale (tens) (mean: 11.7579)

### Variability Comparison

Coefficient of Variation (CV) comparison (lower = less variable):

- **GDP:** CV = 257.99% (High variability)
- **Population:** CV = 305.24% (High variability)
- **Tax Revenues:** CV = 93.41% (High variability)

## Recommendations

### Data Quality

- **GDP:** Good data quality with low missing rate (0.0%).
- **Population:** Good data quality with low missing rate (0.0%).
- **Tax Revenues:** Good data quality with low missing rate (0.0%).

### Statistical Considerations

- **GDP:** Highly skewed distribution. Consider log transformation or non-parametric methods.
- **Population:** Highly skewed distribution. Consider log transformation or non-parametric methods.
- **Tax Revenues:** Highly skewed distribution. Consider log transformation or non-parametric methods.

---
*Report generated automatically by descriptive_statistics.py*