# Django DRF Async

[![pypi-version]][pypi]
[![Downloads](https://static.pepy.tech/badge/django-drf-async)](https://pepy.tech/project/django-drf-async)
[![build-status-image]][build-status]
[![coverage-status-image]][codecov]
[![package-status]][repo]

---

## Purpose

This package provides a way to implement asynchronous views in Django DRF.


## Installation

<div class="termy">

```console
$ pip install django-drf-async

---> 100%
```

</div>


## Example

### Create it


<div class="termy">

```console
$ django-admin startproject example
$ cd example
$ django-admin startapp example
```

</div>

## Project layout

```console

├── example
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations
│   │   └── __init__.py
│   ├── models.py
│   ├── tests.py
│   └── views.py
├── example
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py
└── requirements.txt
```


[coverage-status-image]: https://codecov.io/gh/godd0t/django-drf-async/branch/main/graph/badge.svg
[codecov]: https://codecov.io/gh/godd0t/django-drf-async
[pypi-version]: https://badge.fury.io/py/django-drf-async.svg
[pypi]: https://pypi.org/project/djangorestframework/
[build-status-image]: https://github.com/godd0t/django-drf-async/actions/workflows/ci.yml/badge.svg
[build-status]: https://github.com/godd0t/django-drf-async/actions/workflows/ci.yml
[repo]: https://github.com/godd0t/django-drf-async
[package-status]: https://img.shields.io/badge/work%20in%20progress-yellow
