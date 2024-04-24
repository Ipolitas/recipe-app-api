FROM python:3.9-alpine3.13
LABEL maintainer="Ipolitas"

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./app /app
WORKDIR /app
EXPOSE 8000

# single RUN for efficiency reasons
# create venv
RUN python -m venv /py && \
# upgrade pip inside venv
    /py/bin/pip install --upgrade pip && \
# install specified requirements
    /py/bin/pip install -r /tmp/requirements.txt && \
# remove "tmp" directory since we no longer need it
    rm -rf /tmp && \
# adds new user to our image (otherwise we would default to root user, and if container would become compromised - attacked would have full access to container)
    adduser \
    # no password for simplicity
        --disabled-password \
    # no home dir for this new user to save space
        --no-create-home \
    # name of new user
        django-user


# Update environment variables
# PATH - points to system PATH, so we wouldn't need to specify for each command
ENV PATH="/py/bin:$PATH"

USER django-user