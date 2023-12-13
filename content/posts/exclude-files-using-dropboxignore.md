---
title: Exclude files from your dropbox easily using dropboxignore
date: 2021-01-02T15:24:09+02:00
draft: false
category: posts
tags:
  - shell
  - ignore-file
  - dropbox
keywords:
  - glob-patterns
  - dropboxignore
  - ignore-file
  - shell
  - dropbox
  - wild-card
  - floss
  - oss
  - open-source

description: it's all about the missing .dropboxignore file. This post introduces the dropboxignore, a tool  that allow you to ignore files or folder from your dropbox using patterns.

cover:
  image: "/images/post-covers/dropboxignore.jpg"
  alt: "dropboxignore-alt"
  caption: "Organized tools -- [Barn Images](https://unsplash.com/photos/t5YUoHW6zRo)"
  relative: false
  responsiveImages: true

---

## The "Problem"

A common issue/request about Dropbox was about ignoring files without using
[Selective Sync](https://help.dropbox.com/installs-integrations/sync-uploads/selective-sync-overview). Dropbox recently
[introduced](https://help.dropbox.com/files-folders/restore-delete/ignored-files) the ability to ignore specific files
or folders. Although the significance of the new feature, many users [
[1](https://stackoverflow.com/questions/52207327/implement-dropbox-gitignore),
[2](https://www.dropboxforum.com/t5/Dropbox-files-folders/dropbox-ignore-to-prevent-folders-being-uploaded-to-DropBox-like/td-p/445435)
,
[3](https://www.reddit.com/r/webdev/comments/69qnml/is_there_a_way_to_ignore_a_folder_on_dropbox/),
[4](https://news.ycombinator.com/item?id=15419715)] have expressed the importance of ignoring files from Dropbox using
[Glob](https://en.wikipedia.org/wiki/Glob_(programming)) just like `.gitignore`. For various
[reasons](https://mjtsai.com/blog/2020/01/30/dropbox-ignore-feature-in-beta/#comment-3161133) Dropbox doesn't seem to
have the will to implement such a feature :/

## The walk-around

![dropboxigno-you-fools](https://dev-to-uploads.s3.amazonaws.com/i/x0hpxonrbqemoy7lx8uo.jpg)

As a result, I decided to implement [dropboxignore](https://github.com/sp1thas/dropboxignore) which is a simple shell
script that ignores files from Dropbox based on glob patterns. Additionally, existing `.gitignore` files can be used to
automatically generate `.dropboxignore` files.

The main difference between [dropboxignore](https://github.com/sp1thas/dropboxignore) and the other relevant projects:

- [rozbb/DropboxIgnore](https://github.com/rozbb/DropboxIgnore)
- [swapagarwal/dropbox_ignore](https://github.com/swapagarwal/dropbox_ignore)
- [ridvanaltun/dropbox-ignore-anywhere](https://github.com/ridvanaltun/dropbox-ignore-anywhere)
- [MichalKarol/dropboxignore](MichalKarol/dropboxignore)
- [mweirauch/dropignore](https://github.com/mweirauch/dropignore)

is the fact that dropboxignore is implemented in shell and has the minimum requirements (`attr` package is the only
requirement)

[dropboxignore](https://github.com/sp1thas/dropboxignore) is currently available only for Mac and Linux and has various
features:

- Ignore/Revert specific files
- Automatically update `.dropboxignore`
- Revert all ignored files
- Updated `.dropboxignore` based on changes in `.gitignore` file.
- Generate `.dropboxignore` files based on existing `.gitignore` files.
- Generate, update and ignore using a single command.
- Delete all `.dropboxignore` files.

## A usecase

The simplest usage example could be this: Let's say that you want to ignore every `.txt` under your Dropbox folder, in
that case you only have to run the following command:

```shell
$ dropboxignore ignore *.txt
```

You can find more usage examples [here](https://dropboxignore.simakis.me/en/latest/getting-started/#long-story-short).
The full documentation of the project is available [here](https://dropboxignore.simakis.me/en/latest)

## Things to not expect from dropboxignore

1. **Automatically ignore new matching files.**

When a new file has been created and is matched by a `.dropboxignore` file, user should re-ignore matching files. A
cronjob could solve this drawback.

2. **Automatically detect deletions from `.gitignore` files**

Current implementation can detect and update `.dropboxignore` file if an extra pattern has been added in the
corresponding `.gitignores` but it can not handle deletions in the same way.