from typing import Any

from requests import Request, Response, Session


class RESTfulAPI:
    ENDPOINT = ""

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

    def process_response(self, request: Request, response: Response):
        try:
            data = response.json()
        except ValueError:
            response.raise_for_status()
            raise
        else:
            # message: "throw unkown exceptions, Failed to get data!"
            # resultCode: "0004"
            if not data.get("success") or data.get("code") != 0:
                raise Exception(data.get("message", "Fail to get data"))

            return data

    def search(self, keyword: str):
        data = self.get("/szlcsc/eda/product/list", params={"wd": keyword})

        return data.get("result", [])
