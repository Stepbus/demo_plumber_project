import requests

from logger_module.logger_ import logger, user_log_name
from scrapers_module.services import headers, query_newjobslist, variables_newjobslist, proxies


class NewJobSpider:
    url = "https://api/graphql"

    def __init__(self, last_id=None, key_words=None, ignore_words=None):
        self.last_id = int(last_id) if last_id else None
        self.key_words = [] if key_words is None else list(key_words)
        self.ignore_words = [] if ignore_words is None else list(ignore_words)

    def make_web_request(self):
        logger.log(user_log_name, f"Request for receiving all new clients")
        try:
            response = requests.request("POST", self.url, headers=headers,
                                        json={"query": query_newjobslist, "variables": variables_newjobslist},
                                        proxies=proxies[0], timeout=20)
            response.raise_for_status()
        except requests.exceptions.RequestException:
            raise
        work_requests_dict = response.json()
        return work_requests_dict

    def extract_all(self, last_work_requests):
        work_requests = []
        work_request_list = last_work_requests.get("data", {}).get("serviceRequestList", {}).get("edges", {})
        if work_request_list:
            for work_request in work_request_list:
                client_id = work_request.get('node').get('id')
                job_title = work_request.get('node').get('title')
                date_published = work_request.get('node').get('publishedAt')
                job_location = work_request.get('node').get('location').get("localityNode").get("name")
                work_requests.append(
                    {"client_id": client_id, "job_title": job_title, "date_published": date_published,
                     "job_location": job_location}
                )
        return work_requests

    def extraction_by_novelty(self, data):
        new_work_requests = []
        data_sort_by_date = sorted(data, key=lambda x: x["client_id"], reverse=True)
        for work_request in data_sort_by_date:
            if work_request["client_id"] == self.last_id:
                return new_work_requests
            else:
                new_work_requests.append(work_request)
        return new_work_requests

    def by_key_words(self, client):
        for word in self.key_words:
            if word.key_words.lower() in client.get("job_title").lower():
                return True

    def by_ignore_words(self, client):
        for word in self.ignore_words:
            if word.key_ignore.lower() in client.get("job_title").lower():
                return False
        return True

    def select_by_key_words(self, new_job_requests):
        selected_job_request = list(filter(self.by_key_words, new_job_requests))
        selected_job_request = list(filter(self.by_ignore_words, selected_job_request))
        return selected_job_request

    def run(self):
        result = self.make_web_request()
        all_record = self.extract_all(result)
        new_job_requests = self.extraction_by_novelty(all_record)
        result = self.select_by_key_words(new_job_requests)
        return result
