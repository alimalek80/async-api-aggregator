# Async API Aggregator

A small Django project built to answer one question with real numbers instead of theory: how much faster is `async`/`await` compared to synchronous code when a backend has to call multiple external APIs?

## The experiment

Both endpoints below call the same 5 external URLs (`httpbin.org/delay/1`, each artificially delayed by 1 second to simulate a real network round trip). The only thing that changes is how the requests are made.

| Endpoint | Method | Library | Result |
|---|---|---|---|
| `GET /api/sync/` | One request after another | `requests` | **8.57 seconds** |
| `GET /api/async/` | All requests concurrently | `httpx` + `asyncio.gather` | **2.62 seconds** |

That's roughly a **3.3x speedup**, with no change to the number of requests, only to whether the code waits around between them.

## Why this matters

Most backend code spends most of its time waiting, not computing: waiting on an external API, a database, a file. Synchronous code blocks the whole thread during that wait. Async code hands control back to the event loop instead, so it can start the next request while the first one is still in flight.

This is the exact pattern behind things like calling multiple third-party services in one request, fetching data from several sources for a dashboard, or running many independent I/O tasks in parallel.

## A limitation worth knowing

Django REST Framework does not yet fully support async views. The sync endpoint here is a normal DRF `APIView`. For the async endpoint, this project drops down to a plain Django function-based view with `async def`, because DRF's `APIView.dispatch()` is still synchronous under the hood.

This is one of the reasons frameworks like FastAPI have gained popularity: they were designed async-first, so this workaround isn't necessary. A FastAPI version of this same benchmark is planned as a follow-up.

## Project structure

```
async-api-aggregator/
├── config/          # Django project settings and root urls
├── benchmark/        # The app with both endpoints
│   ├── views.py       # SyncBenchmarkView + async_benchmark
│   └── urls.py
└── manage.py
```

## Running it locally

```bash
git clone https://github.com/alimalek80/async-api-aggregator.git
cd async-api-aggregator

python -m venv venv
venv\Scripts\Activate.ps1        # Windows PowerShell
# source venv/bin/activate       # macOS/Linux

pip install django djangorestframework httpx requests

python manage.py migrate
python manage.py runserver
```

Then hit the two endpoints and compare:

```
http://127.0.0.1:8000/api/sync/
http://127.0.0.1:8000/api/async/
```

## Stack

- Django 5
- Django REST Framework
- httpx (async HTTP client)
- requests (sync HTTP client)

## What's next

- A FastAPI version of the same benchmark, to compare an async-first framework against Django's async workaround.
- Possibly a version that benchmarks concurrent database queries instead of HTTP calls.
