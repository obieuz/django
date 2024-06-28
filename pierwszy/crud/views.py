from django.http import JsonResponse
from django.core.paginator import Paginator
import json
import os

try:
    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(dir_path, 'cache.json')
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

except Exception as err:
    error = err


def getMovies(request):
    if request.method != 'GET':
        return JsonResponse({"error": "GET method required"}, status=405)
    if not data:
        return JsonResponse({"error": error}, status=500)

    page_number = request.GET.get('page', 1)

    movies_page_number = request.GET.get('movies_page', 1)

    paginatorCinema = Paginator(data["cinemas"], 1)

    page = paginatorCinema.get_page(page_number)

    paginatorMovies = Paginator(page.object_list[0]['movies'], 10)

    pageMovies = paginatorMovies.get_page(movies_page_number)

    print(page.object_list[0]['movies'])
    response = {
        "movies": list(pageMovies.object_list),
        "meta": {
            "page": int(movies_page_number),
            "total_pages": paginatorMovies.num_pages,
            "shownMovies": len(list(pageMovies.object_list)),
            "totalMovies": len(page.object_list[0]['movies']),
        }
    }
    return JsonResponse(response, safe=False, status=200)


def getMeta(request):
    if request.method != 'GET':
        return JsonResponse({"error": "GET method required"}, status=405)
    if not data:
        return JsonResponse({"error": error}, status=500)
    return JsonResponse(data["meta"], safe=False, status=200)
