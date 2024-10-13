from django.shortcuts import render, redirect, get_object_or_404
from .models import Event, Point, Participation
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .forms import CustomUserCreationForm
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
from time import sleep
import json
from django.db.models import Q
from datetime import datetime
from django.utils import timezone
from django.http import HttpResponseBadRequest
from urllib.parse import unquote
from datetime import datetime
from django.core.paginator import Paginator


def event_detail_view(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return render(request, "event_detail.html", {"event": event})


@login_required
def my_page_view(request):
    points = Point.objects.filter(user=request.user)
    return render(request, "my_page.html", {"points": points})


def search_view(request):
    query = request.GET.get("q", "").strip()  # 検索クエリを取得
    month_query = request.GET.get("month")  # 月の検索クエリを取得

    # データベースからのイベント検索
    events = Event.objects.all()

    # イベント名でのフィルタリング（一文字でもヒットするように）
    if query:
        events = events.filter(
            Q(title__icontains=query)
            | Q(description__icontains=query)
            | Q(location__icontains=query)
        )

    # 月でのフィルタリング（開始日でフィルタリング）
    if month_query:
        events = events.filter(date__month=month_query)

    # スクレイピングイベントの処理
    url = "https://www.walkerplus.com/event_list/today/ar0313113/shibuya/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    scraped_events = []
    event_list = soup.find_all("script", type="application/ld+json")

    for script in event_list:
        try:
            event_data = json.loads(script.string.strip())
            if isinstance(event_data, list):
                for event in event_data:
                    title = event.get("name", "タイトル不明")
                    start_date = event.get("startDate", "日付不明")
                    end_date = event.get("endDate", "日付不明")
                    location = event.get("location", {}).get(
                        "addressLocality", "場所不明"
                    )

                    # startDateが正しく取得できた場合に月でフィルタリング
                    event_month = None
                    if start_date != "日付不明":
                        event_month = datetime.strptime(start_date, "%Y-%m-%d").month

                    # 月またはクエリに一致するスクレイピングイベントをフィルタリング
                    if (
                        not month_query
                        or (event_month and str(event_month) == month_query)
                    ) and (
                        not query
                        or (
                            query.lower() in title.lower()
                            or query.lower() in location.lower()
                        )
                    ):
                        scraped_events.append(
                            {
                                "title": title,
                                "startDate": start_date,
                                "endDate": end_date,
                                "location": location,
                            }
                        )
        except Exception as e:
            print(f"Error parsing event: {e}")

    # データベースのイベントとスクレイピングイベントを結合
    all_events = list(events) + scraped_events

    # 検索結果がない場合のメッセージ
    no_results_message = ""
    if not all_events:
        if query and month_query:
            no_results_message = "該当のイベントはありません。若しくは終了しました。"
        elif month_query:
            no_results_message = "該当月のイベントはありません。もしくは終了しました。"
        elif query:
            no_results_message = "該当のイベントはありません。若しくは終了しました。"

    # テンプレートに月リストとイベント、検索クエリ、メッセージを渡す
    return render(
        request,
        "search.html",
        {
            "events": all_events,
            "query": query,
            "month_query": month_query,
            "months": list(range(1, 13)),  # 1月から12月までのリスト
            "no_results_message": no_results_message,
        },
    )


def signup_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")  # 適切なリダイレクト先に変更
    else:
        form = CustomUserCreationForm()
    return render(request, "registration/signup.html", {"form": form})


def profile(request):
    return render(
        request, "registration/profile.html"
    )  # プロフィール用のテンプレートをレンダリング


@login_required
def my_page_view(request):
    points = Point.objects.filter(user=request.user, is_used=False)
    total_points = sum(point.points for point in points)  # Calculate total points
    return render(
        request, "my_page.html", {"points": points, "total_points": total_points}
    )


@login_required
def participate_in_event_with_points(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    points = Point.objects.filter(user=request.user, is_used=False)
    total_points = sum(point.points for point in points)

    # Check if the user has enough points for free participation
    if total_points >= 5000:
        for point in points:
            point.is_used = True  # Mark points as used
            point.save()
        Participation.objects.create(user=request.user, event=event)
        message = "5000ポイントを使用してイベントに無料で参加しました！"
    else:
        message = f"ポイントが不足しています。現在のポイント: {total_points}pt"

    return render(request, "event_detail.html", {"event": event, "message": message})


@login_required
def event_detail_view(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    # Check if the user has already visited this event
    if not Point.objects.filter(user=request.user, event=event, points=1).exists():
        Point.objects.create(user=request.user, event=event, points=1)
        message = "イベントを閲覧しました！1ポイント獲得！"
    else:
        message = "このイベントはすでに閲覧済みです。"

    return render(request, "event_detail.html", {"event": event, "message": message})


@login_required
def participate_in_event(request, event_id):
    if not isinstance(event_id, int):
        return HttpResponseBadRequest("Invalid event ID")
    event = get_object_or_404(Event, id=event_id)

    # Check if the user has already participated in the event
    if Participation.objects.filter(user=request.user, event=event).exists():
        message = "既にこのイベントに参加済みです。"
    else:
        Participation.objects.create(user=request.user, event=event)
        Point.objects.create(user=request.user, event=event, points=50)
        message = "イベントに参加しました！50ポイント獲得！"

    return render(request, "event_detail.html", {"event": event, "message": message})


def events_view(request):
    # Seleniumでブラウザを開く
    driver = webdriver.Chrome(
        executable_path="/path/to/chromedriver"
    )  # 適切なパスに修正
    driver.get("https://www.walkerplus.com/event_list/today/ar0313113/shibuya/")
    sleep(5)  # ページが完全に読み込まれるまで待機

    # ページのHTMLを取得して解析
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    events = []
    event_list = soup.find_all("div", class_="event-list-item")
    print(len(event_list))  # デバッグ用に取得したイベントの数を確認

    for event in event_list:
        title = event.find("h3").get_text() if event.find("h3") else "タイトル不明"
        date = (
            event.find("span", class_="date").get_text()
            if event.find("span", class_="date")
            else "日付不明"
        )
        location = (
            event.find("span", class_="location").get_text()
            if event.find("span", "location")
            else "場所不明"
        )
        events.append({"title": title, "date": date, "location": location})

    driver.quit()
    return render(request, "home.html", {"events": events})


def home_view(request):
    # 現在の月を取得
    current_month = datetime.now().strftime("%m")

    # データベースからイベントを取得
    db_events = Event.objects.all()

    # スクレイピングしたイベントを取得
    scraped_events = scrape_events()

    # データベースのイベントとスクレイピングしたイベントを統合
    all_events = list(db_events) + scraped_events

    # Paginatorで全てのイベントを6件ずつに分割
    paginator = Paginator(all_events, 6)
    page_number = request.GET.get("page")  # ページ番号を取得
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "home.html",
        {
            "page_obj": page_obj,  # ページ分割されたイベント
            "current_month": current_month,  # 現在の月
        },
    )


def scrape_events():
    url = "https://www.walkerplus.com/event_list/today/ar0313113/shibuya/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    events = []
    event_list = soup.find_all("script", type="application/ld+json")

    for script in event_list:
        try:
            event_data = json.loads(script.string.strip())

            if isinstance(event_data, list):
                for event in event_data:
                    title = event.get("name", "タイトル不明")
                    start_date = event.get("startDate", "日付不明")
                    end_date = event.get("endDate", "日付不明")
                    image = event.get("image", "画像なし")
                    telephone = event.get("telephone", "電話番号不明")
                    event_url = event.get("url", "#")  # URLを取得

                    # URLが空でないかチェック
                    if not event_url or event_url == "#":
                        print(f"Event URL missing for {title}")
                        event_url = "#"

                    events.append(
                        {
                            "title": title,
                            "startDate": start_date,
                            "endDate": end_date,
                            "location": event.get("location", {}).get(
                                "addressLocality", "場所不明"
                            ),
                            "image": image,
                            "telephone": telephone,
                            "url": event_url,
                        }
                    )
        except Exception as e:
            print(f"Error parsing event: {e}")

    return events


@login_required
def scraped_event_viewed(request, event_title):
    decoded_event_title = unquote(event_title)
    redirect_url = request.GET.get("redirect_url")

    # リダイレクトURLが無効でないか確認
    if not redirect_url or redirect_url == "":
        return HttpResponseBadRequest("リダイレクトURLが見つかりません。")

    # ポイント付与処理
    if not Point.objects.filter(
        user=request.user, event_title=decoded_event_title, points=1
    ).exists():
        Point.objects.create(
            user=request.user, event_title=decoded_event_title, points=1
        )
        message = "1ポイント獲得しました！"
    else:
        message = "既にこのイベントは閲覧済みです。"

    return redirect(redirect_url)
