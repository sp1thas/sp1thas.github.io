---
title: "Separate app dependencies using Multi-stage builds"
date: 2023-05-16T15:24:09+02:00
draft: false
category: posts
tags:
  - docker
  - python
  - fastapi
  - poetry
  - dependency management
  - packaging

keywords:
  - docker
  - python
  - fastapi
  - poetry
  - dependencies management
  - packaging

description: This is a guide on how to take advantage of the docker multi-stage builds in order to separate core and dev dependencies and keep you docker images even more optimized.
cover:
    image: "/images/post-covers/separate.jpg"
    alt: "separate"
    caption: "Photo by [Will Francis](https://unsplash.com/@willfrancis?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText) on [Unsplash](https://unsplash.com/photos/Rm3nWQiDTzg?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText)"
    relative: false
    responsiveImages: true
---

## Intro

Deploying and testing a web app using docker has become the standard nowadays. Quite often, we don't pay attention on 
building more than one docker images of the service in order to use them for different scenarios. One of the most 
known use cases are the following:
 - Use the docker image to run the application.
 - Use the docker image to run the tests.

Usually, the second scenario comes with some additional dependencies, such us: testing frameworks, mocking tools and 
others. In this case, we don't want to include all these extra dependencies in the production docker image. This post 
demonstrates how [multi-stage builds][multi-stage-builds] could be used for this purpose.

## The tooling

For this demo we are going to use a pretty common set of tools in the world of python:
 - [FastAPI][fastapi] as web framework
 - [Poetry][poetry] for dependencies' management and locking
 - [pytest][pytest] as test framework
 - and ofcourse, [docker][docker] for packaging

## Project structure

We are going to keep the whole thing as minimal as possible. The project structure of our demo service looks like:

```
├── docker-compose.yml
├── Dockerfile
├── poetry.lock
├── pyproject.toml
├── README.md
├── src
│   ├── app.py
│   └── __init__.py
└── tests
    ├── __init__.py
    └── test_foo.py
```

## Multi-stage builds

In order to optimize the runtime docker image and separate the core from the dev dependencies, we are going to use
[multi-stage builds][[multi-stage-builds]:

```dockerfile
FROM python:3.10 as base

RUN pip install poetry

COPY ./ ./

FROM base as prod

RUN poetry install --without dev

EXPOSE 8000
CMD [ "poetry", "run", "uvicorn", "src.app:app" ]

FROM base as dev

RUN poetry install --with dev

CMD [ "poetry", "run", "pytest", "tests/" ]
```

Given this Dockerfile, you can specify a different target during the `docker build` in order to include or not the dev 
dependencies. [docker compose][docker-compose] will be used in order to simplify the process of build:

```yaml
version: '3.4'

services:
  api-base: &api-base
    build:
      dockerfile: Dockerfile
      context: .

  api-prod:
    <<: *api-base
    build:
      target: prod
    profiles:
      - prod

  api-tests:
    <<: *api-base
    build:
      target: dev
    profiles:
      - dev
```

Now, we can build both `api-prod` and `api-tests` services:

```shell
docker compose build
```

and run both of them:

### Server
```shell
$ docker compose run api-server
INFO:     Started server process [1]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

### Tests
```shell
$ docker compose run api-tests
============================= test session starts =============================
platform linux -- Python 3.10.10, pytest-7.2.2, pluggy-1.0.0
rootdir: /tests
plugins: anyio-3.6.2
collected 1 item                                                              

tests/test_foo.py .                                                     [100%]

============================== 1 passed in 0.00s =============================
```

and if you try to run tests using the server image, test dependencies will be missing.

```shell
$ docker compose run api-server pytest
Error response from daemon: failed to create shim task: OCI runtime create failed: runc create failed: unable to start container process: exec: "pytest": executable file not found in $PATH: unknown
```

## Conclusion

When docker is used for both deployment and ci/cd, [multi-stage builds][[multi-stage-builds]] could be really helpful because you can easily 
separate the docker images without having to maintain more than one docker files.

## References

 - [FastAPI][fastapi]
 - [Poetry][poetry]
 - [pytest][pytest]
 - [Multi-stage builds][multi-stage-builds]
 - [Docker][docker]

[fastapi]: https://fastapi.tiangolo.com "FastAPI"
[poetry]: https://python-poetry.org/ "Poetry"
[pytest]: https://docs.pytest.org/en/7.3.x/ "pytest"
[multi-stage-builds]: https://docs.docker.com/build/building/multi-stage/ "Multi-stage builds"
[docker]: https://www.docker.com/ "Docker"
[docker-compose]: https://docs.docker.com/compose/ "Docker Compose"