from typing import Any

from aiohttp import ClientSession


class RESTfulClient:
    ENDPOINT = ""
    HEADERS = {"Content-Type": "application/json"}

    def get(self, path: str, **kwargs) -> Any:
        return self.request("get", path, **kwargs)

    def post(self, path: str, **kwargs) -> Any:
        return self.request("post", path, **kwargs)

    async def request(self, method: str, path: str, **kwargs):
        async with ClientSession(headers=self.HEADERS) as session:
            response = await getattr(session, method)(f"{self.ENDPOINT}{path}", **kwargs)

            res = await response.json()

            return self.process_data(res)

    def process_data(self, data):
        return data


class SZLCSC(RESTfulClient):
    ENDPOINT = "https://pro.lceda.cn/api"

    def process_data(self, data):
        if not data.get("success") or data.get("code") != 0:
            raise Exception(data.get("message", "Fail to get data"))

        return data

    async def search(self, keyword: str):
        data = await self.get("/szlcsc/eda/product/list", params={"wd": keyword})

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
