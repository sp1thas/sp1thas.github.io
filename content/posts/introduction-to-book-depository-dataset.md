---
title: "Book Depository Dataset EDA"
date: 2020-01-18T15:24:09+02:00
draft: false
category: posts
tags:
    - dataset
    - python
    - eda
keywords:
    - book depository dataset
    - python eda
summary: This notebook introduces the Book Depository Dataset and extracts some useful insights.
---

kaggle dataset: [Book Depository Dataset](https://www.kaggle.com/sp1thas/book-depository-dataset)

kaggle notebook: [Introduction to Book Depository Dataset](https://www.kaggle.com/sp1thas/introduction-to-book-depository-dataset)

github repo: [book-depository-dataset](https://github.com/sp1thas/book-depository-dataset)

# Book Depository Dataset EDA
Through this notebook we will try to become familiar `Book Depository Dataset` and extract some usefull insights. The goal of this notebook is to become an introductory step for the dataset.


```python
import pandas as pd
import os
import json
from glob import glob
import matplotlib.pyplot as plt
import seaborn as sns
%matplotlib inline
```

## Dataset Structure
Files:
 - `categories.csv`
 - `dataset.csv`
 - `formats.csv`
 - `places.csv`

The dataset consists of 5 file, the main `dataset.csv` file and some extra files. Extra files works as lookup tables for category, author, format and publication place. The reason behind this decision was to prevent data redundancy.

Fields:

 * `authors`: Book's author(s) (`list of str`)
 * `bestsellers-rank`: Bestsellers ranking (`int`)
 * `categories`: Book's categories. Check `authors.csv` for mapping (`list of int`)
 * `description`: Book description (`str`)
 * `dimension_x`: Book's dimension X (`float` cm)
 * `dimension_y`: Book's dimension Y (`float` cm)
 * `dimension_z`: Book's dimension Z (`float` mm)
 * `edition`: Edition (`str`)
 * `edition-statement`: Edition statement (`str`)
 * `for-ages`: Range of ages (`str`)
 * `format`: Book's format. Check `formats.csv` for mapping (`int`)
 * `id`: Book's unique id (`int`)
 * `illustrations-note`: 
 * `imprint`: 
 * `index-date`: Book's crawling date (`date`)
 * `isbn10`: Book's ISBN-10 (`str`)
 * `isbn13`: Book's ISBN-13 (`str`)
 * `lang`: List of book' language(s)
 * `publication-date`: Publication date (`date`)
 * `publication-place`: Publication place (`id`)
 * `publisher`: Publisher (`str`)
 * `rating-avg`: Rating average [0-5] (`float`)
 * `rating-count`: Number of ratings
 * `title`: Book's title (`str`)
 * `url`: Book relative url (https://bookdepository.com + `url`)
 * `weight`: Book's weight (`float` gr)

So, lets assign each file to a different dataframe


```python
if os.path.exists('../input/book-depository-dataset'):
    path_prefix = '../input/book-depository-dataset/{}.csv'
else:
    path_prefix = '../export/kaggle/{}.csv'


df, df_f, df_a, df_c, df_p = [
    pd.read_csv(path_prefix.format(_)) for _ in ('dataset', 'formats', 'authors', 'categories', 'places')
]
```


```python
# df = df.sample(n=500)
df.head()
```

{{< rawhtml >}}
<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>authors</th>
      <th>bestsellers-rank</th>
      <th>categories</th>
      <th>description</th>
      <th>dimension-x</th>
      <th>dimension-y</th>
      <th>dimension-z</th>
      <th>edition</th>
      <th>edition-statement</th>
      <th>for-ages</th>
      <th>...</th>
      <th>isbn10</th>
      <th>isbn13</th>
      <th>lang</th>
      <th>publication-date</th>
      <th>publication-place</th>
      <th>rating-avg</th>
      <th>rating-count</th>
      <th>title</th>
      <th>url</th>
      <th>weight</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>[1]</td>
      <td>57858</td>
      <td>[220, 233, 237, 2644, 2679, 2689]</td>
      <td>They were American and British air force offic...</td>
      <td>142.0</td>
      <td>211.0</td>
      <td>20.0</td>
      <td>NaN</td>
      <td>Reissue</td>
      <td>NaN</td>
      <td>...</td>
      <td>393325792</td>
      <td>9.780393e+12</td>
      <td>en</td>
      <td>2004-08-17</td>
      <td>1.0</td>
      <td>4.24</td>
      <td>6688.0</td>
      <td>The Great Escape</td>
      <td>/Great-Escape-Paul-Brickhill/9780393325799</td>
      <td>243.00</td>
    </tr>
    <tr>
      <th>1</th>
      <td>[2, 3]</td>
      <td>114465</td>
      <td>[235, 3386]</td>
      <td>John Moran and Carl Williams were the two bigg...</td>
      <td>127.0</td>
      <td>203.2</td>
      <td>25.4</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>...</td>
      <td>184454737X</td>
      <td>9.781845e+12</td>
      <td>en</td>
      <td>2009-03-13</td>
      <td>2.0</td>
      <td>3.59</td>
      <td>291.0</td>
      <td>Underbelly : The Gangland War</td>
      <td>/Underbelly-Andrew-Rule/9781844547371</td>
      <td>285.76</td>
    </tr>
    <tr>
      <th>2</th>
      <td>[4]</td>
      <td>61,471</td>
      <td>[241, 245, 247, 249, 378]</td>
      <td>Plain English is the art of writing clearly, c...</td>
      <td>136.0</td>
      <td>195.0</td>
      <td>16.0</td>
      <td>Revised</td>
      <td>4th Revised edition</td>
      <td>NaN</td>
      <td>...</td>
      <td>199669171</td>
      <td>9.780200e+12</td>
      <td>en</td>
      <td>2013-09-15</td>
      <td>3.0</td>
      <td>4.18</td>
      <td>128.0</td>
      <td>Oxford Guide to Plain English</td>
      <td>/Oxford-Guide-Plain-English-Martin-Cutts/97801...</td>
      <td>338.00</td>
    </tr>
    <tr>
      <th>3</th>
      <td>[5]</td>
      <td>1,347,994</td>
      <td>[245, 253, 263, 273, 274, 276, 279, 280, 281, ...</td>
      <td>When travelling, do you want to journey off th...</td>
      <td>136.0</td>
      <td>190.0</td>
      <td>33.0</td>
      <td>Unabridged</td>
      <td>Unabridged edition</td>
      <td>NaN</td>
      <td>...</td>
      <td>1444185497</td>
      <td>9.781444e+12</td>
      <td>en</td>
      <td>2014-12-03</td>
      <td>2.0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>Get Talking and Keep Talking Portuguese Total ...</td>
      <td>/Get-Talking-Keep-Talking-Portuguese-Total-Aud...</td>
      <td>156.00</td>
    </tr>
    <tr>
      <th>4</th>
      <td>[6]</td>
      <td>58154</td>
      <td>[1938, 1941, 1995]</td>
      <td>No matter what your actual job title, you are-...</td>
      <td>179.0</td>
      <td>229.0</td>
      <td>18.0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>...</td>
      <td>321934075</td>
      <td>9.780322e+12</td>
      <td>en</td>
      <td>2016-02-28</td>
      <td>4.0</td>
      <td>4.30</td>
      <td>212.0</td>
      <td>The Truthful Art : Data, Charts, and Maps for ...</td>
      <td>/Truthful-Art-Alberto-Cairo/9780321934079</td>
      <td>732.00</td>
    </tr>
  </tbody>
</table>
<p>5 rows × 25 columns</p>
</div>
{{< /rawhtml >}}


## Basic Stats
Firtly, lets display some basic statistics:


```python
df.describe()
```



{{< rawhtml >}}
<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>dimension-x</th>
      <th>dimension-y</th>
      <th>dimension-z</th>
      <th>id</th>
      <th>isbn13</th>
      <th>publication-place</th>
      <th>rating-avg</th>
      <th>rating-count</th>
      <th>weight</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>count</th>
      <td>742112.000000</td>
      <td>713278.000000</td>
      <td>742112.000000</td>
      <td>7.790050e+05</td>
      <td>7.658780e+05</td>
      <td>556846.000000</td>
      <td>502381.000000</td>
      <td>5.023810e+05</td>
      <td>714289.000000</td>
    </tr>
    <tr>
      <th>mean</th>
      <td>160.560373</td>
      <td>222.289753</td>
      <td>25.609538</td>
      <td>9.781553e+12</td>
      <td>9.781559e+12</td>
      <td>247.989972</td>
      <td>3.932002</td>
      <td>1.187949e+04</td>
      <td>444.768939</td>
    </tr>
    <tr>
      <th>std</th>
      <td>37.487785</td>
      <td>43.145377</td>
      <td>44.218401</td>
      <td>1.563374e+09</td>
      <td>1.565216e+09</td>
      <td>643.253808</td>
      <td>0.530740</td>
      <td>1.174093e+05</td>
      <td>610.212039</td>
    </tr>
    <tr>
      <th>min</th>
      <td>0.250000</td>
      <td>1.000000</td>
      <td>0.130000</td>
      <td>9.771131e+12</td>
      <td>9.780000e+12</td>
      <td>1.000000</td>
      <td>1.000000</td>
      <td>1.000000e+00</td>
      <td>15.000000</td>
    </tr>
    <tr>
      <th>25%</th>
      <td>135.000000</td>
      <td>198.000000</td>
      <td>9.140000</td>
      <td>9.780764e+12</td>
      <td>9.780772e+12</td>
      <td>2.000000</td>
      <td>3.690000</td>
      <td>6.000000e+00</td>
      <td>172.370000</td>
    </tr>
    <tr>
      <th>50%</th>
      <td>152.000000</td>
      <td>229.000000</td>
      <td>16.000000</td>
      <td>9.781473e+12</td>
      <td>9.781475e+12</td>
      <td>8.000000</td>
      <td>4.000000</td>
      <td>5.200000e+01</td>
      <td>299.000000</td>
    </tr>
    <tr>
      <th>75%</th>
      <td>183.000000</td>
      <td>240.000000</td>
      <td>25.000000</td>
      <td>9.781723e+12</td>
      <td>9.781724e+12</td>
      <td>178.000000</td>
      <td>4.220000</td>
      <td>6.880000e+02</td>
      <td>521.630000</td>
    </tr>
    <tr>
      <th>max</th>
      <td>1905.000000</td>
      <td>1980.000000</td>
      <td>1750.000000</td>
      <td>9.798485e+12</td>
      <td>9.798389e+12</td>
      <td>5501.000000</td>
      <td>5.000000</td>
      <td>5.870281e+06</td>
      <td>90717.530000</td>
    </tr>
  </tbody>
</table>
</div>
{{< /rawhtml >}}


**Publication Date Distribution**:
Most books are published in t


```python
df["publication-date"] = df["publication-date"].astype("datetime64")
df.groupby(df["publication-date"].dt.year).id.count().plot(title='Publication date distribution')
```




    <matplotlib.axes._subplots.AxesSubplot at 0x7f7827af68d0>




    
![png](/introduction-to-book-depository-dataset_8_1.png)
    



```python
df["index-date"] = df["index-date"].astype("datetime64")
df.groupby(df["index-date"].dt.month).id.count().plot(title='Crawling date distribution')
```




    <matplotlib.axes._subplots.AxesSubplot at 0x7f7827af61d0>




    
![png](/introduction-to-book-depository-dataset_9_1.png)
    



```python
df.groupby(['lang']).id.count().sort_values(ascending=False)[:5].plot(kind='pie', title="Most common languages")
```




    <matplotlib.axes._subplots.AxesSubplot at 0x7f78279aca58>




    
![png](/introduction-to-book-depository-dataset_10_1.png)
    



```python
import math
sns.lineplot(data=df.groupby(df['rating-avg'].dropna().apply(int)).id.count().reset_index(), x='rating-avg', y='id')
```




    <matplotlib.axes._subplots.AxesSubplot at 0x7f7827970dd8>




    
![png](i/introduction-to-book-depository-dataset_11_1.png)
    



```python
dims = pd.DataFrame({
    'dims': df['dimension-x'].fillna('0').astype(int).astype(str).str.cat(df['dimension-y'].fillna('0').astype(int).astype(str),sep=" x ").replace('0 x 0', 'Unknown').values, 
    'id': df['id'].values
})
dims.groupby(['dims']).id.count().sort_values(ascending=False)[:8].plot(kind='pie', title="Most common dimensions")
```




    <matplotlib.axes._subplots.AxesSubplot at 0x7f77ee8a2b38>




    
![png](/introduction-to-book-depository-dataset_12_1.png)
    



```python
pd.merge(
    df[['id', 'publication-place']], df_p, left_on='publication-place', right_on='place_id'
).groupby(['place_name']).id.count().sort_values(ascending=False)[:8].plot(kind='pie', title="Most common publication places")
```




    <matplotlib.axes._subplots.AxesSubplot at 0x7f77ee96a208>




    
![png](/introduction-to-book-depository-dataset_13_1.png)
    

