from bottle import (
    route, run, template, request, redirect
)

from scraputils import extract_news, get_news
from db import News, session
from bayes import NaiveBayesClassifier


@route("/news")
def news_list():
    s = session()
    rows = s.query(News).filter(News.label == None).all()
    return template('news_template', rows=rows)


@route("/add_label/")
def add_label():
    news_id = request.query.id
    label = request.query.label
    s = session()
    news_item = s.query(News).filter(News.id == news_id).first()
    if news_item:
        news_item.label = label
        s.commit()
        s.close()
        redirect("/news")


@route("/update")
def update_news():
    s = session()
    news = get_news("https://news.ycombinator.com/newest", 5)
    for news_item in news:
        if not s.query(News).filter(News.title == news_item['title']).first():
            new_news = News(title=news_item['title'], author=news_item['author'], url=news_item['url'])
            s.add(new_news)
    s.commit()
    s.close()
    redirect("/news")


@route("/classify")
def classify_news():
    s = session()

    labeled_news = s.query(News).filter(News.label is not None).all()
    x_train = [news.title for news in labeled_news]
    y_train = [news.label for news in labeled_news]

    model = NaiveBayesClassifier(alpha=1.0)
    model.fit(x_train, y_train)

    unlabeled_news = s.query(News).filter(News.label == None).all()
    x_test = [news.title for news in unlabeled_news]
    predictions = model.predict(x_test)

    for news, label in zip(unlabeled_news, predictions):
        news.label = label
    s.commit()
    s.close()
    redirect("/news")


@route("/recommendations")
def recommendations():
    s = session()
    _ = classify_news()
    news = s.query(News).filter(News.label is not None).all()
    first, second, third = [], [], []

    for piece in news:
        if piece.label == "good":
            first.append(piece)
        elif piece.label == "maybe":
            second.append(piece)
        elif piece.label == "never":
            third.append(piece)
    res = first + second + third

    return template("news_recommendations", rows=res)


if __name__ == "__main__":
    run(host="localhost", port=8080)

