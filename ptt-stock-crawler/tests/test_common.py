# -*- coding: utf-8 -*-
# @Author  : kelvin.chiu021@gmail.com
# @Time    : 2024/11/15 15:50
# @Desc    : public data model test code

import unittest
from common import PostContent, PostComment, PostContentDetail  # 假设你的数据类定义在一个名为 your_module.py 的文件中


class TestPostContent(unittest.TestCase):
    def test_post_content_initialization(self):
        post = PostContent(
            title="Sample Title",
            author="John Doe",
            publish_date="2023-10-01",
            detail_link="https://example.com/post"
        )
        self.assertEqual(post.title, "Sample Title")
        self.assertEqual(post.author, "John Doe")
        self.assertEqual(post.publish_date, "2023-10-01")
        self.assertEqual(post.detail_link, "https://example.com/post")

    def test_post_content_str_representation(self):
        post = PostContent(
            title="Sample Title",
            author="John Doe",
            publish_date="2023-10-01",
            detail_link="https://example.com/post"
        )
        expected_str = """
            Title: Sample Title
            User: John Doe
            Publish Date: 2023-10-01
            Detail Link: https://example.com/post
        """.strip()
        self.assertEqual(str(post).strip(), expected_str)


class TestPostComment(unittest.TestCase):
    def test_post_comment_initialization(self):
        comment = PostComment(
            comment_user_name="Jane Doe",
            comment_content="Great post!",
            comment_time="2023-10-01 12:00:00"
        )
        self.assertEqual(comment.comment_user_name, "Jane Doe")
        self.assertEqual(comment.comment_content, "Great post!")
        self.assertEqual(comment.comment_time, "2023-10-01 12:00:00")

    def test_post_comment_repr_representation(self):
        comment = PostComment(
            comment_user_name="Jane Doe",
            comment_content="Great post!",
            comment_time="2023-10-01 12:00:00"
        )
        expected_repr = ("PostComment(comment_user_name='Jane Doe', comment_content='Great post!', "
                         "comment_time='2023-10-01 12:00:00')")
        self.assertEqual(repr(comment), expected_repr)


class TestPostContentDetail(unittest.TestCase):
    def test_post_content_detail_initialization(self):
        comment1 = PostComment(
            comment_user_name="Jane Doe",
            comment_content="Great post!",
            comment_time="2023-10-01 12:00:00"
        )
        comment2 = PostComment(
            comment_user_name="Alice Smith",
            comment_content="Very informative!",
            comment_time="2023-10-01 13:00:00"
        )
        post = PostContentDetail(
            title="Sample Title",
            author="John Doe",
            publish_date="2023-10-01",
            detail_link="https://example.com/post",
            post_comments=[comment1, comment2]
        )
        self.assertEqual(post.title, "Sample Title")
        self.assertEqual(post.author, "John Doe")
        self.assertEqual(post.publish_date, "2023-10-01")
        self.assertEqual(post.detail_link, "https://example.com/post")
        self.assertEqual(post.post_comments, [comment1, comment2])

    def test_post_content_detail_str_representation(self):
        comment1 = PostComment(
            comment_user_name="Jane Doe",
            comment_content="Great post!",
            comment_time="2023-10-01 12:00:00"
        )
        comment2 = PostComment(
            comment_user_name="Alice Smith",
            comment_content="Very informative!",
            comment_time="2023-10-01 13:00:00"
        )
        post = PostContentDetail(
            title="Sample Title",
            author="John Doe",
            publish_date="2023-10-01",
            detail_link="https://example.com/post",
            post_comments=[comment1, comment2]
        )
        expected_str = """
            Title: Sample Title
            User: John Doe
            Publish Date: 2023-10-01
            Detail Link: https://example.com/post
            Comments: [PostComment(comment_user_name='Jane Doe', comment_content='Great post!', comment_time='2023-10-01 12:00:00'), PostComment(comment_user_name='Alice Smith', comment_content='Very informative!', comment_time='2023-10-01 13:00:00')]
        """.strip()
        self.assertEqual(str(post).strip(), expected_str)


if __name__ == '__main__':
    unittest.main()
