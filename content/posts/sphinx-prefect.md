---
title: Add prefect flow visualizations into a Sphinx project
date: 2021-11-12T15:24:09+02:00
draft: false
category: posts
tags:
  - prefect
  - sphinx
keywords:
 - prefect
 - sphinx
 - documentation
 - visualization
summary: This article demonstrates an easy way to add your prefect flow visualizations into your sphinx documentation using the `sphinxcontrib-prefectviz` plugin.
---

This article demonstrates an easy way (hopefully) to add your prefect flow visualizations into your sphinx documentation using the [sphinxcontrib-prefectviz][1] plugin.

## Some context

Let's say that you have implemented some pipelines using the lovely [Prefect][2], great news so 
far, you chose a great tool to automate the boring stuff. Now it's time to document your flows, a simple way to 
have an overview of your flows is to use the [flow visualization][3].

Let's start by creating an awesome project called `example`. The only prefect flow that this project has is inside the 
`flow.py` file:

*example/flow.py:*

```python
from prefect import task, Flow, Parameter


@task
def add(a: int, b: int) -> int:
    return a + b


with Flow(name="1+1=2") as flow:
    a = Parameter(name="a", default=1)
    b = Parameter(name="b", default=1)
    add(a, b)
```

and the flow visualization looks like:

```python
flow.visualize()
```
![flow visualization][4]

Wouldn't be nice to add this visualization into your Sphinx documentation with the minimum effort?

## The Sphinx plugin

[sphinxcontrib-prefectviz][1] aims to help you to add your prefect flow 
visualizations easily into you sphinx docs. As prefect users, we really want to automate whatever is 
automatable. Given that, let's demonstrate this plugin using a simple Sphinx project.

Our awesome `example` project now looks like:

```
example
├── _build
├── conf.py
├── index.rst
├── make.bat
├── Makefile
├── _static
├── _templates
└── flow.py
```

A Sphinx project has been created in the project's root folder.

Now it's time to install the Sphinx plugin:

```shell
pip install sphinxcontrib-prefectviz
```

And add it into the Sphinx project:

```python
extensions = [ 'sphinxcontrib.prefectviz' ]
```

Last but not least, we have to ensure that `flow.py` can be imported by sphinx, to achieve such thing, we have 
to add the current path into  the `PYTHONPATH` by adding the following LOC in the very top of `conf.py`:

```python
import os
import sys
sys.path.insert(0, os.path.abspath('.'))
```

## Ready to use

Now we are ready to use the plugin. Let's add the flow visualization into the `index.rst`:

```rst
.. flowviz:: flow.flow
```

and voilà! The flow visualization appears in the index page:

![sphinx-overview][5]

## Future work

Currently, the plugin consists of a single [Sphinx directive][6], 
the goal is to add more directives in order to support more prefect-related stuff like:

 - Add flow scheduling into Sphinx using a human-friendly format

Do you have an idea on this? Feel free to [open an issue][7] to 
discuss it.

[1]: https://github.com/sphinx-contrib/prefectviz
[2]: https://www.prefect.io/
[3]: https://docs.prefect.io/core/advanced_tutorials/visualization.html
[4]: /prefect-sphinx/flow-viz.png
[5]: /prefect-sphinx/sphinx-overview.png
[6]: https://www.sphinx-doc.org/en/master/usage/restructuredtext/directives.html
[7]: https://github.com/sphinx-contrib/prefectviz/issues
