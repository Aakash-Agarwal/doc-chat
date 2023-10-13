import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def query(request):
    # Get the query params from the request.
    query = request.GET['query']

    response = {
        "input": query,
        "output": "some response from gpt"
    }

    # Save the Post object.
    return HttpResponse(json.dumps(response), content_type="application/json")
