---
title: "OSS: Estimate and monitor the number of active users using Github Actions"
date: 2022-02-20T15:24:09+02:00
draft: false
category: posts
tags:
  - oss
  - github-actions
  - snapcraft
  - flatpak
keywords:
  - count
  - count-installations
  - github-actions
  - floss
  - oss
  - open-source

description: Track and monitor the total number of users using Github Actions.

cover:
  image: "/images/post-covers/counting.jpg"
  alt: "counting"
  caption: "Photo by [Miguel Á. Padriñán](https://www.pexels.com/@padrinan?utm_content=attributionCopyText&utm_medium=referral&utm_source=pexels) from [Pexels](https://www.pexels.com/photo/5-strike-symbol-1010973/?utm_content=attributionCopyText&utm_medium=referral&utm_source=pexels)"
  relative: false
  responsiveImages: true

---

## Context

A beta version of your awesome open-source software has been released. Great news so far. Except from introducing new features, fixing bugs and answering users' questions, it's really important to have an estimation of the total number of users. In case you are not the only user of your OSS, it's significant to monitor the active users for the following reasons:

 1. **Motivation**. Knowing that people are using you software will motivate you to keep maintaining and improving your project.
 2. **Trustworthy software**. Spreading the total number of active users indicates that your OSS is trustworthy.

So, this article is going to present a way to count active users and installations using [Github Actions](https://github.com/features/actions).

## Numerous package distributors

Nowadays, there are numerous ways to distribute your OSS. Snapcraft and Flatpak are two of the most known package management tools. Have in mind that you always have to provide the option to "Build from source" to keep your geek users happy too. In a nutshell, you have to provide various installation methods, therefore, you have to summarize active users from more than one sources.


## Count installations

So, let's dig into how to count installations and active users for each installation method.

### Kickstart script

A common way to distribute your OSS is by providing a kickstart shell script, the purpose of this script is to download, build and install the software locally. In the case of `dropboxignore`, there is a kickstart script, and the installation instructions look like:

| Method | Command                                                        |
|--------|----------------------------------------------------------------|
| curl   | <code>sudo sh -c "$(curl -fsSL https://rb.gy/12plgs)" c</code> |
| wget   | <code>sudo sh -c "$(wget -qO- https://rb.gy/12plgs)" w</code>  |

as you can see, I'm using and extra parameter at the end of each command in order to specify which lib was used to download the script (via `wget` or `curl`)

Inside the kickstart file, when installation is completed, I'm making few HTTP requests in order to count the installation process that just finished:

```shell
INSTALL_COUNT_URL="https://api.countapi.xyz/hit/dropboxignore.simakis.me"

if [ "$0" == c ]; then
  curl -s --request GET --url "${INSTALL_COUNT_URL}/wget" > /dev/null
  curl -s --request GET --url "${INSTALL_COUNT_URL}/total" > /dev/null
elif [ "$0" == w ]; then
  wget -q "${INSTALL_COUNT_URL}/curl" -O /dev/null 2> /dev/null
  wget -q "${INSTALL_COUNT_URL}/total" -O /dev/null 2> /dev/null
fi
```

[CountAPI](https://countapi.xyz/) is a simple way to store stateful information like the total number of installations. You have to create a namespace for your project, and after that, make an `GET /hit/:namespace?/:key` to increase total installations by one.

Finally, you can get the total number of installations by making an `GET /info/:namespace?/:key`. In case of `dropboxignore`:

```shell
$ MANUAL_INSTALLATIONS=$(curl -s https://api.countapi.xyz/info/dropboxignore.simakis.me/total | jq -r .value)
$ echo $MANUAL_INSTALLATIONS
12
```

At the time of writing `dropboxignore` has been installed 12 times using the kickstart.

### Snapcraft

Another common way to distribute your software is as a snap. Snapcraft provides a nice monitoring dashboard:

![Snapcraft-dashboard](/images/snapcraft-dashboard.jpg)

But in our case, this is not enough, we have to extract the raw data programmatically. For this reason we are going to use [Snapcraft](https://snapcraft.io/snapcraft) CLI and [Snapcraft Action](https://github.com/marketplace/actions/snapcraft-action)

To get snapcraft metrics, you have to export a credential file and to create a github secret using the content of the exported file:

```shell
$ snapcraft login
$ snapcraft export-login exported
```

In order to get the current total number of active user, you have to use the `snapcraft metric` command:

```shell
$ SNAP_INSTALLATIONS=$( \
  snapcraft metrics dropboxignore --name installed_base_by_channel \
                                  --start "$(date +"%Y-%m-%d" --date="yesterday")" \
                                  --end "$(date +"%Y-%m-%d" --date="yesterday")" \
                                  --format=json \
  | jq '.series[].values[]' \
  | awk '{s+=$1} END {printf "%.0f\n", s}' \
)
$ echo $SNAP_INSTALLATIONS
118
```

So, 118 users have installed `dropboxignore` using snap.

## Summarize

The easy part is to summarize user from different sources:

```shell
$ TOTAL_INSTALLATIONS=$((MANUAL_INSTALLATIONS + SNAP_INSTALLATIONS))
$ echo $TOTAL_INSTALLATIONS
130
```

130 users. I'm already boosted morally 🤣.

## Automate the boring staff using Github Actions

Finally, given that we retrieved the necessary information programmatically, we are going to create a nightly job to store active users. The wiki of the repo should be enabled, so, we will use the wiki to store the statistics.

```shell
JSON_BADGE_STRING=$(cat <<-END
{"schemaVersion": 1, "label": "installations", "message": "$TOTAL_INSTALLATIONS"}
END
)
JSON_FULL_STRING=$(cat <<-END
{"manual-installations": "$MANUAL_INSTALLATIONS", "snap-installations": "$SNAP_INSTALLATIONS", "total-installations": "$TOTAL_INSTALLATIONS"}
END
)
FILENAME="$(date +"%Y-%m-%d" --date="yesterday")-stats.json"
echo "$JSON_BADGE_STRING" > latest-stats.json
echo "$JSON_FULL_STRING" > "$FILENAME"

git add latest-stats.json
git add "$FILENAME"

if ! git diff --staged --exit-code
then
    git config --global user.email "coverage-comment-action"
    git config --global user.name "Coverage Comment Action"
    git commit -m "$(date +"%Y-%m-%d" --date="yesterday") stats"

    git push -u origin
else
    echo "No change detected, skipping."
fi
```
## Badges everywhere

There is always space for one more badge with the total number of ![installations-badge](https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Fwiki%2Fsp1thas%2Fdropboxignore%2Fstats.json)

![Badges](/images/installations-badge.jpg)

## Cronjob using Github Actions

The number of active users is updated every night using the following job:

```shell
name: Nightly stats

on:
  schedule:
    - cron: "1 1 * * *"
  workflow_dispatch:

jobs:
  stats:
    runs-on: ubuntu-latest

    steps:
      - name: Install Snapcraft
        uses: samuelmeuli/action-snapcraft@v1
        with:
          snapcraft_token: ${{ secrets.SNAPCRAFT_LOGIN_FILE }}
      - name: Install os dependencies
        run: sudo apt update && sudo apt install curl jq git
      
      - name: Create stats file
        run: sh -c "$(curl -fsSL https://raw.githubusercontent.com/sp1thas/dropboxignore/master/utils/stats.sh)" '${{ secrets.GITHUB_TOKEN }}'
```
## Next steps

 - Count manual uninstalls.
 - Count flatpak installations.

## References

 - [sp1thas/dropboxignore](https://github.com/sp1thas/dropboxignore.git)
 - [`dropboxignore/utils/stats.sh`](https://github.com/sp1thas/dropboxignore/blob/master/utils/stats.sh)
 - [`dropboxignore/.github/workflows/stats.yml`](https://github.com/sp1thas/dropboxignore/blob/master/.github/workflows/stats.yml)
 - [Snapcraft Action](https://github.com/marketplace/actions/snapcraft-action)
 - [Snapcraft](https://snapcraft.io/)
 - [CountAPI](https://countapi.xyz/)