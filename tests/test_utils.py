"""Tests for utils.py"""

from datetime import datetime, timedelta
from typing import Any, Dict

import pytest

from bareutils.cookies import encode_set_cookie

from bareclient.utils import (
    NullIter,
    extract_cookies_from_response,
    gather_cookies
)


@pytest.mark.asyncio
async def test_null_iter() -> None:
    """Test for NullIter"""
    count = 0
    async for _ in NullIter():
        count += 1
    assert count == 0


def test_extract_cookies():
    """Tests for extracting cookies"""
    now = datetime(2000, 1, 1, 12, 0, 0)
    response: Dict[str, Any] = {
        'headers': [
            (
                b'set-cookie',
                encode_set_cookie(
                    b'one',
                    b'1.1',
                    max_age=timedelta(days=2)
                )
            ),
            (
                b'set-cookie',
                encode_set_cookie(
                    b'one',
                    b'1.2',
                    max_age=timedelta(days=2),
                    domain=b'example.com'
                )
            ),
            (
                b'set-cookie',
                encode_set_cookie(
                    b'one',
                    b'1.3',
                    max_age=timedelta(days=2),
                    path=b'/foo'
                )
            ),
            (
                b'set-cookie',
                encode_set_cookie(
                    b'one',
                    b'1.3',
                    max_age=timedelta(days=2),
                    domain=b'www.example.com',
                    path=b'/foo'
                )
            )
        ]
    }
    cache = extract_cookies_from_response({}, response, now)
    cookies = gather_cookies(
        cache, b'https', b'www.example.com', b'/foo', now + timedelta(days=1))
    print(cookies)
