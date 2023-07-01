# README

This is a script that downloads metadata from youtube. More precicely: In `youtube_analyzer/channels_to_parse.json` is a list of users specified. For each user the metadatas of the last 50 videos are downloaded and stored in a json file. By repeatedly applying the script, time series information can be obtained. These time series are to be analyzed in a separate repo, which is yet to be created.

## Prerequisites

- Python 3.10 or above
- Poetry

## Install

To install all the necessary dependencies, use

```shell
poetry install
```

In the `youtube_analyzer/settings.py` there is the class `Settings`. In this class, basic settings such as the storage location of the heating data are defined. In addition, a file named `credentials.env` must be created in `youtube_analyzer/`. This file must define these variables, which have no default value in `settings.py`. For the creation of youtube credentials, please refer to this [website](https://developers.google.com/youtube/v3?hl=en).

If the script encounters an error, an email is sent. It is tested with Apple icloud, with other email providers probably minor changes will be necessary. If icloud is to be used, it is recommended to create an app [specific password](https://support.apple.com/en-us/HT204397).

## Usage

Start the script with

```shell
poetry run python heizung_viewer/main.py
```

## Commit

Before committing, make sure that the following commands do not return errors:

```shell
poetry run isort .
poetry run black .
poetry run pyflakes .
poetry run pylint .
poetry run mypy .
poetry run pytest
```

## Usefull links

Collection of useful links:

[APIs und Dienste - Console](https://console.cloud.google.com/apis/dashboard?hl=de&project=stone-anvil-369816)

[YouTube Data API (v3) – Kontingentrechner](https://developers.google.com/youtube/v3/determine_quota_cost?hl=de)

[YouTube Channel ID Finder](https://www.streamweasels.com/tools/youtube-channel-id-and-user-id-convertor/)
