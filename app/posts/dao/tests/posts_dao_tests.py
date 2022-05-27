from sqlite3 import paramstyle
import pytest
from app.posts.dao.posts_dao import PostsDAO


class TestPostsDao:

    @pytest.fixture
    def posts_dao(self):
        return PostsDAO ("data/posts.json")

    @pytest.fixture
    def keys_expected (self):
        return {"poster_name","poster_avatar","pic","content","views_count","likes_count","pk"}

    def test_get_all_check_type (self, posts_dao):
        posts = posts_dao.get_all()
        assert type(posts) == list, "Список постов должен быть списком"
        assert type (posts[0]) == dict, "Каждый посто должен быть словарем"

    def teat_get_all_has_key (self,posts_dao,keys_expected):
        posts = posts_dao.get_all()
        first_post = posts[0] 
        ferst_post_keys = set(first_post.keys())
        assert ferst_post_keys == keys_expected, "Полученные ключи не верны"

    def test_get_one_check_type (self, posts_dao):
        post = posts_dao.get_by_pk(1)
        assert type (post) == dict, "Каждый посто должен быть словарем"
    
    def test_get_one_has_key(self, posts_dao,keys_expected):
        post = posts_dao.get_by_pk(1)
        post_keys = set(post.keys())
        assert post_keys == keys_expected, "Полученные ключи не верны"
    
    parameters_to_by_pk = [1,2,3,4,5,6,7,8]
    @pytest.mark.parametrize("post_pk", parameters_to_by_pk)
    def test_get_one_check_type_has_correct_pk (self, posts_dao,post_pk):
        post = posts_dao.get_by_pk(post_pk)
        assert post["pk"] == post_pk, "Номер полученного поста не соответствует номеру запрошенного"


    parameters_by_user = [("Leo",{1, 5}), ("larry",{4, 8}), ("hank", {3, 7})]
    @pytest.mark.parametrize("poster_name", "post_pks_correct", parameters_by_user)
    def test_get_posts_by_user (self,posts_dao,poster_name,post_pks_correct):
        posts = posts_dao.get_by_user(poster_name)
        post_pks = set()
        for post in posts:
            post_pks.add(post["pk"])

        assert post_pks == post_pks_correct


    def test_search_check_type (self, posts_dao):
        posts = posts_dao.search("а")
        assert type(posts) == list, "Список постов должен быть списком"
        assert type (posts[0]) == dict, "Каждый посто должен быть словарем"


    def test_search_has_keys (self, posts_dao, keys_expected):
        post = posts_dao.search("а")[0]
        post_keys = set(post.keys())
        assert post_keys == keys_expected, "Полученные ключи не верны"

    queries_and_responses =[("еда",[1]), ("дом", [2,7,8]), ("а",list(range(1,8+1)))]
    @pytest.mark.parametrize ("query", "post_pks",queries_and_responses)
    def test_search_correct_match(self,posts_dao,query,post_pks):
        posts = posts_dao.search(query)
        pks = []
        for post in posts:
            pks.append(post["pk"])

        assert pks == post_pks, f"Неверный поиск по запросу {post_pks}"


    






