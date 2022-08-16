#!/usr/bin/env bash

poetry run isort gallerymaker
poetry run black gallerymaker
poetry run flake8 gallerymaker
