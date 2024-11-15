# -*- coding: utf-8 -*-
# @Author  : kelvin.chiu021@gmail.com
# @Time    : 2024/11/15 17:00
# @Desc    : Code of synchronised crawler, target: https://www.ptt.cc/bbs/Stock/index.html,
#            extract posts and comments of first N pages

from typing import List

import requests
from bs4 import BeautifulSoup

from common import PostContent, PostComment, PostContentDetail, parse_post_content, dataclass_to_dict

FIRST_N_PAGE = 2  # extract first N page
BASE_HOST = "https://www.ptt.cc"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
}


def parse_post_use_bs(html_content: str) -> PostContent:
    """
    Using BeautifulSoup to extract post title, author, publish date based on css selector
    :param html_content: html source code content
    :return:
    """
    # initialize a post content container
    post_content = PostContent()
    # create a BeautifulSoup object
    soup = BeautifulSoup(html_content, "lxml")
    # extract title and strip the whitespace
    post_content.title = soup.select("div.r-ent div.title a")[0].text.strip() if len(
        soup.select("div.r-ent div.title a")) > 0 else ""
    # extract author
    post_content.author = soup.select("div.r-ent div.meta div.author")[0].text.strip() if len(
        soup.select("div.r-ent div.meta div.author")) > 0 else ""
    # extract publish date
    post_content.publish_date = soup.select("div.r-ent div.meta div.date")[0].text.strip() if len(
        soup.select("div.r-ent div.meta div.date")) > 0 else ""
    # extract post link
    post_content.detail_link = soup.select("div.r-ent div.title a")[0]["href"] if len(
        soup.select("div.r-ent div.title a")) > 0 else ""
    return post_content


def get_latest_page_number() -> int:
    """
    Get the latest page number
    :return:
    """
    uri = "/bbs/Stock/index.html"
    response = requests.get(url=BASE_HOST + uri, headers=HEADERS)
    if response.status_code != 200:
        raise Exception("send request got error status code, reason：", response.text)
    soup = BeautifulSoup(response.text, "lxml")

    css_selector = "#action-bar-container > div > div.btn-group.btn-group-paging > a:nth-child(2)"
    pagination_link = soup.select(css_selector)[0]["href"].strip()

    # pagination_link: /bbs/Stock/index7084.html -> 7084
    latest_page_number = int(pagination_link.replace("/bbs/Stock/index", "").replace(".html", ""))
    return latest_page_number


def fetch_bbs_posts_list(latest_number: int) -> List[PostContent]:
    """
    Fetch the note list from the latest page number to the latest page number - FIRST_N_PAGE
    :return:
    """
    posts_list: List[PostContent] = []

    # true start page number = latest page number + 1
    start_page_number = latest_number + 1
    end_page_number = start_page_number - FIRST_N_PAGE
    for page_number in range(start_page_number, end_page_number, -1):
        print(f"Start getting the list of posts on page {page_number}...")

        # assemble the uri
        uri = f"/bbs/Stock/index{page_number}.html"
        response = requests.get(url=BASE_HOST + uri, headers=HEADERS)
        if response.status_code != 200:
            print(f"Page {page_number} post fetch exception, cause: {response.text}")
            continue

        soup = BeautifulSoup(response.text, "lxml")
        all_post_elements = soup.select("div.r-ent")
        for post_element in all_post_elements:
            # using .prettify() to fetch the html content of the element
            post_content: PostContent = parse_post_use_bs(post_element.prettify())
            posts_list.append(post_content)
        print(f"End Get the list of posts on page {page_number}, this time getting :{len(all_post_elements)} posts...")
    return posts_list


def fetch_bbs_post_detail(post_content: PostContent) -> PostContentDetail:
    """
    Fetch the post detail page
    :param post_content:
    :return:
    """
    print(f"Start getting posts {post_content.detail_link} detail page ....")
    post_content_detail = PostContentDetail()

    # reuse the post_content object
    post_content_detail.title = post_content.title
    post_content_detail.author = post_content.author
    post_content_detail.detail_link = BASE_HOST + post_content.detail_link

    response = requests.get(url=BASE_HOST + post_content.detail_link, headers=HEADERS)
    if response.status_code != 200:
        print(f"Post: {post_content.title} Get Exception, Reason: {response.text}")
        return post_content_detail

    soup = BeautifulSoup(response.text, "lxml")
    post_content_detail.publish_datetime = soup.select("#main-content > div:nth-child(4) > span.article-meta-value")[
        0].text
    post_content_detail.content = parse_post_content(response.text)

    # extract all comments
    post_content_detail.post_comments = []
    all_comment_elements = soup.select("#main-content > div.push")
    for comment_element in all_comment_elements:
        post_comment = PostComment()
        if len(comment_element.select("span")) < 3:
            continue

        post_comment.comment_user_name = comment_element.select("span")[1].text.strip()
        post_comment.comment_content = comment_element.select("span")[2].text.strip().replace(": ", "")
        post_comment.comment_time = comment_element.select("span")[3].text.strip()
        post_content_detail.post_comments.append(post_comment)

    print(post_content_detail)
    return post_content_detail


def run_crawler(save_posts: List[PostContentDetail]):
    """
    Crawler main function
    :param save_posts: data container
    :return:
    """
    # step1: get the latest page number
    latest_number: int = get_latest_page_number()

    # step2: get the post list from the latest page number to the (latest page number - FIRST_N_PAGE)
    post_list: List[PostContent] = fetch_bbs_posts_list(latest_number)

    # step3: get the post detail
    for post_content in post_list:
        if not post_content.detail_link:
            continue
        post_content_detail = fetch_bbs_post_detail(post_content)
        save_posts.append(post_content_detail)

    print("Task completed, total posts: ", len(save_posts))


if __name__ == '__main__':
    all_posts_content_detail: List[PostContentDetail] = []
    run_crawler(all_posts_content_detail)

    # export the data to json
    import json
    with open("ptt_stock_posts.json", "w", encoding="utf-8") as f:
        f.write(json.dumps([dataclass_to_dict(post) for post in all_posts_content_detail], ensure_ascii=False, indent=4))
    print("Export data to ptt_stock_posts.json successfully!")
