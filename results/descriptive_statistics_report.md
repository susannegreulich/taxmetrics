# Descriptive Statistics Report

**Generated on:** 2025-07-14 14:36:08

## Overview

This report provides comprehensive descriptive statistics for the VALUE column in the three labeled datasets:

1. **GDP Labeled Data** - Economic growth indicators
2. **Labor Force Labeled Data** - Employment statistics
3. **Tax Revenues Labeled Data** - Government revenue data

## Summary Table

| Dataset                   | Total Rows | Valid Values | Missing Values (%) | Mean       | Median    | Std Dev    | Min      | Max         |
|---------------------------|------------|--------------|--------------------|------------|-----------|------------|----------|-------------|
| GDP Labeled Data          | 3,009      | 3,009        | 0.0              % | 2.7462     | 2.8112    | 3.4719     | -15.2669 | 14.2931     |
| Labor Force Labeled Data  | 1,106      | 1,106        | 0.0              % | 35580.0134 | 5194.1375 | 86970.7557 | 153.8000 | 649174.9000 |
| Tax Revenues Labeled Data | 18,439     | 18,439       | 0.0              % | 9.2269     | 6.9370    | 9.4744     | 0.0000   | 50.2860     |

## GDP Labeled Data

**File:** `data/labeled/gdp_labeled.csv`

### Data Quality

- **Total Observations:** 3,009
- **Valid Values:** 3,009
- **Missing Values:** 0 (0.0%)

### Central Tendency

- **Mean:** 2.7462
- **Median:** 2.8112

### Dispersion

- **Standard Deviation:** 3.4719
- **Range:** 29.56
- **Interquartile Range (IQR):** 3.4456
- **Coefficient of Variation:** 126.43%

### Percentiles

- **25th Percentile (Q1):** 1.1803
- **75th Percentile (Q3):** 4.6259

### Distribution Shape

- **Skewness:** -0.6939
  - *Interpretation: Left-skewed (negative skew)*

- **Kurtosis:** 3.1052
  - *Interpretation: Heavy-tailed (leptokurtic)*

### Extreme Values

- **Minimum:** -15.2669
- **Maximum:** 14.2931

## Labor Force Labeled Data

**File:** `data/labeled/labor_force_labeled.csv`

### Data Quality

- **Total Observations:** 1,106
- **Valid Values:** 1,106
- **Missing Values:** 0 (0.0%)

### Central Tendency

- **Mean:** 35580.0134
- **Median:** 5194.1375

### Dispersion

- **Standard Deviation:** 86970.7557
- **Range:** 649021.1
- **Interquartile Range (IQR):** 21508.5588
- **Coefficient of Variation:** 244.44%

### Percentiles

- **25th Percentile (Q1):** 2669.2312
- **75th Percentile (Q3):** 24177.79

### Distribution Shape

- **Skewness:** 4.6259
  - *Interpretation: Right-skewed (positive skew)*

- **Kurtosis:** 24.6579
  - *Interpretation: Heavy-tailed (leptokurtic)*

### Extreme Values

- **Minimum:** 153.8
- **Maximum:** 649174.9

## Tax Revenues Labeled Data

**File:** `data/labeled/tax_revenues_labeled.csv`

### Data Quality

- **Total Observations:** 18,439
- **Valid Values:** 18,439
- **Missing Values:** 0 (0.0%)

### Central Tendency

- **Mean:** 9.2269
- **Median:** 6.937

### Dispersion

- **Standard Deviation:** 9.4744
- **Range:** 50.286
- **Interquartile Range (IQR):** 10.927
- **Coefficient of Variation:** 102.68%

### Percentiles

- **25th Percentile (Q1):** 1.734
- **75th Percentile (Q3):** 12.661

### Distribution Shape

- **Skewness:** 1.565
  - *Interpretation: Right-skewed (positive skew)*

- **Kurtosis:** 2.4192
  - *Interpretation: Light-tailed (platykurtic)*

### Extreme Values

- **Minimum:** 0.0
- **Maximum:** 50.286

## Comparative Analysis

### Scale Comparison

The datasets operate on different scales:

- **GDP Labeled Data:** Very small scale (units/percentages) (mean: 2.7462)
- **Labor Force Labeled Data:** Large scale (thousands+) (mean: 35580.0134)
- **Tax Revenues Labeled Data:** Very small scale (units/percentages) (mean: 9.2269)

### Variability Comparison

Coefficient of Variation (CV) comparison (lower = less variable):

- **GDP Labeled Data:** CV = 126.43% (High variability)
- **Labor Force Labeled Data:** CV = 244.44% (High variability)
- **Tax Revenues Labeled Data:** CV = 102.68% (High variability)

## Recommendations

### Data Quality

- **GDP Labeled Data:** Good data quality with low missing rate (0.0%).
- **Labor Force Labeled Data:** Good data quality with low missing rate (0.0%).
- **Tax Revenues Labeled Data:** Good data quality with low missing rate (0.0%).

### Statistical Considerations

- **GDP Labeled Data:** Moderately skewed. Parametric methods may still be appropriate.
- **Labor Force Labeled Data:** Highly skewed distribution. Consider log transformation or non-parametric methods.
- **Tax Revenues Labeled Data:** Highly skewed distribution. Consider log transformation or non-parametric methods.

---
*Report generated automatically by descriptive_statistics.py*