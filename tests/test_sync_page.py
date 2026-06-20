import argparse

import pytest

from scripts.sync_page import (
    make_safe_filename,
    resolve_sync_targets,
    validate_page_mapping,
)


def test_validate_page_mapping_accepts_valid_mapping() -> None:
    result = validate_page_mapping(
        {
            "sample": {
                "title": "Sample Page",
                "page_id": "page-id",
                "file": "notes/sample.md",
            }
        },
        "config/pages.json",
    )

    assert result == {
        "sample": {
            "title": "Sample Page",
            "page_id": "page-id",
            "file": "notes/sample.md",
        }
    }


def test_validate_page_mapping_uses_page_key_as_default_title() -> None:
    result = validate_page_mapping(
        {"sample": {"page_id": "page-id", "file": "notes/sample.md"}},
        "config/pages.json",
    )

    assert result["sample"]["title"] == "sample"


@pytest.mark.parametrize(
    ("page_mapping", "message"),
    [
        ({}, "비어 있습니다"),
        ({"sample": {"file": "notes/sample.md"}}, "page_id"),
        ({"sample": {"page_id": "page-id"}}, "file"),
        ({"sample": []}, "JSON object"),
    ],
)
def test_validate_page_mapping_rejects_invalid_mapping(
    page_mapping: object,
    message: str,
) -> None:
    with pytest.raises(ValueError, match=message):
        validate_page_mapping(page_mapping, "config/pages.json")


def test_resolve_sync_targets_accepts_direct_page_id_and_file() -> None:
    args = argparse.Namespace(
        all=False,
        page=None,
        page_id="page-id",
        file="notes/sample.md",
        config="config/pages.json",
    )

    assert resolve_sync_targets(args) == [("direct", "page-id", "notes/sample.md")]


def test_resolve_sync_targets_rejects_partial_direct_target() -> None:
    args = argparse.Namespace(
        all=False,
        page=None,
        page_id="page-id",
        file=None,
        config="config/pages.json",
    )

    with pytest.raises(ValueError, match="--page-id와 --file"):
        resolve_sync_targets(args)


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("Sample Page", "Sample-Page"),
        ("../bad/name", "..-bad-name"),
        ("", "notion-page"),
    ],
)
def test_make_safe_filename(value: str, expected: str) -> None:
    assert make_safe_filename(value) == expected
