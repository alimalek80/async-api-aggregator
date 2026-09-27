import time
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
import asyncio
import httpx
from django.http import JsonResponse

EXTERNAL_URLS = [
    "https://httpbin.org/delay/1",
    "https://httpbin.org/delay/1",
    "https://httpbin.org/delay/1",
    "https://httpbin.org/delay/1",
    "https://httpbin.org/delay/1",
]

class SyncBenchmarkView(APIView):
    def get(self, request):
        start = time.perf_counter()

        results = []
        for url in EXTERNAL_URLS:
            response = requests.get(url)
            results.append(response.status_code)

        elapsed = time.perf_counter() - start

        return Response({
            "mode": "sync",
            "requests_made": len(EXTERNAL_URLS),
            "status_codes": results,
            "elapsed_seconds": round(elapsed, 2),
        })

async def async_benchmark(request):
    start = time.perf_counter()

    async with httpx.AsyncClient() as client:
        tasks = [client.get(url) for url in EXTERNAL_URLS]
        responses = await asyncio.gather(*tasks)

    elapsed = time.perf_counter() - start

    return JsonResponse({
        "mode": "async",
        "requests_made": len(EXTERNAL_URLS),
        "status_codes": [r.status_code for r in responses],
        "elapsed_seconds": round(elapsed, 2),
    })
