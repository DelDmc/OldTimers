import requests
from django.http import HttpResponse

from mongoblog.models import Blog, Entry


def get_random_text(text):
    r = requests.post(
        "https://api.deepai.org/api/text-generator",
        data={
            "text": text,
        },
        headers={"api-key": "1cc93b29-9333-4ead-a990-da64dbbdf338"},
    )
    text = r.json()["output"]
    return text


def create_in_mongo(request):
    text = "random text"
    saved = Entry(
        blog=[Blog(name="MongoBlog", text=get_random_text(text))], headline="Very interesting random text"
    ).save()

    return HttpResponse(f"Done: {saved}")


def all_entries(request):
    blog_timestamps = list(Entry.objects.all().values_list("timestamp"))

    print(blog_timestamps)
    return HttpResponse(" | ".join([timestamp.strftime("%m-%d-%Y %H:%M:%S") for timestamp in blog_timestamps]))
