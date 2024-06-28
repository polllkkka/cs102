import requests
from bs4 import BeautifulSoup


def extract_news(parser):
    """ Extract news from a given web page """
    news_list = []

    try:
        TRs = parser.body.findAll("table")[3].findAll("tr")

        for i, tr in enumerate(TRs[:-2]):
            if i % 3 == 0:
                news_list.append({})
                news_list[-1]["title"] = tr.findAll("td")[-1].a.text
                news_list[-1]["url"] = tr.findAll("td")[-1].a.get("href")

            if i % 3 == 1:
                news_list[-1]["author"] = tr.findAll("td")[1].findAll("a")[0].text
                points_str = tr.findAll("td")[1].findAll("span")[0].text
                news_list[-1]["points"] = int(points_str[: points_str.find("point") - 1])

                comments_str = tr.findAll("td")[1].findAll("a")[-1].text
                if "comment" in comments_str:
                    news_list[-1]["comments"] = int(comments_str[: comments_str.find("comment") - 1])
                else:
                    news_list[-1]["comments"] = 0

        return news_list
    except (IndexError, AttributeError):
        pass

def extract_next_page(parser):
    """ Extract next page URL """
    link_tag = parser.body.findAll("table")[2].findAll("tr")[-1].a
    if link_tag is None:
        return "front"

    return link_tag.get("href")


def get_news(url, n_pages=1):
    """ Collect news from a given web page """
    news = []
    while n_pages:
        print("Collecting data from page: {}".format(url))
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        news_list = extract_news(soup)
        next_page = extract_next_page(soup)
        url = "https://news.ycombinator.com/" + next_page
        news.extend(news_list)
        n_pages -= 1
    return news

