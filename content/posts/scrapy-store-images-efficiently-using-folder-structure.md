---
title: "Store images efficiently in scrapy using folder structure"
date: 2020-08-06T15:24:09+02:00

draft: false
mathjax: true
category: posts
tags:
 - scrapy
 - python

keywords:
 - scrapy
 - python
 - items
 - pipelines
 - image storing
 - scrapy images
 - folder structure
description: How to employ folder structure as an efficient and easy way to store large number of images using scrapy pipelines

cover:
    image: "/images/post-covers/scrapy.jpg"
    alt: "scrapy-plugin-alt"
    caption: "Archive Shelfs at Sächsisches Staatsarchiv in Dresden, Saxony, Germany -- [C M](https://unsplash.com/photos/X_j3b4rqnlk)"
    relative: false
    responsiveImages: true
---

## Introduction

### What is the problem and how deal with it

When it comes to image storing, a common pitfall is to save all the images in a single folder. If the number of images
is less than few thousands, when, stop reading this post because you will not face any issue. On the other hand, if you
are planing to store numerous images, then consider splitting them in different folders. Listing a directory will become
faster, more efficient and at the end of the day, your kernel will be happier. A common pattern is to create a folder
structure based on the name of every file. For example, let’s say that `path/to/image/dir` will be the main directory,
and you want to store `imagefile.jpg`. Create folder structure based on file’s characters and save the file inside the
leaf folder:

```shell
$ tree path/to/image/dir
path/to/image/dir
└── i
    └── m
        └── a
            └── imagefile.jpg
```

### A testcase

Given the following situation:

- Folder structure’s depth is 3
- The maximum number of images per leaf folder is 1000
- A common hashing function is used for naming (`[a-z0-9]`)

The main folder can host up to:

$$\left ( \left ( 26 + 10 \right )^3 \right ) * 1000 \approx 46 \text{ Milion images}$$

## Application

Time to get our hands dirty.

### Description

The purpose of this post is demonstrate an easy way to apply this methodology using [`scrapy`](https://scrapy.org/) and
specifically
the [`ImagePipeline`](https://docs.scrapy.org/en/latest/topics/media-pipeline.html#using-the-images-pipeline). The
default behavior of `ImagePipeline` is to store all images in the same folder based
on [`IMAGES_STORE`](https://docs.scrapy.org/en/latest/topics/media-pipeline.html#std-setting-IMAGES_STORE)‘s value
in [`settings.py`](https://docs.scrapy.org/en/latest/topics/settings.html#project-settings-module). We are going to make
an `ImagePipeline` sub-class and we will
override [`file_path`](https://docs.scrapy.org/en/latest/topics/media-pipeline.html#scrapy.pipelines.images.ImagesPipeline.file_path)
and `thumb_path` methods. Please find below the full pipeline:

### Implementation

{{< gist sp1thas 8a05a4e2710b82e9d8e57d6153a7dd1f >}}

