Title: Store images efficiently in scrapy using folder structure
Date: 2020-07-06 18:40
Modified: 2020-07-06 18:40
Tags: python
Category: blog
Slug: scrapy-store-images-efficiently-using-folder-structure
Author: Panagiotis Simakis
Summary: How to employ folder structure as an efficient and easy way to store large number of images using scrapy pipelines.

How to employ folder structure as an efficient and easy way to store large number of images using scrapy pipelines.

## Introduction

When it comes to image storing, a common pitfall is to save all the images in a single folder. If the number of images is less than few thousands, when, stop reading this post because you will not face any issue. On the other hand, if you are planing to store a large number of images, then consider to split them in different folders. Listing a directory will become faster, more efficient and at the end of the day, your kernel will be happier. A common pattern is to create a folder structure based on name of every file. For example, let’s say that `path/to/image/dir` will be the main directory and you want to store `imagefile.jpg`. Create folder structure based on file’s characters and save the file inside the leaf folder:

```
$ tree path/to/image/dir
path/to/image/dir
└── i
    └── m
        └── a
            └── imagefile.jpg
```

Given the following situation:

 - Folder structure’s depth is 3
 - The maximum number of images per leaf folder is 1000
 - A common hashing function is used for naming (`[a-z0-9]`)

The main folder can host up to:

![formula](https://latex.codecogs.com/png.latex?%28%2826%20+%2010%29%20%5E%203%29%20*%201000%20%5Capprox%2046M%20images)

Get your hands dirty

The purpose of this post is demonstrate an easy way to apply this methodology using `scrapy` and specificaly the `ImagePipeline`. The default behavior of `ImagePipeline` is to store all images in the same folder based on `IMAGES_STORE`‘s value in `settings.py`. We are going to make an `ImagePipeline` sub-class and we will override `file_path` and `thumb_path` methods. Please find below the full pipeline:

<script src="https://gist.github.com/sp1thas/8a05a4e2710b82e9d8e57d6153a7dd1f.js"></script>

Feel free to provide any feedback or comment and of course employ this pipeline to your project if you found it useful.

This methodology has been used in the [source code](https://github.com/sp1thas/book-depository-dataset) of [Book Depository Dataset](https://simakis.me/book-depository-dataset/).