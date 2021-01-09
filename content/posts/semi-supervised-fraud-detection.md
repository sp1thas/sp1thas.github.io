---
title: Semi-Supervised Fraud Detection
date: 2020-03-30T15:24:09+02:00
draft: false
category: posts
tags:
  - python
  - machine learning
  - deep learning
keywords:
 - fraud detection
 - novelty detection
 - ensemble
 - learning representation
 - semi-supervised learning
summary: A jupyter notebook about semi-supervised fraud detection.
---

## Intro

**dataset:** [Credit Card Fraud Detection](https://www.kaggle.com/mlg-ulb/creditcardfraud)

**kaggle notebook:** [Semi-Supervised Fraud Detection](https://www.kaggle.com/sp1thas/semi-supervised-fraud-detection)

keywords: `fraud detection`, `novelty detection`, `ensembling`, `learning representation`, `semi-supervised learning`

Usually, datasets related to fraud detection are highly unbalanced due to the fact that, in the of transactions, only few of then are fraudulent. Instead of trying to augment the dataset using a resample method, we are going to approach this problem as a Novelty Detection problem.

On this kernel, we are goind describe the dataset briefly and then, we will compare multiple machine learning algorithms using some evaluation metrics.

Most common machine learning algorithms for this kind of tasks are the following:

1. Isolation forest
2. One class SVM
3. Autoencoders


### Isolation Forest
![isolation-tree](https://i.imgur.com/rzP7siS.png)

[source](https://blog.easysol.net/using-isolation-forests-anamoly-detection/)

> The Isolation Forest algorithm isolates observations by randomly selecting a feature and then randomly selecting a split value between the maximum and minimum values of the selected feature. The logic argument goes: isolating anomaly observations is easier because only a few conditions are needed to separate those cases from the normal observations. On the other hand, isolating normal observations require more conditions. Therefore, an anomaly score can be calculated as the number of conditions required to separate a given observation.


### One Class SVM (OCSVM)
![](https://ars.els-cdn.com/content/image/1-s2.0-S0031320314002751-gr6.jpg)

[source](https://towardsdatascience.com/outlier-detection-with-one-class-svms-5403a1a1878c)

> A One-Class Support Vector Machine is an unsupervised learning algorithm that is trained only on the ‘normal’ data, in our case the negative examples. It learns the boundaries of these points and is therefore able to classify any points that lie outside the boundary as, you guessed it, outliers.

### Autoencoders

[source](https://www.deeplearningbook.org/contents/autoencoders.html)

> An autoencoder is a neural network that is trained to attempt to copy its input to its output. Internally, it has a hidden layer h that describes a code used to represent the input. The network may be viewed as consisting of two parts: an encoder function `h = f (x)` and a decoder that produces a reconstruction `r = g(h)`.

![autoencoder](https://miro.medium.com/max/3524/1*oUbsOnYKX5DEpMOK3pH_lg.png)

In our case, we will train the autoencoder using samples of normal transactions only. After that, we will provide a fraudulent sample as input to the model. As a result, the representation should have larger loss error. Therefore, by defining a loss threashold, this ANN model will work as novelty detection model.

## Implementation

![implementation](https://i.imgur.com/Y8FWKqi.png)


```python
import numpy as np
import pandas as pd

from sklearn.ensemble import IsolationForest
from sklearn.svm import OneClassSVM
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, recall_score, f1_score, accuracy_score, precision_score
from sklearn.ensemble import VotingClassifier, RandomForestClassifier
from sklearn.decomposition import PCA, IncrementalPCA, LatentDirichletAllocation
from sklearn.manifold import TSNE

from tqdm.notebook import tqdm, trange
from typing import NoReturn, Union, List
from mlxtend.classifier import EnsembleVoteClassifier
import matplotlib.pyplot as plt
import seaborn as sns
import tensorflow as tf
from umap import UMAP
```


```python
df = pd.read_csv('../input/creditcardfraud/creditcard.csv')
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
      <th>Time</th>
      <th>V1</th>
      <th>V2</th>
      <th>V3</th>
      <th>V4</th>
      <th>V5</th>
      <th>V6</th>
      <th>V7</th>
      <th>V8</th>
      <th>V9</th>
      <th>...</th>
      <th>V21</th>
      <th>V22</th>
      <th>V23</th>
      <th>V24</th>
      <th>V25</th>
      <th>V26</th>
      <th>V27</th>
      <th>V28</th>
      <th>Amount</th>
      <th>Class</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>0.0</td>
      <td>-1.359807</td>
      <td>-0.072781</td>
      <td>2.536347</td>
      <td>1.378155</td>
      <td>-0.338321</td>
      <td>0.462388</td>
      <td>0.239599</td>
      <td>0.098698</td>
      <td>0.363787</td>
      <td>...</td>
      <td>-0.018307</td>
      <td>0.277838</td>
      <td>-0.110474</td>
      <td>0.066928</td>
      <td>0.128539</td>
      <td>-0.189115</td>
      <td>0.133558</td>
      <td>-0.021053</td>
      <td>149.62</td>
      <td>0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>0.0</td>
      <td>1.191857</td>
      <td>0.266151</td>
      <td>0.166480</td>
      <td>0.448154</td>
      <td>0.060018</td>
      <td>-0.082361</td>
      <td>-0.078803</td>
      <td>0.085102</td>
      <td>-0.255425</td>
      <td>...</td>
      <td>-0.225775</td>
      <td>-0.638672</td>
      <td>0.101288</td>
      <td>-0.339846</td>
      <td>0.167170</td>
      <td>0.125895</td>
      <td>-0.008983</td>
      <td>0.014724</td>
      <td>2.69</td>
      <td>0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>1.0</td>
      <td>-1.358354</td>
      <td>-1.340163</td>
      <td>1.773209</td>
      <td>0.379780</td>
      <td>-0.503198</td>
      <td>1.800499</td>
      <td>0.791461</td>
      <td>0.247676</td>
      <td>-1.514654</td>
      <td>...</td>
      <td>0.247998</td>
      <td>0.771679</td>
      <td>0.909412</td>
      <td>-0.689281</td>
      <td>-0.327642</td>
      <td>-0.139097</td>
      <td>-0.055353</td>
      <td>-0.059752</td>
      <td>378.66</td>
      <td>0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>1.0</td>
      <td>-0.966272</td>
      <td>-0.185226</td>
      <td>1.792993</td>
      <td>-0.863291</td>
      <td>-0.010309</td>
      <td>1.247203</td>
      <td>0.237609</td>
      <td>0.377436</td>
      <td>-1.387024</td>
      <td>...</td>
      <td>-0.108300</td>
      <td>0.005274</td>
      <td>-0.190321</td>
      <td>-1.175575</td>
      <td>0.647376</td>
      <td>-0.221929</td>
      <td>0.062723</td>
      <td>0.061458</td>
      <td>123.50</td>
      <td>0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>2.0</td>
      <td>-1.158233</td>
      <td>0.877737</td>
      <td>1.548718</td>
      <td>0.403034</td>
      <td>-0.407193</td>
      <td>0.095921</td>
      <td>0.592941</td>
      <td>-0.270533</td>
      <td>0.817739</td>
      <td>...</td>
      <td>-0.009431</td>
      <td>0.798278</td>
      <td>-0.137458</td>
      <td>0.141267</td>
      <td>-0.206010</td>
      <td>0.502292</td>
      <td>0.219422</td>
      <td>0.215153</td>
      <td>69.99</td>
      <td>0</td>
    </tr>
  </tbody>
</table>
<p>5 rows × 31 columns</p>
</div>
{{< /rawhtml >}}


### Dataset
 - `V{1-28}`: `PCA` decompossition outcome
 - `Class` label (0: normal, 1: fraudulent)
 - `Time`: Number of seconds elapsed between this transaction and the first transaction in the dataset
 - `Amount`: transaction amount


```python
# use a dataset sample for development purposes
dev = False
```


```python
df.groupby(['Class']).Class.count().plot(kind='pie', title='Fraudulent VS Genuine Transactions')
```




    <matplotlib.axes._subplots.AxesSubplot at 0x7f5dca0a79d0>




    
![png](semi-supervised-fraud-detection_files/semi-supervised-fraud-detection_6_1.png)
    



```python
df_s = df.sample(2000)
X = df_s[[_ for _ in df.columns if _ != 'Class']]

pca = PCA(n_components=2)
tsne = TSNE(n_components=2)
ump = UMAP(n_components=2)
ipca = IncrementalPCA(n_components=2)

x_pca = pca.fit_transform(X)
x_tsne = tsne.fit_transform(X)
x_umap = ump.fit_transform(X)
```

`PCA`, `UMAP` and `t-SNE` will be used for further dimensionality reduction in order to visualize a sample of the dataset


```python
fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(15, 5))

sizes = pd.Series(df_s['Class']+1).pow(5) # represent fraud with bigger point

axes[0].scatter(x_pca[:, 0], x_pca[:, 1], s=sizes, c=df_s['Class'].values)
axes[1].scatter(x_tsne[:, 0], x_tsne[:, 1], s=sizes, c=df_s['Class'].values)
axes[2].scatter(x_umap[:, 0], x_umap[:, 1], s=sizes, c=df_s['Class'].values)

axes[0].set_title('PCA')
axes[1].set_title('t-SNE')
axes[2].set_title('UMAP')

fig.tight_layout()
plt.show()
```


    
![png](semi-supervised-fraud-detection_files/semi-supervised-fraud-detection_9_0.png)
    


### Preprocessing
`Time` and `Amount` fields should be scaled

During the step of pre-processing, the dataset will be splited in two parts:
1. ~283K samples of genuine transactions (Training set)
2. All fraudulent samples and equal number of genuine samples (Test set)

Novelty detection is concered as a semi-supervised task due to the fact that only the normal samples are used during the phase of training. During the phase of evaluation, a balanced subset of genuine and fraudulent samples will be used.


```python
# time and amount scaling
df['Time'] = StandardScaler().fit_transform(df['Time'].values.reshape(-1, 1))
df['Amount'] = StandardScaler().fit_transform(df['Amount'].values.reshape(-1, 1))

df_anom = df[df['Class'] == 1]
df_norm = df[df['Class'] == 0]

if dev:
    df_norm = df_norm.sample(5000, random_state=42)
df_test_norm = df_norm.sample(df_anom.shape[0])
df_test = pd.concat([
    df_anom,
    df_test_norm
])
df_train = df_norm.drop(df_test_norm.index)

feature_cols = [_ for _ in df.columns if _ != 'Class']
```


```python
X_train = df_train[feature_cols]
y_train = df_train['Class'] # will not be used
X_test = df_test[feature_cols]
y_test = df_test['Class'] # for evaluation
print('''
train: [{:>8} x {:<5}]
 test: [{:>8} x {:<5}]
'''.format(*X_train.shape, *X_test.shape))
```

    
    train: [  283823 x 30   ]
     test: [     984 x 30   ]
    



```python
def sensitivity_keras(y_true, y_pred):
    """credits: https://datascience.stackexchange.com/a/40746/28592
    
    param:
    y_pred - Predicted labels
    y_true - True labels 
    Returns:
    Specificity score
    """
    neg_y_true = 1 - y_true
    neg_y_pred = 1 - y_pred
    fp = tf.keras.backend.sum(neg_y_true * y_pred)
    tn = tf.keras.backend.sum(neg_y_true * neg_y_pred)
    specificity = tn / (tn + fp + tf.keras.backend.epsilon())
    return specificity
```

### Training

We are going to define some wrappers, these classes will work as adapters in order to have an abstract implementation.


```python
class Scaled_IsolationForest(IsolationForest):
    """The purpose of this sub-class is to transform prediction values from {-1, 1} to {1,0}
    """
    def predict(self, X):
        pred = super().predict(X)
        scale_func = np.vectorize(lambda x: 1 if x == -1 else 0)
        return scale_func(pred)

class Scaled_OneClass_SVM(OneClassSVM):
    """The purpose of this sub-class is to transform prediction values from {-1, 1} to {1,0}
    """
    def predict(self, X):
        return np.array([y==-1 for y in super().predict(X)])
    
class NoveltyDetection_Sequential(tf.keras.models.Sequential):
    """This custom `tf.keras.models.Sequential` sub-class transforms autoencoder's output into {1,0}.
    Output value is determined based on reproduction (decode) loss. If reproduction loss is more than a threashold then, the input sample is considered as anomaly (outlier).
    Based on few experiments, 1.5 is a dissent threashold (don't as why :P). Future work: determine the threashold using a more sophisticated method.
    """
    def predict(self, x, *args, **kwargs):
        pred = super().predict(x, *args, **kwargs)
        mse = np.mean(np.power(x - pred, 2), axis=1)
        scale_func = np.vectorize(lambda x: 1 if x > 1.5 else 0)
        return scale_func(mse)
```


```python
# define early stop in order to prevent overfitting and useless training
early_stop = tf.keras.callbacks.EarlyStopping(
    monitor='mse',
    patience=10,
    verbose=1, 
    mode='min',
    restore_best_weights=True,
)

# it's a common practice to store the best model
checkpoint = tf.keras.callbacks.ModelCheckpoint(
    filepath='autoenc.hdf5',
    save_best_only=True,
    monitor='val_loss',
    mode='min',
    verbose=0
)

def get_autoencoder() -> tf.keras.models.Sequential:
    """Build an autoencoder
    """
    model = NoveltyDetection_Sequential([
        tf.keras.layers.Dense(X_train.shape[1], activation='relu', input_shape=(X_train.shape[1], )),
        # add some noise to prevent overfitting
        tf.keras.layers.GaussianNoise(0.05),
        tf.keras.layers.Dense(2, activation='relu'),
        tf.keras.layers.Dense(X_train.shape[1], activation='relu')
    ])
    model.compile(optimizer='adam', 
                        loss='mse',
                        metrics=['acc', sensitivity_keras])
    return model
```

The following dictionary containes the models and the parameters that we are going to use during the phase of training


```python
clfs = {
    'isolation_forest': {
        'label': 'Isolation Forest',
        'clb': Scaled_IsolationForest,
        'params': {
            'contamination': 'auto',
            'n_estimators': 300
        },
        'predictions': None,
        'model': None
    },
    'ocsvm': {
        'label': 'OneClass SVM',
        'clb': Scaled_OneClass_SVM,
        'params': {
            'kernel': 'rbf',
            'gamma': 0.3,
            'nu': 0.01,
        },
        'prediction': None,
        'model': None
    },
    'auto-encoder': {
        'label': 'Autoncoder',
        'clb': get_autoencoder,
        'params': {},
        'fit_params': {
            'x': X_train, 'y': X_train,
            'validation_split': 0.2,
            'callbacks': [early_stop, checkpoint],
            'epochs': 64,
            'batch_size': 256,
            'verbose': 0
        },
        'predictions': None,
        'model': None
    }
}
```


```python
%%time

t = trange(len(clfs))
for name in clfs:
    t.set_description(clfs[name]['label'])
    clfs[name]['model'] = clfs[name]['clb'](**clfs[name]['params'])
    if 'fit_params' in clfs[name]:
        clfs[name]['model'].fit(**clfs[name].get('fit_params', {}))
    else:
        clfs[name]['model'].fit(X_train)
    clfs[name]['predictions'] = clfs[name]['model'].predict(X_test)
    t.update()
t.close()
```


    HBox(children=(FloatProgress(value=0.0, max=3.0), HTML(value='')))


    
    CPU times: user 3h 9min 26s, sys: 38.6 s, total: 3h 10min 4s
    Wall time: 3h 8min 34s



```python
def print_eval_metrics(y_true, y_pred, name='', header=True):
    """Function for printing purposes
    """
    if header:
        print('{:>20}\t{:>10}\t{:>10}\t{:>8}\t{:>5}'.format('Algorith', 'Accuracy', 'Recall', 'Precision', 'f1'))
    acc = accuracy_score(y_true, y_pred)
    recall = recall_score(y_true, y_pred)
    prec = precision_score(y_true, y_pred)
    f1 = f1_score(y_true, y_pred)
    print('{:>20}\t{:>1.8f}\t{:>1.8f}\t{:>1.6f}\t{:>1.3f}'.format(
        name, acc, recall, prec, f1
    ))
```

### Enseble


```python
y_preds = np.column_stack([clfs[_]['predictions'] for _ in clfs])
enseble_preds = []
```

#### Hard Voting
This is one of the simplest way to combine multiple models in order to generalize better and achive better performance.


```python
hard_vot = EnsembleVoteClassifier([clfs[_]['model'] for _ in clfs], fit_base_estimators=False)
hard_vot.fit(X_test, y_test)
enseble_preds.append((hard_vot.predict(X_test), 'Hard Voting'))
```

    /opt/conda/lib/python3.7/site-packages/mlxtend/classifier/ensemble_vote.py:166: UserWarning: fit_base_estimators=False enforces use_clones to be `False`
      warnings.warn("fit_base_estimators=False "


#### Weighted Hard Voting
Using weighted hard voting you can take advantage of most high-performed models


```python
wei_hard_vot = EnsembleVoteClassifier([clfs[_]['model'] for _ in clfs], weights=[
        0.4,
        0.1,
        0.8
    ], fit_base_estimators=False)
wei_hard_vot.fit(X_test, y_test)
enseble_preds.append((wei_hard_vot.predict(X_test), 'Weighted Hard Voting'))
```

    /opt/conda/lib/python3.7/site-packages/mlxtend/classifier/ensemble_vote.py:166: UserWarning: fit_base_estimators=False enforces use_clones to be `False`
      warnings.warn("fit_base_estimators=False "


#### Blending
We are going to use the the predicted values as input to another model


```python
rf = RandomForestClassifier()

x_tr_ens, x_ts_ens, y_tr_ens, y_ts_ens = train_test_split(y_preds, y_test, test_size=.5)
rf.fit(x_tr_ens, y_tr_ens)
```




    RandomForestClassifier()



### Evaluation

It's crusial to detect fraudulent transactions, therefor a significat evaluation metric could the `simplicity`. For every trained method and ensebling method the following evaluation metrics will be calculated:
 - Accuracy
 - Recall
 - Precision
 - f1 Score


```python
print_header = True
for k, v in clfs.items():
    print_eval_metrics(y_test, v['predictions'], v['label'], print_header)
    print_header = False

print('\n')

for prds, l in enseble_preds:
    print_eval_metrics(y_test, prds, l, print_header)
    print_header = False

print('\n')
    
print_eval_metrics(
    y_ts_ens,
    rf.predict(x_ts_ens),
    'Bleding using RF', False
)
```

                Algorith	  Accuracy	    Recall	Precision	   f1
        Isolation Forest	0.90040650	0.84349593	0.951835	0.894
            OneClass SVM	0.87398374	0.93699187	0.832130	0.881
              Autoncoder	0.89939024	0.87398374	0.920771	0.897
    
    
             Hard Voting	0.90548780	0.88008130	0.927195	0.903
    Weighted Hard Voting	0.89939024	0.87398374	0.920771	0.897
    
    
        Bleding using RF	0.92479675	0.90909091	0.942623	0.926


## Future Work

 - Find the auto-encoding loss threashold using a more sophisticated way
 - Test more models and different configurations

## Resources
1. Outlier Detection with One-Class SVMs [url](https://towardsdatascience.com/outlier-detection-with-one-class-svms-5403a1a1878c)
2. Niu, X., Wang, L., & Yang, X. (2019). A comparison study of credit card fraud detection: Supervised versus unsupervised. arXiv preprint arXiv:1904.10604. [url](https://arxiv.org/abs/1904.10604) [pdf](https://arxiv.org/pdf/1904.10604)
3. Benefits of Anomaly Detection Using Isolation Forests [url](https://blog.easysol.net/using-isolation-forests-anamoly-detection/)
4. scikit-learn: Voting Classifier [url](https://scikit-learn.org/stable/modules/ensemble.html#voting-classifier)
5. scikit-learn: Novelty and Outlier Detection [url](https://scikit-learn.org/stable/modules/outlier_detection.html#outlier-detection)
6. Building Autoencoders in Keras [url](https://blog.keras.io/building-autoencoders-in-keras.html)
7. Goodfellow, Ian, Yoshua Bengio, and Aaron Courville. Deep learning. MIT press, 2016. [url](https://www.deeplearningbook.org/)
8. Porwal, Utkarsh, and Smruthi Mukund. "Credit card fraud detection in e-commerce: An outlier detection approach." arXiv preprint arXiv:1811.02196 (2018). [url](https://arxiv.org/abs/1811.02196)
