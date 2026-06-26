import asyncio
import json

from weread_exporter import utils
from weread_exporter.webpage import WeReadWebPage


def _make_detail_html(book_info, chapter_infos):
    data = {
        "reader": {
            "bookInfo": book_info,
            "chapterInfos": chapter_infos,
        }
    }
    return (
        "<html><script>window.__INITIAL_STATE__ = %s;</script></html>"
        % json.dumps(data, ensure_ascii=False)
    ).encode("utf-8")


def test_check_valid_accepts_soldout_book(monkeypatch, tmp_path):
    html = _make_detail_html(
        {
            "title": "test",
            "author": "author",
            "cover": "cover",
            "intro": "intro",
            "soldout": 1,
        },
        [],
    )

    async def fake_fetch(*args, **kwargs):
        return html

    monkeypatch.setattr(utils, "fetch", fake_fetch)
    page = WeReadWebPage("book-id", cookie_path=str(tmp_path / "cookie.txt"))
    assert asyncio.run(page.check_valid()) is True


def test_check_valid_rejects_invalid_detail_page(monkeypatch, tmp_path):
    async def fake_fetch(*args, **kwargs):
        return b"<html>not found</html>"

    monkeypatch.setattr(utils, "fetch", fake_fetch)
    page = WeReadWebPage("book-id", cookie_path=str(tmp_path / "cookie.txt"))
    assert asyncio.run(page.check_valid()) is False
