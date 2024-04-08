# slackbot

LLM bots for integration with Slack.

![](https://img.shields.io/badge/Code-Python-informational?style=flat&logo=python&logoColor=white&color=3776AB)
![](https://img.shields.io/badge/Tool-Slack-informational?style=flat&logo=slack&logoColor=white&color=4A154B)

## Contents

- [Models](#models)
- [Files](#files)
- [Development](#development)
  - [(Dev) Installation](#dev-installation)
  - [(Dev) Operation](#dev-operation)
  - [(Dev) Termination](#dev-termination)
- [Deployment](#deployment)
  - [Installation](#installation)
  - [Updates](#updates)
  - [Operation](#operation)
    - [Run once](#run-once)
    - [Run continuously](#run-continuously)
  - [Termination](#termination)

## Models

Source: [together.ai](https://docs.together.ai/docs/inference-models)

| Organization | Model Name            | Model String for API               | Context length | Type  |
| ------------ | --------------------- | ---------------------------------- | -------------- | ----- |
| 01.AI        | 01-ai Yi Chat (34B)   | zero-one-ai/Yi-34B-Chat            | 4096           | Chat  |
| Meta         | LLaMA-2 Chat (13B)    | meta-llama/Llama-2-13b-chat-hf     | 4096           | Chat  |
| mistralai    | Mistral (7B) Instruct | mistralai/Mistral-7B-Instruct-v0.1 | 8192           | Chat  |
| Stanford     | Alpaca (7B)           | togethercomputer/alpaca-7b         | 2048           | Chat  |
| Stability AI | Stable Diffusion 2.1  | stabilityai/stable-diffusion-2-1   | N/A            | Image |

## Files

- This app is run from `app.py`.
- Global variables such as LLM model types and token limits are configured in `src/config.py`.
- Model-related functions are contained in `src/llm_model.py`.
- Text-formatting functions are contained in `src/regex.py`.

## Development

### (Dev) Installation

`Linux` | `macOS`

```console
$ git clone git@github:jenx-ai/slackbot
$ python3 -m venv venv
$ source venv/bin/activate
(venv)$ python3 -m pip install --upgrade pip
(venv)$ python3 -m pip install -r requirements.txt
```

`Windows`

Note that the virtual machine in deployment use `Linux`. These `Windows` instructions are provided for development on local machines only.

```console
$ git clone git@github:jenx-ai/slackbot
$ cd slackbot
$ python -m venv venv
$ venv\scripts\activate
(venv)$ python -m pip install --upgrade pip
(venv)$ python -m pip install -r requirements.txt
```

### (Dev) Operation

Run the slackbot from an active virtual environment.

`Linux` | `macOS`

```console
$ source venv/bin/activate
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

### (Dev) Termination

Stop the app with `CTRL+C`.

## Deployment

`slackbot` is deployed on an `AWS EC2` instance named `slackbot-vm-medium-01`.

The virtual machine (`vm`) uses `Linux` and runs `Python 3.9` as the system python. `uv` is installed system-wide as a `pip` alternative.

The `vm` uses `SSH` keys for authorisation with the `JENX-AI` `GitHub` repository. The relevant files are `id_rsa` and `id_rsa.pub`, located in the `vm`'s `~/.ssh` directory. These files will be accessed automatically when attempting to interact with `GitHub`; the user will need to provide the `SSH` key password to perform operations such as cloning or fetching from the remote repository.

Push operations have not been authorised - changes to a repository on `vm` cannot be pushed to overwrite the remote repository.

### Directory structure

The current structure for hosting four baseline chat models is as follows:

| Parent directory  | Model directory            | Repo directory |
| ----------------- | -------------------------- | -------------- |
| `slackbot-repos`/ |                            |                |
|                   | `alpaca-7b`                | `slackbot`     |
|                   | `Llama-2-13b-chat-hf`      | `slackbot`     |
|                   | `Mistral-7B-Instruct-v0.1` | `slackbot`     |
|                   | `Yi-34B-Chat`              | `slackbot`     |

Image models and specialised models will be added when available.

### Installation

```console
$ cd slackbot-repos
[ec2-user@ip-172-XX-XX-161~]$ cd {model-dir}
[ec2-user@ip-172-XX-XX-161~model-dir]$ git clone git@github:jenx-ai/slackbot
Cloning into 'slackbot'...
Enter passphrase for key '/home/ec2-user/.ssh/id_rsa':
```

Enter the password for the `SSH` key when prompted. If successful, a similar output to that below will display:

```console
remote: Enumerating objects: 94, done.
remote: Counting objects: 100% (31/31), done.
remote: Compressing objects: 100% (28/28), done.
remote: Total 94 (delta 4), reused 11 (delta 3), pack-reused 63
Receiving objects: 100% (94/94), 29.27 KiB | 4.88 MiB/s, done.
Resolving deltas: 100% (33/33), done.
[ec2-user@ip-172-XX-XX-161~model-dir]$ ls
slackbot
```

Create a virtual environment using `uv`, then install dependencies from `requirements.txt`.

```console
[ec2-user@ip-172-XX-XX-161~model-dir]$ cd slackbot
[ec2-user@ip-172-XX-XX-161~slackbot]$ uv venv
[ec2-user@ip-172-XX-XX-161~slackbot]$ source .venv/bin/activate
(venv)[ec2-user@ip-172-XX-XX-161~slackbot]$ uv pip install --upgrade pip
(venv)[ec2-user@ip-172-XX-XX-161~slackbot]$ uv pip install -r requirements.txt
```

Create a `.env` file with required variables. The file should be created at the top level of the `slackbot` repo directory, alongside the `src` and `venv` directories.

### Updates

Use standard `Git` commands to fetch the latest state of the remote repository or pull changes. Enter the password for the `SSH` key when prompted, as per the installation instructions.

```console
$ cd slackbot-repos
[ec2-user@ip-172-XX-XX-161~]$ cd {model-dir}
[ec2-user@ip-172-XX-XX-161~model-dir]$ cd slackbot
[ec2-user@ip-172-XX-XX-161~slackbot]$ git fetch origin main
[ec2-user@ip-172-XX-XX-161~slackbot]$ git pull origin main
```

### Operation

First navigate to the repository and activate the virtual environment, then change to the `src` directory.

```console
$ cd slackbot-repos
[ec2-user@ip-172-XX-XX-161~]$ cd {model-dir}
[ec2-user@ip-172-XX-XX-161~model-dir]$ cd slackbot
[ec2-user@ip-172-XX-XX-161~slackbot]$ source .venv/bin/activate
(venv)[ec2-user@ip-172-XX-XX-161~slackbot]$ cd src
(venv)[ec2-user@ip-172-XX-XX-161~src]$
```

#### Run once

To run the app on a one-off basis, use the same approach as on a local machine - first activate the virtual environment, then navigate to `src` and run `app.py`:

```console
(venv)[ec2-user@ip-172-XX-XX-161~src]$ python3 app.py
⚡Bolt app is running!
```

#### Run continuously

To run the app continuously so that it will remain active upon exiting the terminal, use the `nohup` (no hang-up) command:

```console
(venv)[ec2-user@ip-172-XX-XX-161~src]$ nohup python3 app.py
nohup: ignoring input and appending output to 'nohup.out'

```

If the operation is successful, the line `nohup: ignoring input and appending output to 'nohup.out'` will be output, followed by a blank line.

Close the terminal to leave the app running.

### Termination

If the app is run on a one-off basis using `python3 app.py`, stop the app with `CTRL+C`.

If the app was run using the `nohup` command, connect to a new terminal window for the `vm`.

Navigate to the location of the repository - be sure to go to the correct model version.

```console
$ cd slackbot-repos
[ec2-user@ip-172-XX-XX-161~]$ cd {model-dir}
[ec2-user@ip-172-XX-XX-161~model-dir]$ cd slackbot
```

Use the following command to view a list of live processes:

```console
[ec2-user@ip-172-XX-XX-161~slackbot]$ ps aux | grep app.py
```

The process ID (PID) numbers for each service will be listed as the first number on each line.

Note the PID for the relevant process for the model to terminate, then run:

```console
[ec2-user@ip-172-XX-XX-161~slackbot]$ kill <PID>
```
