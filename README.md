# slackbot

LLM bots for integration with Slack.

![](https://img.shields.io/badge/Code-Python-informational?style=flat&logo=python&logoColor=white&color=3776AB)
![](https://img.shields.io/badge/Tool-Slack-informational?style=flat&logo=slack&logoColor=white&color=4A154B)

## Contents

- [Models](#models)
- [Setup](#setup)
- [Operation](#operation)
  - [Launch the app](#launch-the-app)
  - [Terminate the app](#terminate-the-app)

## Models

Source: [together.ai](https://docs.together.ai/docs/inference-models)

| Organization | Model Name            | Model String for API               | Context length | Type  |
| ------------ | --------------------- | ---------------------------------- | -------------- | ----- |
| 01.AI        | 01-ai Yi Chat (34B)   | zero-one-ai/Yi-34B-Chat            | 4096           | Chat  |
| Meta         | LLaMA-2 Chat (13B)    | meta-llama/Llama-2-13b-chat-hf     | 4096           | Chat  |
| mistralai    | Mistral (7B) Instruct | mistralai/Mistral-7B-Instruct-v0.1 | 8192           | Chat  |
| Stanford     | Alpaca (7B)           | togethercomputer/alpaca-7b         | 2048           | Chat  |
| Stability AI | Stable Diffusion 2.1  | stabilityai/stable-diffusion-2-1   | N/A            | Image |

## Setup

`Linux` | `macOS`

```console
$ git clone git@github:jenx-ai/slackbot
$ python3 -m venv venv
$ source .venv/bin/activate
(venv)$ python3 -m pip install --upgrade pip
(venv)$ python3 -m pip install -r requirements.txt
```

`Windows`

```console
$ git clone git@github:jenx-ai/slackbot
$ cd slackbot
$ python -m venv venv
$ venv\scripts\activate
(venv)$ python -m pip install --upgrade pip
(venv)$ python -m pip install -r requirements.txt
```

## Operation

### Launch the app

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
$ venv\Scripts\activate
(venv)$ cd src
(venv)$ python app.py
Bolt app is running!
```

### Terminate the app

Stop the app with `CTRL+C`.
