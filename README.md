# Gallery Maker

This is a [Discord] bot designed to create an Andromeda Labs gallery view from tokens.

## Table of Contents

- [Setup](#setup)
  - [Create the floor channels](#create-the-floor-channels)
  - [Create a discord bot](#create-a-discord-bot)
- [Installation](#installation)
  - [Build the docker image](#build-the-docker-image)
  - [Configuration](#configuration)
  - [Run the docker image](#run-the-docker-image)
  - [Running without docker](#running-without-docker)
- [Usage](#usage)
- [Deployment](#deployemnt)
- [Donations](#donations)

## Setup

The following must be set up before you can use the bot.

### Create a discord bot

You will need to create a discord bot and invite it to your server.

1. Go to the [Discord Developer](https://discord.com/developers/applications) page
2. Click "New Application" and create a new app
3. Click on "Bot" and select "Add Bot"
4. Give your bot a username and icon (optional)
5. Click on "OAuth2" > "URL Generator"

You will want to give your bot the following permissions:

#### Scopes

- bot
- applications.commands

#### Bot Permissions

- Manage Channels
- Send Messages
- Manage Messages
- Embed Links
- Attach Files

Now copy the URL generated at the bottom and paste it in your browser to invite the bot to your server.

You will also need to know your `DISCORD_KEY` which can be found by clicking on "Bot" and selecting "Reset Token."

## Installation

### Build the docker image

You can build the docker file with the following command:

```sh
docker build -t gallerymaker:dev .
```

If you need to build a multi-platform image, you can set up a [buildx] context that supports the architectures you want and then build:

```sh
docker buildx build --push \
  --platform linux/amd64,linux/arm64 \
  -t ghcr.io/starship-ibc/gallerymaker:dev \
  .

docker pull ghcr.io/starship-ibc/gallerymaker:dev
```

> For buildx, you will need to `--push` to a registry and then pull it down because docker does not currently support loading multi-architecture images locally.

### Configuration

The following environment variables should be set:

- `DISCORD_KEY` The discord bot secret key
- `IPFS_ROOT` An optional IPFS root address. (default `https://stargaze.mypinata.cloud`)

### Run the docker image

To run the docker image with a local yaml file, you can mount it within the container:

```sh
docker run --rm gallerymaker:dev
```

### Running without docker

Alternatively, you can run the bot without using containers as well. You will need to have the following dependencies installed on your machine:

- [Python3.10](https://www.python.org/)
- [Poetry](https://python-poetry.org/docs/master/#installation)

Install the python dependencies:

```sh
poetry install
```

Run the project

```sh
poetry run python -m gallerymaker
```

## Usage

You can create new galleries using the command `/create-gallery` or you can run the system locally:

```sh
poetry run python local/create_gallery.py STARGAZE_PUNK 1 ANDROMA_PUNK 2 EGG 3 ANDROMAVERSE 4
```

> If you have a local or preferred IPFS server, you can set the `IPFS_ROOT` value.

## Deployment

This bot is designed to be deployed to [Akash], which lets you deploy containers to a decentralized cloud at a very low cost. The recommended method for deploying to Akash is to use [Akashlytics]. You will need at least 5 $AKT to create a deployment, which should be enough for the bot to run for a few months. You can also follow any of the published [Akash deployment guides].

> If you're on a computer with arm64 architecture such as M1 mac, you'll need to cross-compile with buildx as most of the Akash providers run amd64 architecture.

1. Copy `akash.yaml` to `akash-deploy.yaml`
2. Set the `DISCORD_KEY` environment variable.
3. In Akashlytics, click "CREATE DEPLOYMENT"
4. Select "From a file" and select your `akash-deploy.yaml` file
5. Give your deployment a name and click "CREATE DEPLOYMENT ➡️"

    > You will be prompted to deposit 5 $AKT to get bids on your deployment. This will be used as an escrow account and the remainder refunded when you close the deployment.

6. Click "DEPOSIT" and "Approve" to sign the transaction

    > This will transmit a **"Create Deployment"** message that initializes the escrow contract and allows you to accept bids on your deployment.

7. Select a bid and click "Accept Bid" and "Approve" to sign the transaction

    > This is a **"Create Lease"** message and reserves your compute space until you close the deployment or the assicated escrow contract runs out of funds.

It may take a few minutes your deployment to be published and get started. You should be able to see the container logs and system events.

### Closing a deployment

In order to stop spending $AKT, you will need to close your deployment which will shut down the bot and release any funds remaining in the deployment escrow account.

Click on the "•••" next to your deployment and choose "Close deloyment." You should be prompted to sign a transaction that contains the "Close deployment" message. Approve this to shut down your deployment.

## Donations

If you'd like to make a donation, you may send $STARS to the following address. If you're like to sponsor a specific issue, feel free to include it in the memo line so I know what's most important to the community.

```txt
stars1z6mj02l2s8v0vsxfsark5v7t076ds8pu9nj2fv
```

[Akash]: https://akash.network/
[Akashlytics]: https://www.akashlytics.com/
[Akash deployment guides]: https://docs.akash.network/guides
[buildx]: https://docs.docker.com/build/buildx/
[Discord]: https://discord.com/
[Andromeda Labs]: https://twitter.com/AndromaverseLab
[stargaze-utils]: https://github.com/starship-ibc/stargaze-utils
[/examples/get_collection_info.py]: https://github.com/starship-ibc/stargaze-utils/blob/main/examples/get_collection_info.py
[/examples/get_new_collections.py]: https://github.com/starship-ibc/stargaze-utils/blob/main/examples/get_new_collections.py
