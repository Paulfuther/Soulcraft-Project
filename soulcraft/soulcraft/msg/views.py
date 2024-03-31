import json
import os

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
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
def fetch_sendgrid_stats(request):
    sg = SendGridAPIClient(os.environ.get("SENDGRID_API_KEY"))
    params = {"start_date": "2024-03-20"}

    try:
        response = sg.client.stats.get(query_params=params)
        # Assuming response.body is a byte string of JSON, decode and load it into a Python object
        stats_data = json.loads(response.body.decode("utf-8"))
        # print(stats_data)
        # Pass the 'body' part of the stats data to your template
        # Assuming stats_data['body'] is the correct path within your JSON to the data of interest
        return render(request, "msg/sendgrid_stats.html", {"stats_data": stats_data})
    except Exception as e:
        # Render an error template or respond with an error message
        return HttpResponse(f"An error occurred: {str(e)}", status=500)


@login_required
def fetch_sendgrid_messages(request):
    sg = SendGridAPIClient(os.environ.get("SENDGRID_API_KEY"))

    params = {"start_date": "2024-03-25"}

    response = sg.client.messages.get(query_params=params)
    print(response.status_code)
    print(response.body)
