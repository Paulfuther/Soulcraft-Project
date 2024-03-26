import os
from datetime import datetime

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from sendgrid import SendGridAPIClient

from .forms import DateRangeForm


def fetch_sendgrid_events(request):
    events = None
    if request.method == "POST":
        form = DateRangeForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data["start_date"]
            end_date = form.cleaned_data["end_date"]
            # Make the API call with start_date and end_date as before
            # Assume events variable holds the fetched data
            try:
                sg = SendGridAPIClient(os.environ.get("SENDGRID_API_KEY"))
                query_params = {"query": f"date > {start_date} date < {end_date}"}
                response = sg.client.messages.search.get(query_params=query_params)
                events = response.to_dict()
            except Exception as e:
                events = {"error": str(e)}
    else:
        form = DateRangeForm()

    return render(request, "msg/events.html", {"form": form, "events": events})
