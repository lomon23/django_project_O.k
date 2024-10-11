from http.client import responses

from django.shortcuts import render
from django.http import HttpResponse

def hello_app1(request):
    return HttpResponse("Hello World")






def hello_view(request):
    author_name = "Ostap Krochak"
    response = HttpResponse("Hello, World!")

    response.set_cookie("name", author_name)
    cookies = request.COOKIES

    if 'views' in request.session:
        request.session['views'] += 1
    else:
        request.session['views'] = 1

    views_count = request.session['views']

    response_content = f"{response.content.decode()}<br><br>"
    response_content += "Реп'яшки (cookies):<br>"
    for key, value in cookies.items():
        response_content += f"{key}: {value}<br>"
    response_content += f"<br>Кількість переглядів: {views_count}"

    response.content = response_content.encode()
    return response
