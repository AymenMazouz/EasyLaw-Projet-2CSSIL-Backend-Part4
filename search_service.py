from elasticsearch import Elasticsearch
from config import Config
from typing import Any, List


class SearchService:
    def __init__(self):
        self.es = Elasticsearch(
            Config.ELASTIC_HOST,
            basic_auth=("elastic", Config.ELASTIC_PASSWORD),
            verify_certs=False,
        )

    def _format_search_res(self, search_res: dict, page, per_page) -> dict:
        res: dict[str, Any] = {"data": []}
        for hit in search_res["hits"]["hits"]:
            item = hit["_source"]
            item["_id"] = hit["_id"]
            res["data"].append(item)

        res["results"] = len(res["data"])
        res["page"] = page
        res["total_results"] = search_res["hits"]["total"]["value"]
        res["has_more"] = (page * per_page) < res["total_results"]
        return res

    def supreme_court_decisions(
        self,
        search_query: str,
        page: int,
        per_page: int,
        start_date: str | None,
        end_date: str | None,
        search_field: str | None,
        subject: str | None,
        number: int | None,
        sort_by: str = "relevance",
    ):
        filters: List[dict[str, Any]] = []
        if start_date:
            filters.append({"range": {"date": {"gte": start_date}}})
        if end_date:
            filters.append({"range": {"date": {"lte": end_date}}})
        if subject:
            filters.append({"term": {"subject.keyword": {"value": subject}}})
        if number:
            filters.append({"term": {"number": {"value": number}}})

        if search_query == "":
            match_query: dict[str, Any] = {"match_all": {}}
        # search by specific field
        elif search_field:
            match_query = {"match": {search_field: search_query}}
        # multi field search
        else:
            match_query = {
                "multi_match": {
                    "query": search_query,
                    "fields": [
                        "subject",
                        "parties",
                        "keywords",
                        "reference",
                        "principle",
                        "ground_of_appeal",
                        "supreme_court_response",
                        "verdict",
                        "president",
                        "reporting_judge",
                    ],
                }
            }

        es_query = {
            "query": {
                "bool": {
                    "must": match_query,
                    "filter": filters,
                }
            },
            "from": (page - 1) * per_page,
            "size": per_page,
        }
        if sort_by == "date":
            es_query["sort"] = [{"date": {"order": "desc"}}]

        search_res = self.es.search(index="supreme-court", body=es_query)

        return self._format_search_res(search_res.body, page, per_page)

    def laws(
        self,
        search_query: str,
        page: int,
        per_page: int,
        signature_start_date: str | None,
        signature_end_date: str | None,
        journal_start_date: str | None,
        journal_end_date: str | None,
        text_type: str | None,
        text_number: str | None,
        ministry: str | None,
        field: str | None,
        sort_by: str = "relevance",
    ):

        filters: List[dict[str, Any]] = []
        if signature_start_date:
            filters.append({"range": {"signature_date": {"gte": signature_start_date}}})
        if signature_end_date:
            filters.append({"range": {"signature_date": {"lte": signature_end_date}}})
        if journal_start_date:
            filters.append({"range": {"journal_date": {"gte": journal_start_date}}})
        if journal_end_date:
            filters.append({"range": {"journal_date": {"lte": journal_end_date}}})
        if text_type:
            filters.append({"term": {"text_type": {"value": text_type}}})
        if text_number:
            filters.append({"term": {"text_number": {"value": text_number}}})
        if ministry:
            filters.append({"term": {"ministry": {"value": ministry}}})
        if field:
            filters.append({"term": {"field": {"value": field}}})

        # query
        if search_query == "":
            match_query: dict[str, Any] = {"match_all": {}}
        # multi field search
        else:
            match_query = {
                "multi_match": {
                    "query": search_query,
                    "fields": ["content^2", "long_content"],
                }
            }

        es_query = {
            "query": {
                "bool": {
                    "must": match_query,
                    "filter": filters,
                }
            },
            "from": (page - 1) * per_page,
            "size": per_page,
        }
        if sort_by == "signature_date":
            es_query["sort"] = [{"signature_date": {"order": "desc"}}]
        elif sort_by == "journal_date":
            es_query["sort"] = [{"journal_date": {"order": "desc"}}]

        search_res = self.es.search(index="laws", body=es_query)

        return self._format_search_res(search_res.body, page, per_page)

    def constitution(
        self,
        search_query: str,
        page: int,
        per_page: int,
        section_name: str | None,
        chapter_name: str | None,
        section_number: int | None,
        chapter_number: int | None,
        article_number: int | None,
    ):

        filters: List[dict[str, Any]] = []
        if section_name:
            filters.append({"term": {"section_name": {"value": section_name}}})
        if chapter_name:
            filters.append({"term": {"chapter_name": {"value": chapter_name}}})
        if section_number:
            filters.append({"term": {"section_number": {"value": section_number}}})
        if chapter_number:
            filters.append({"term": {"chapter_number": {"value": chapter_number}}})
        if article_number:
            filters.append({"term": {"article_number": {"value": article_number}}})

        if search_query == "":
            match_query: dict[str, Any] = {"match_all": {}}
        else:
            match_query = {
                "match": {
                    "article_text": search_query,
                }
            }

        es_query = {
            "query": {
                "bool": {
                    "must": match_query,
                    "filter": filters,
                }
            },
            "from": (page - 1) * per_page,
            "size": per_page,
        }
        search_res = self.es.search(index="dostor", body=es_query)

        return self._format_search_res(search_res.body, page, per_page)

    def conseil(
        self,
        search_query: str,
        page: int,
        per_page: int,
        number: int | None,
        chamber: str | None,
        section: str | None,
        procedure: str | None,
        start_date: str | None,
        end_date: str | None,
        sort_by: str = "relevance",
    ):
        filters: List[dict[str, Any]] = []
        if number:
            filters.append({"term": {"number": {"value": number}}})
        if chamber:
            filters.append({"term": {"chamber": {"value": chamber}}})
        if section:
            filters.append({"term": {"section": {"value": section}}})
        if procedure:
            filters.append({"term": {"procedure": {"value": procedure}}})
        if start_date:
            filters.append({"range": {"date": {"gte": start_date}}})
        if end_date:
            filters.append({"range": {"date": {"lte": end_date}}})

        if search_query == "":
            match_query: dict[str, Any] = {"match_all": {}}
        else:
            match_query = {
                "multi_match": {
                    "query": search_query,
                    "fields": ["subject^2", "principle"],
                }
            }

        es_query = {
            "query": {
                "bool": {
                    "must": match_query,
                    "filter": filters,
                }
            },
            "from": (page - 1) * per_page,
            "size": per_page,
        }
        if sort_by == "date":
            es_query["sort"] = [{"date": {"order": "desc"}}]

        search_res = self.es.search(index="conseil", body=es_query)

        return self._format_search_res(search_res.body, page, per_page)
