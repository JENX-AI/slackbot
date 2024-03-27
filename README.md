# slackbot

An LLM bot for integration with Slack.

![](https://img.shields.io/badge/Code-Python-informational?style=flat&logo=python&logoColor=white&color=3776AB)
![](https://img.shields.io/badge/Tool-Slack-informational?style=flat&logo=slack&logoColor=white&color=4A154B)

## Setup

`Linux` | `macOS`

```console
$ git clone git@github:jenx-ai/slackbot
$ python3 -m venv venv
$ source .venv/bin/activate
(venv)$ python3 -m pip install --upgrade pip
(venv)$ pip install .
```

`Windows`

```console
$ git clone git@github:jenx-ai/slackbot
$ cd slackbot
$ python -m venv venv
$ venv\scripts\activate
(venv)$ python -m pip install --upgrade pip
(venv)$ pip install .
```

## Operation

Run the slackbot from an active virtual environment.

`Linux` | `macOS`

```console
$ source .venv/bin/activate
(venv)$ cd src
(venv)$ python3 app.py
Bolt app is running!
```

`Windows`

```console
$ venv\scripts\activate
(venv)$ cd src
(venv)$ python app.py
Bolt app is running!
```

Stop the app with `CTRL+C`.
