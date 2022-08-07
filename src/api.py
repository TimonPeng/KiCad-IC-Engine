from typing import Any

from aiohttp import ClientSession


class RESTfulClient:
    ENDPOINT = ""
    HEADERS = {
        "Content-Type": "application/json",
        "User-Agent": "KiCad-IC-Engine/1.0.0 (+https://github.com/TimonPeng/KiCad-IC-Engine)",
    }
    TABLE_HEADERS = {}

    @classmethod
    def get(cls, path: str, **kwargs) -> Any:
        return cls.request("get", path, **kwargs)

    @classmethod
    def post(cls, path: str, **kwargs) -> Any:
        return cls.request("post", path, **kwargs)

    @classmethod
    async def request(cls, method: str, path: str, **kwargs):
        async with ClientSession(headers=cls.HEADERS) as session:
            response = await getattr(session, method)(f"{cls.ENDPOINT}{path}", **kwargs)

            res = await response.json()

            return cls.process_data(res)

    @classmethod
    def process_data(cls, data):
        return data


class SZLCSC(RESTfulClient):
    ENDPOINT = "https://pro.lceda.cn/api"
    TABLE_HEADERS = {
        "No.": "index",
        "Device": "title",
        "Footprint": "footprint_title",
        "Symbol": "symbol_title",
        "Value": "value",
        "Supplier Part": "supplier_part",
    }

    @classmethod
    def process_data(cls, data):
        if not data.get("success") or data.get("code") != 0:
            raise Exception(data.get("message", "Fail to get data"))

        return data

    @classmethod
    async def search(cls, keyword: str):
        data = await cls.get("/szlcsc/eda/product/list", params={"wd": keyword})

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
