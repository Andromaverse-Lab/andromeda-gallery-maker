###
FROM python:3.10 as poetry_builder

ENV PATH="/root/.local/bin:$PATH"
ENV POETRY_VIRTUALENVS_CREATE=false

RUN curl -sSL https://install.python-poetry.org | python -

###
FROM poetry_builder as builder

# Install imagemagick
RUN apt update \
    && apt install -y \
         imagemagick  

WORKDIR /gallerymaker
COPY images/ images/
COPY pyproject.toml .
COPY dependencies/ dependencies/
RUN poetry lock \
    && poetry install --no-dev

COPY gallerymaker/ gallerymaker/

ENTRYPOINT [ "python", "-m", "gallerymaker" ]
