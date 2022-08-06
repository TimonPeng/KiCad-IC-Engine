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

        results = []

        for index, result in enumerate(data.get("result", [])):
            title = result.get("display_title")

            footprint = result.get("footprint", {})
            footprint_title = footprint.get("display_title")

            symbol = result.get("symbol", {})
            symbol_title = symbol.get("display_title")

            attributes = result.get("attributes", {})
            value = attributes.get("Value")
            supplier_part = attributes.get("Supplier Part")

            results.append(
                {
                    "index": index + 1,
                    "title": title,
                    "footprint_title": footprint_title,
                    "symbol_title": symbol_title,
                    "value": value,
                    "supplier_part": supplier_part,
                }
            )

        return results
