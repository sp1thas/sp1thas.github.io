Title: Introduction to Book Depository Dataset
Date: 2020-01-18 18:40
Modified: 2020-01-18 18:40
Tags: python, dataset
Category: blog
Slug: introduction-to-book-depository-dataset
Author: Panagiotis Simakis
Summary: A large collection of books, scraped from bookdepository.com

Through this notebook we will try to become familiar `Book Depository Dataset` and extract some useful insights. The goal of this notebook is to become an introductory step for the dataset.

```python
import pandas as pd
import os
import json
```


```python
if os.path.exists('../input/'):
    path_prefix = '../input/{}.csv'
else:
    path_prefix = '../export/{}.csv'

df, df_f, df_a, df_c = [
    pd.read_csv(path_prefix.format(_)) for _ in ('dataset', 'formats', 'authors', 'categories')
]
```


```python
df.head()
```




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
      <th>dimension_x</th>
      <th>dimension_y</th>
      <th>dimension_z</th>
      <th>dimensions</th>
      <th>edition</th>
      <th>edition-statement</th>
      <th>...</th>
      <th>format</th>
      <th>id</th>
      <th>illustrations-note</th>
      <th>imprint</th>
      <th>index-date</th>
      <th>isbn10</th>
      <th>isbn13</th>
      <th>lang</th>
      <th>publication-date</th>
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
      <td>NaN</td>
      <td>Reissue</td>
      <td>...</td>
      <td>1</td>
      <td>9780393325799</td>
      <td>16 pages of photographs</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>393325792</td>
      <td>9.780393e+12</td>
      <td>["en"]</td>
      <td>2004-08-17</td>
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
      <td>1</td>
      <td>9781844547371</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>184454737X</td>
      <td>9.781845e+12</td>
      <td>["en"]</td>
      <td>2009-03-13</td>
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
      <td>NaN</td>
      <td>Revised</td>
      <td>4th Revised edition</td>
      <td>...</td>
      <td>1</td>
      <td>9780199669172</td>
      <td>Illustrations (black and white)</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>199669171</td>
      <td>9.780200e+12</td>
      <td>["en"]</td>
      <td>2013-09-15</td>
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
      <td>NaN</td>
      <td>Unabridged</td>
      <td>Unabridged edition</td>
      <td>...</td>
      <td>2</td>
      <td>9781444185492</td>
      <td>NaN</td>
      <td>TEACH YOURSELF</td>
      <td>NaN</td>
      <td>1444185497</td>
      <td>9.781444e+12</td>
      <td>["en"]</td>
      <td>2014-12-03</td>
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
      <td>1</td>
      <td>9780321934079</td>
      <td>NaN</td>
      <td>New Riders Publishing</td>
      <td>NaN</td>
      <td>321934075</td>
      <td>9.780322e+12</td>
      <td>["en"]</td>
      <td>2016-02-28</td>
      <td>732.00</td>
    </tr>
  </tbody>
</table>
<p>5 rows × 21 columns</p>
</div>




```python
df_a.head()
```




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
      <th>author_id</th>
      <th>author_name</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>Paul Brickhill</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2</td>
      <td>John Silvester</td>
    </tr>
    <tr>
      <th>2</th>
      <td>3</td>
      <td>Andrew Rule</td>
    </tr>
    <tr>
      <th>3</th>
      <td>4</td>
      <td>Martin Cutts</td>
    </tr>
    <tr>
      <th>4</th>
      <td>5</td>
      <td>Sue Tyson-Ward</td>
    </tr>
  </tbody>
</table>
</div>




```python
df_f.head()
```




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
      <th>format_id</th>
      <th>format_name</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>Paperback</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2</td>
      <td>CD</td>
    </tr>
    <tr>
      <th>2</th>
      <td>3</td>
      <td>Hardback</td>
    </tr>
    <tr>
      <th>3</th>
      <td>4</td>
      <td>Mixed</td>
    </tr>
    <tr>
      <th>4</th>
      <td>5</td>
      <td>Pre</td>
    </tr>
  </tbody>
</table>
</div>




```python
df_c.head()
```




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
      <th>category_id</th>
      <th>category_name</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>220</td>
      <td>Biography: Historical, Political &amp; Military</td>
    </tr>
    <tr>
      <th>1</th>
      <td>233</td>
      <td>Memoirs</td>
    </tr>
    <tr>
      <th>2</th>
      <td>237</td>
      <td>True War  &amp; Combat Stories</td>
    </tr>
    <tr>
      <th>3</th>
      <td>2644</td>
      <td>European History</td>
    </tr>
    <tr>
      <th>4</th>
      <td>2679</td>
      <td>Military History</td>
    </tr>
  </tbody>
</table>
</div>




```python
def parse_list_fields(x):
    if isinstance(x, str):
        return json.loads(x)
    elif isinstance(x, list):
        return x
    else:
        return []
```


```python
df['categories'] = df['categories'].apply(parse_list_fields)
df['authors'] = df['authors'].apply(parse_list_fields)
```


```python

```

