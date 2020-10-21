Title: Weka Categorization Commands
Date: 2017-01-20 18:40
Modified: 2017-01-20 18:40
Tags: machine learning
Category: blog
Slug: weka-categorization-commands
Author: Panagiotis Simakis
Summary: Shell script to facilitate weka operations via CLI.

it’s known that WEKA crashes when the input dataset is too big. For this reason you have to run the algorithms from your terminal avoiding the GUI. Because the length of the commands is too big, I developed this script which takes as input the installation directory of WEKA, the directory of dataset and the output directory. Then a menu with available algorithms will appeared and you have to choose one. Finally when the algorithm has terminated the results is visible in the terminal.

## Built and run

```
$ git clone https://github.com/sp1thas/WEKACMDs.git && cd WEKACMDs
$ python WekaCommands.py
```

## Prerequisites

 - Python 2.7
 - termcolor
 
Installation (run as root):

```
$ pip install -r requirements.txt
```

 - WEKA [link](http://www.cs.waikato.ac.nz/ml/weka/)
 - Your dataset
 
 ## Usage
 
 ```
$ python WekaCommands.py -i <inputfile> -o <outputfile> -w <wekadirectory>
```

```

  -i, --ifile

          This is the input dataset

  -o, --ofile
          This is the output file with classification results
          (model is not contained)

  -w, --wekadir
          Direction with WEKA software

  -h,
          Prints these options
```
