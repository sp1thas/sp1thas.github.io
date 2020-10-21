Title: pyclimenu
Date: 2018-03-28 18:40
Modified: 2018-03-28 18:40
Tags: python
Category: blog
Slug: pyclimenu
Author: Panagiotis Simakis
Summary: The easy way to create command line menus.

This python module creates simple command line menus. Just define the callable and the label of each option and voila! Foreground, background color numbering and labels are adjustable.

## Install

```
$ pip install git+https://github.com/sp1thas/pyclimenu.git
```

## Demo

```
>>> from pyclimenu.menu import Menu
>>> def a():
...     print('''
...     Let's Rock!
...     ''')
...     return 1
>>> mn = Menu()
>>> mn.add_item(label='The easy way', callback=a, args=())
>>> mn.add_item(label='to create', callback=a, kwargs={})
>>> mn.add_item(label='command line menus', callback=a)
>>> mn.set_colors(num_fg='cyan', num_bld=True, label_fg='blue', label_bld=True)
>>> results = mn.run(header='pyclimenu')
>>> results
1
```
