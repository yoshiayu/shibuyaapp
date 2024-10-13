from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("events.urls")),  # eventsアプリのURLをインクルード
    path(
        "accounts/", include("django.contrib.auth.urls")
    ),  # ログイン・ログアウト用URLの追加
]
