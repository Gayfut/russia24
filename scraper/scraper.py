"""file for control scraper and his specification"""
import asyncio
import json
import datetime
import os
from requests_html import AsyncHTMLSession
from bs4 import BeautifulSoup

from .scraper_settings import path_to_dumps


class Scraper:
    """Scraper for Russia24 site"""

    def __init__(self):
        # Session for requests
        self.session = AsyncHTMLSession()
        # Asynchronous main loop
        self.main_loop = asyncio.get_event_loop()

    def start_scraping(self):
        """start scraping and return all scraped info"""
        # main page of Russia24 for scraping
        main_page = self.session.run(self.__get_main_page)[0]
        # all elements with posts which need scrap
        all_posts_elements = self.__get_all_posts_elements(main_page)
        # all links to posts
        main_news_posts_links = self.__get_news_posts_links(main_page)
        (
            auto_posts_links,
            sport_posts_links,
            health_posts_links,
            ecology_posts_links,
            covid_posts_links,
            government_posts_links,
            opposition_posts_links,
            ru24_posts_links,
            ua24_posts_links,
            bl24_posts_links,
            life24_posts_links,
            blogs_posts_links,
            game_posts_links,
            world_posts_links,
            other_posts_links,
        ) = self.__get_links_to_all_posts(all_posts_elements)
        # all info from posts
        (
            main_news_posts_info,
            auto_posts_info,
            sport_posts_info,
            health_posts_info,
            ecology_posts_info,
            covid_posts_info,
            government_posts_info,
            opposition_posts_info,
            ru24_posts_info,
            ua24_posts_info,
            bl24_posts_info,
            life24_posts_info,
            blogs_posts_info,
            game_posts_info,
            world_posts_info,
            other_posts_info,
        ) = self.__get_all_posts_info(
            main_news_posts_links,
            auto_posts_links,
            sport_posts_links,
            health_posts_links,
            ecology_posts_links,
            covid_posts_links,
            government_posts_links,
            opposition_posts_links,
            ru24_posts_links,
            ua24_posts_links,
            bl24_posts_links,
            life24_posts_links,
            blogs_posts_links,
            game_posts_links,
            world_posts_links,
            other_posts_links,
        )
        # all info in dict format
        all_info = self.__get_info_in_dict(
            main_news_posts_info,
            auto_posts_info,
            sport_posts_info,
            health_posts_info,
            ecology_posts_info,
            covid_posts_info,
            government_posts_info,
            opposition_posts_info,
            ru24_posts_info,
            ua24_posts_info,
            bl24_posts_info,
            life24_posts_info,
            blogs_posts_info,
            game_posts_info,
            world_posts_info,
            other_posts_info,
        )

        return all_info

    async def __get_main_page(self):
        """return site main page for scraping"""
        response = await self.session.get("https://russia24.pro/")
        main_page = BeautifulSoup(response.text, "lxml")

        return main_page

    @staticmethod
    def __get_news_posts_links(main_page):
        """return links to main news posts from main page"""
        news_posts_elements1 = main_page.find_all("a", {"class": "r24_url"})
        news_posts_elements2 = main_page.find_all("a", {"class": "r24_item"})
        news_posts_elements = news_posts_elements1 + news_posts_elements2

        news_posts_links = []
        for news_post in news_posts_elements:
            link_to_post = news_post["href"]
            news_posts_links.append(link_to_post)

        return news_posts_links

    @staticmethod
    def __get_all_posts_elements(main_page):
        """return all elements of posts from main page"""
        all_posts_prev_elements = main_page.find_all("div", {"class": "s29_body"})

        all_posts_elements = []
        for prev_post_element in all_posts_prev_elements:
            post_element = prev_post_element.find_all("a")
            all_posts_elements.append(post_element)

        return all_posts_elements

    @staticmethod
    async def __get_definite_posts_links(all_posts_elements, topic):
        """return definite links to posts"""
        posts_links = []

        for posts in all_posts_elements:
            for post in posts:
                if post["href"].find(topic) != -1:
                    posts_links.append(post["href"])

        return posts_links

    async def __get_other_posts_links(self, all_posts_elements):
        """return links to other posts"""
        other_posts_links1 = await self.__get_definite_posts_links(
            all_posts_elements, "123ru"
        )
        other_posts_links2 = await self.__get_definite_posts_links(
            all_posts_elements, "29ru"
        )
        other_posts_links = other_posts_links1 + other_posts_links2

        return other_posts_links

    def __get_links_to_all_posts(self, all_posts_elements):
        """return links to all posts"""
        tasks = [
            self.__get_definite_posts_links(all_posts_elements, "auto"),
            self.__get_definite_posts_links(all_posts_elements, "sport"),
            self.__get_definite_posts_links(all_posts_elements, "health"),
            self.__get_definite_posts_links(all_posts_elements, "ecology"),
            self.__get_definite_posts_links(all_posts_elements, "covid"),
            self.__get_definite_posts_links(all_posts_elements, "putin"),
            self.__get_definite_posts_links(all_posts_elements, "navalny"),
            self.__get_definite_posts_links(all_posts_elements, "ru24"),
            self.__get_definite_posts_links(all_posts_elements, "ua24"),
            self.__get_definite_posts_links(all_posts_elements, "lukashenko"),
            self.__get_definite_posts_links(all_posts_elements, "life24"),
            self.__get_definite_posts_links(all_posts_elements, "news24"),
            self.__get_definite_posts_links(all_posts_elements, "game24"),
            self.__get_definite_posts_links(all_posts_elements, "today24"),
            self.__get_other_posts_links(all_posts_elements),
        ]

        (
            auto_posts_links,
            sport_posts_links,
            health_posts_links,
            ecology_posts_links,
            covid_posts_links,
            government_posts_links,
            opposition_posts_links,
            ru24_posts_links,
            ua24_posts_links,
            bl24_posts_links,
            life24_posts_links,
            blogs_posts_links,
            game_posts_links,
            world_posts_links,
            other_posts_links,
        ) = self.main_loop.run_until_complete(asyncio.gather(*tasks))

        return (
            auto_posts_links,
            sport_posts_links,
            health_posts_links,
            ecology_posts_links,
            covid_posts_links,
            government_posts_links,
            opposition_posts_links,
            ru24_posts_links,
            ua24_posts_links,
            bl24_posts_links,
            life24_posts_links,
            blogs_posts_links,
            game_posts_links,
            world_posts_links,
            other_posts_links,
        )

    async def __get_definite_posts_info(self, links_to_posts):
        """return info about definite posts"""
        posts_info = []
        for link_to_post in links_to_posts:
            post_info = await self.__get_post_info(link_to_post)
            posts_info.append(post_info)

        return posts_info

    async def __get_post_info(self, link_to_post):
        """return one info about definite post"""
        response = await self.session.get(link_to_post)
        page_for_scraping = BeautifulSoup(response.text, "lxml")

        try:
            title = page_for_scraping.find("h1").text
        except AttributeError:
            title = None

        try:
            description = page_for_scraping.find("div", {"class": "r24_text"}).text
        except AttributeError:
            try:
                description = page_for_scraping.find("div", {"class": "n24_text"}).text
            except AttributeError:
                try:
                    description = page_for_scraping.find_all(
                        "div", {"class": "n123_body"}
                    )[1].text
                except IndexError:
                    description = None

        try:
            post_time = page_for_scraping.find("time").text
        except AttributeError:
            post_time = None

        try:
            source = (
                page_for_scraping.find("div", {"class": "s29Source"})
                .find("a", {"class": "s29_link"})
                .text
            )
        except AttributeError:
            try:
                source = page_for_scraping.find("a", {"class": "r24SourceUrl"}).text
            except AttributeError:
                try:
                    source = page_for_scraping.find("a", {"class": "n24SourceUrl"}).text
                except AttributeError:
                    source = None

        post_info = {
            "title": title,
            "description": description,
            "source": source,
            "time": post_time,
            "link_to_post": link_to_post,
        }

        return post_info

    def __get_all_posts_info(
        self,
        main_news_posts_links,
        auto_posts_links,
        sport_posts_links,
        health_posts_links,
        ecology_posts_links,
        covid_posts_links,
        government_posts_links,
        opposition_posts_links,
        ru24_posts_links,
        ua24_posts_links,
        bl24_posts_links,
        life24_posts_links,
        blogs_posts_links,
        game_posts_links,
        world_posts_links,
        other_posts_links,
    ):
        """return all info about posts"""
        tasks = [
            self.__get_definite_posts_info(main_news_posts_links),
            self.__get_definite_posts_info(auto_posts_links),
            self.__get_definite_posts_info(sport_posts_links),
            self.__get_definite_posts_info(health_posts_links),
            self.__get_definite_posts_info(ecology_posts_links),
            self.__get_definite_posts_info(covid_posts_links),
            self.__get_definite_posts_info(government_posts_links),
            self.__get_definite_posts_info(opposition_posts_links),
            self.__get_definite_posts_info(ru24_posts_links),
            self.__get_definite_posts_info(ua24_posts_links),
            self.__get_definite_posts_info(bl24_posts_links),
            self.__get_definite_posts_info(life24_posts_links),
            self.__get_definite_posts_info(blogs_posts_links),
            self.__get_definite_posts_info(game_posts_links),
            self.__get_definite_posts_info(world_posts_links),
            self.__get_definite_posts_info(other_posts_links),
        ]

        (
            main_news_posts_info,
            auto_posts_info,
            sport_posts_info,
            health_posts_info,
            ecology_posts_info,
            covid_posts_info,
            government_posts_info,
            opposition_posts_info,
            ru24_posts_info,
            ua24_posts_info,
            bl24_posts_info,
            life24_posts_info,
            blogs_posts_info,
            game_posts_info,
            world_posts_info,
            other_posts_info,
        ) = self.main_loop.run_until_complete(asyncio.gather(*tasks))

        return (
            main_news_posts_info,
            auto_posts_info,
            sport_posts_info,
            health_posts_info,
            ecology_posts_info,
            covid_posts_info,
            government_posts_info,
            opposition_posts_info,
            ru24_posts_info,
            ua24_posts_info,
            bl24_posts_info,
            life24_posts_info,
            blogs_posts_info,
            game_posts_info,
            world_posts_info,
            other_posts_info,
        )

    @staticmethod
    def __get_info_in_dict(
        main_news_posts_info,
        auto_posts_info,
        sport_posts_info,
        health_posts_info,
        ecology_posts_info,
        covid_posts_info,
        government_posts_info,
        opposition_posts_info,
        ru24_posts_info,
        ua24_posts_info,
        bl24_posts_info,
        life24_posts_info,
        blogs_posts_info,
        game_posts_info,
        world_posts_info,
        other_posts_info,
    ):
        """return info in dict format"""
        all_info = {
            "main_news_posts": main_news_posts_info,
            "auto_posts": auto_posts_info,
            "sport_posts": sport_posts_info,
            "health_posts": health_posts_info,
            "ecology_posts": ecology_posts_info,
            "covid_posts": covid_posts_info,
            "government_posts": government_posts_info,
            "opposition_posts": opposition_posts_info,
            "ru24_posts": ru24_posts_info,
            "ua24_posts": ua24_posts_info,
            "bl24_posts": bl24_posts_info,
            "life24_posts": life24_posts_info,
            "blogs_posts": blogs_posts_info,
            "game_posts": game_posts_info,
            "world_posts": world_posts_info,
            "other_posts": other_posts_info,
        }

        return all_info

    @staticmethod
    def dump_in_json(all_info):
        """save info in json file"""
        try:
            with open(
                path_to_dumps + "/dump_" + str(datetime.datetime.now()) + ".json",
                "w",
                encoding="utf-8",
            ) as file_with_info:
                json.dump(all_info, file_with_info, ensure_ascii=False)
        except FileNotFoundError:
            os.mkdir(path_to_dumps)
            with open(
                path_to_dumps + "/dump_" + str(datetime.datetime.now()) + ".json",
                "w",
                encoding="utf-8",
            ) as file_with_info:
                json.dump(all_info, file_with_info, ensure_ascii=False)
