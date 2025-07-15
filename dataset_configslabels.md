# Dataset Configurations

This file contains information about columns that were removed from each dataset because they had only one unique value.
**Note:** The unique values shown below are the human-readable labels (not the original identifiers).

## Population Dataset

### Removed Columns (Single Unique Value)

| Column             | Unique Value (Label)                   |
|--------------------|----------------------------------------|
| FREQ               | Annual                                 |
| SECTOR             | Total economy                          |
| COUNTERPART_SECTOR | Total economy                          |
| TRANSACTION        | Total population                       |
| INSTR_ASSET        | Not applicable                         |
| ACTIVITY           | Not applicable                         |
| EXPENDITURE        | Not applicable                         |
| UNIT_MEASURE       | Persons                                |
| PRICE_BASE         | Not applicable                         |
| TRANSFORMATION     | Non transformed data                   |
| TABLE_IDENTIFIER   | Table 0110 - Population and employment |

### Columns Kept

Total columns kept: 3

```
TIME_PERIOD
REF_AREA
value
```

### Summary

- Original columns: 14
- Columns kept: 3
- Columns removed: 11

---

## GDP Dataset

### Removed Columns (Single Unique Value)

| Column             | Unique Value (Label)                                |
|--------------------|-----------------------------------------------------|
| FREQ               | Annual                                              |
| SECTOR             | Total economy                                       |
| COUNTERPART_SECTOR | Total economy                                       |
| TRANSACTION        | Gross domestic product                              |
| INSTR_ASSET        | Not applicable                                      |
| ACTIVITY           | Not applicable                                      |
| EXPENDITURE        | Not applicable                                      |
| UNIT_MEASURE       | US dollars, PPP converted                           |
| PRICE_BASE         | Current prices                                      |
| TRANSFORMATION     | Non transformed data                                |
| TABLE_IDENTIFIER   | Table 0102 - GDP identity from the expenditure side |

### Columns Kept

Total columns kept: 3

```
TIME_PERIOD
REF_AREA
value
```

### Summary

- Original columns: 14
- Columns kept: 3
- Columns removed: 11

---

## Tax Revenues Dataset

### Removed Columns (Single Unique Value)

| Column                | Unique Value (Label) |
|-----------------------|--------------------|
| MEASURE               | Tax revenue        |
| SECTOR                | General government |
| CTRY_SPECIFIC_REVENUE | Total              |
| UNIT_MEASURE          | Percentage of GDP  |
| FREQ                  | Annual             |

### Columns Kept

Total columns kept: 4

```
TIME_PERIOD
REF_AREA
STANDARD_REVENUE
value
```

### Summary

- Original columns: 9
- Columns kept: 4
- Columns removed: 5

---

