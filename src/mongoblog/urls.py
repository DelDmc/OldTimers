from django.urls import path

from mongoblog.views import all_entries, create_in_mongo

app_name = "mongo"


urlpatterns = [
    path("create-mongo/", create_in_mongo, name="create_mongo"),
    path("all-entries/", all_entries, name="all_entries"),
]
