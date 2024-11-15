# -*- coding: utf-8 -*-
# @Author  : kelvin.chiu021@gmail.com
# @Time    : 2024/11/15 15:30
# @Desc    : public data model code

from typing import List
from dataclasses import dataclass, field, is_dataclass, asdict

from bs4 import BeautifulSoup

@dataclass
class PostContent:
    """
    Basic post content container
    """
    title: str = ""  # post title
    author: str = ""  # post author
    publish_date: str = ""  # post publish date
    detail_link: str = ""  # post detail link

    def __str__(self):
        return f"""
            Title: {self.title}
            User: {self.author}
            Publish Date: {self.publish_date}
            Detail Link: {self.detail_link}
        """


@dataclass
class PostComment:
    """
    Post comment container
    """
    comment_user_name: str = ""  # comment user name
    comment_content: str = ""  # comment content
    comment_time: str = ""  # comment time

    def __repr__(self):
        # using __repr__ instead of __str__ is to make PostContentDetail easier to call.
        return (f"PostComment(comment_user_name='{self.comment_user_name}', comment_content='{self.comment_content}', "
                f"comment_time='{self.comment_time}')")


@dataclass
class PostContentDetail(PostContent):
    """
    Post content detail container
    """
    title: str = ""  # post title
    author: str = ""  # post author
    publish_date: str = ""  # post publish date
    detail_link: str = ""  # post detail link
    content: str = ""  # post content
    post_comments: List[PostComment] = field(default_factory=list)  # post comments

    def __str__(self):
        return f"""
            Title: {self.title}
            User: {self.author}
            Publish Date: {self.publish_date}
            Detail Link: {self.detail_link}
            Content: {self.content[:10].strip()}...
            Comments: {self.post_comments}
        """


def parse_post_content(html_content: str) -> str:
    """
    Parse post content
    :param html_content: html source code content
    :return:
    """
    res_content = ""
    bs = BeautifulSoup(html_content, "lxml")
    last_content_meta_ele = bs.select("#main-content > div:nth-child(4)")[0]

    current_ele = last_content_meta_ele

    while current_ele.next_sibling:
        current_ele = current_ele.next_sibling
        if current_ele.name == "div":
            break
        res_content += current_ele.getText()

    return res_content


def dataclass_to_dict(obj):
    """
    Convert dataclass to dict
    :param obj:
    :return:
    """
    if is_dataclass(obj):
        return {k: dataclass_to_dict(v) for k, v in asdict(obj).items()}
    elif isinstance(obj, list):
        return [dataclass_to_dict(item) for item in obj]
    else:
        return obj
