from datetime import date

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from kori_ai.contracts.parse import (
    ParseRequest,
    ParseResult,
    ProposedTransaction,
    TransactionType,
)
from kori_ai.routes.parse import get_parser

VALID = {
    "text": "lunch 250 bkash",
    "today": "2026-09-29",
    "categories": [{"id": "c1", "name": "Food", "kind": "expense"}],
    "payment_methods": ["Cash", "bKash"],
}


class FakeParser:
    def parse(self, request: ParseRequest) -> ParseResult:
        return ParseResult(
            proposal=ProposedTransaction(
                type=TransactionType.EXPENSE,
                amount="250.00",
                occurred_on=request.today,
                category_id="c1",
                payment_method="bKash",
            ),
            confidence={"amount": 0.99},
            raw_text=request.text,
        )


def test_stub_returns_501_problem_json(client: TestClient) -> None:
    r = client.post("/v1/parse", json=VALID)
    assert r.status_code == 501
    assert r.headers["content-type"].startswith("application/problem+json")
    body = r.json()
    assert body["title"] == "Not implemented"
    assert body["detail"] == "ExpenseParser has no implementation yet (M4)"
    assert body["request_id"] == r.headers["X-Request-ID"]


@pytest.mark.parametrize(
    "patch",
    [
        {"text": ""},
        {"text": "   "},
        {"text": "x" * 501},
        {"today": "not-a-date"},
        {"today": "2026-02-30"},
        {"timezone": "Mars/Olympus"},
    ],
)
def test_invalid_request_is_422(client: TestClient, patch: dict[str, str]) -> None:
    r = client.post("/v1/parse", json={**VALID, **patch})
    assert r.status_code == 422
    assert r.headers["content-type"].startswith("application/problem+json")
    assert r.json()["errors"]


def test_boundary_text_length_is_accepted(client: TestClient) -> None:
    assert client.post("/v1/parse", json={**VALID, "text": "x" * 500}).status_code == 501


def test_timezone_defaults_to_dhaka() -> None:
    req = ParseRequest(text="tea 20", today=date(2026, 9, 29))
    assert req.timezone == "Asia/Dhaka"


def test_fake_parser_override_returns_proposal(app: FastAPI, client: TestClient) -> None:
    app.dependency_overrides[get_parser] = FakeParser
    r = client.post("/v1/parse", json=VALID)
    assert r.status_code == 200
    body = r.json()
    assert body["proposal"] == {
        "type": "expense",
        "amount": "250.00",
        "occurred_on": "2026-09-29",
        "category_id": "c1",
        "merchant": None,
        "note": None,
        "payment_method": "bKash",
        "tags": [],
    }
    assert body["confidence"] == {"amount": 0.99}
    assert body["missing_fields"] == []
    assert body["raw_text"] == "lunch 250 bkash"


@pytest.mark.parametrize("amount", ["250.999", "-5", "0", "0.00", "1e3", "abc", "250.5.1", ""])
def test_amount_must_be_positive_taka_decimal(amount: str) -> None:
    with pytest.raises(ValueError, match="amount"):
        ProposedTransaction(type=TransactionType.EXPENSE, amount=amount, occurred_on=date.today())


@pytest.mark.parametrize("amount", ["250", "1250.5", "1250.50"])
def test_valid_amounts(amount: str) -> None:
    p = ProposedTransaction(type=TransactionType.EXPENSE, amount=amount, occurred_on=date.today())
    assert p.amount == amount


def test_confidence_out_of_range_rejected() -> None:
    with pytest.raises(ValueError, match="confidence"):
        ParseResult(
            proposal=ProposedTransaction(
                type=TransactionType.EXPENSE, amount="1", occurred_on=date.today()
            ),
            confidence={"amount": 1.5},
            raw_text="x",
        )
