from django.shortcuts import render


def error_403(request, exception):
    data = {}
    return render(request, "incident/403.html", data)


def error_500(request, exception=None):
    data = {}
    return render(request, "incident/500.html", data)


def error_404(request, exception=None):
    data = {}
    return render(request, "incident/404.html", data)
