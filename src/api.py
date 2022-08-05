from typing import Any

from requests import Request, Response, Session


class RESTfulAPI:
    def __init__(self) -> None:
        self.session = Session()

    def get(self, path: str, **kwargs) -> Any:
        return self.request("GET", path, **kwargs)

    def post(self, path: str, **kwargs) -> Any:
        return self.request("POST", path, **kwargs)

    def request(self, method: str, path: str, **kwargs):
        request = Request(method, f"{self.ENDPOINT}{path}", **kwargs)
        self.prepare_request(request)

        response = self.session.send(request.prepare())
        return self.process_response(request, response)

    def prepare_request(self, request: Request) -> None:
        pass

    def process_response(self, request: Request, response: Response):
        return response


class SZLCSC(RESTfulAPI):
    ENDPOINT = "https://pro.lceda.cn/api"

    def search(self):
        pass
