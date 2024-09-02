import time

from django.http import JsonResponse
from django.core.paginator import Paginator
import json
import os
from datetime import datetime
from .movies_scrapping.movies_scrapping import scrap_movies

error = False

#uwu
def scrap_movies_script():
    try:
        with open(os.path.join(os.path.dirname(__file__), 'movies.json'), 'r+', encoding='utf-8') as file:
            data = json.load(file)
            if data["meta"]["days"][0] != datetime.date(datetime.now()).strftime("%d.%m"):

                cinemas = ["https://multikino.pl/repertuar/gdansk/","https://helios.pl/gdansk/kino"
                                                                                      "-helios-metropolia/repertuar",
                                             "https://iframe226.biletyna.pl/resize_intermediate.html?url=%2Fif"
                                             "%2Findex%2F%3Fifid%3D226&xdm_e=https%3A%2F%2Fwww.kinokameralnecafe.pl"
                                             "&xdm_c=default8285&xdm_p=1"]

                scrap_result = scrap_movies(cinemas)

                if not scrap_result:
                    while not scrap_result:
                        scrap_result = scrap_movies(cinemas)
                file.seek(0)
                file.truncate(0)
                file.seek(0)
                file.write(scrap_result)

    except Exception as err:
        error = err
        print(err)


def get_movies(request):
    try:
        with open(os.path.join(os.path.dirname(__file__), 'movies.json'), 'r', encoding='utf-8') as f:
            data = json.load(f)

            if request.method != 'GET':
                return JsonResponse({"error": "GET method required"}, status=405)
            if error:
                return JsonResponse({"error": str(error)}, status=500)

            page_number = request.GET.get('page')

            if page_number is None:
                response = {
                    "movies": data["movies"],
                    "meta": {
                        "records": len(data["movies"]),
                        "total_records": len(data["movies"]),
                    }
                }
                return JsonResponse(response, safe=False, status=200)

            paginator = Paginator(data["movies"], 10)

            page = paginator.get_page(page_number)

            response = {
                "movies": list(page.object_list),
                "meta": {
                    "page": int(page_number),
                    "total_pages": paginator.num_pages,
                    "records": len(list(page.object_list)),
                    "total_records": len(data["movies"]),
                }
            }
            return JsonResponse(response, safe=False, status=200)
    except Exception as err:
        print(err)
        return JsonResponse({"error": "Error occurred, try again later"}, status=500)


def get_meta(request):
    with open(os.path.join(os.path.dirname(__file__), 'movies.json'), 'r', encoding='utf-8') as f:
        data=json.load(f)
        if request.method != 'GET':
            return JsonResponse({"error": "GET method required"}, status=405)
        if error:
            return JsonResponse({"error": str(error)}, status=500)
        return JsonResponse(data["meta"], safe=False, status=200)
