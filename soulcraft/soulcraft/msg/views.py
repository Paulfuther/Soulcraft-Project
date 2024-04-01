import json
import os

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from sendgrid import SendGridAPIClient

from .forms import DateRangeForm


@login_required
def fetch_sendgrid_events(request):
    events = None
    if request.method == "POST":
        form = DateRangeForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data["start_date"]
            end_date = form.cleaned_data["end_date"]
            # Make the API call with start_date and end_date as before
            # Assume events variable holds the fetched data
            params = {"start_date": "2024-03-25"}
            try:
                sg = SendGridAPIClient(os.environ.get("SENDGRID_API_KEY"))
                response = sg.client.messages.get(query_params=params)
                print(response.body)
                stats_data = json.loads(response.body.decode("utf-8"))
                print(stats_data)

            except Exception as e:
                events = {"error": str(e)}
    else:
        form = DateRangeForm()

    return render(request, "msg/events.html", {"form": form, "events": events})


@login_required
def fetch_sendgrid_messages(request):
    sg = SendGridAPIClient(os.environ.get("SENDGRID_API_KEY"))

    params = {"start_date": "2024-03-25"}

    response = sg.client.messages.get(query_params=params)
    print(response.status_code)
    print(response.body)


def tobacco_vape_compliance(request):
    return render(request, "msg/tobacco_vape_compliance.html")