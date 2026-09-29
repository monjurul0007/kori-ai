"""Contract for turning free text such as "lunch 250 bkash" into a proposed transaction.

The parser only ever *proposes*. Kori shows the proposal to the user, who confirms or edits it
before anything is written (see AGENTS.md: the AI never writes directly).
"""

import re
from datetime import date
from decimal import Decimal
from enum import StrEnum
from typing import Annotated
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from pydantic import BaseModel, ConfigDict, Field, field_validator

# Decimal string in taka with at most 2 decimal places (ADR-0004). Never a float.
_TAKA = re.compile(r"\d+(\.\d{1,2})?")

Confidence = Annotated[float, Field(ge=0, le=1)]


class TransactionType(StrEnum):
    EXPENSE = "expense"
    INCOME = "income"


class CategoryKind(StrEnum):
    EXPENSE = "expense"
    INCOME = "income"


class CategoryOption(BaseModel):
    """A category the user owns. The parser may only pick from the list it is given."""

    id: str = Field(description="Kori's category ID. Echo it back in `category_id` when chosen.")
    name: str = Field(description="Display name, e.g. 'Food'. Match the user's words against it.")
    kind: CategoryKind = Field(description="Whether this category is for expenses or income.")


class ParseRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    text: str = Field(
        min_length=1,
        max_length=500,
        description="The user's raw entry, e.g. 'rickshaw 60 yesterday'. Copied to `raw_text`.",
    )
    today: date = Field(
        description="The user's local calendar date. Resolve 'today', 'yesterday', 'last Friday' "
        "against this, never against the server clock."
    )
    timezone: str = Field(
        default="Asia/Dhaka",
        description="IANA time zone of the user. `occurred_on` is a date in this zone.",
    )
    categories: list[CategoryOption] = Field(
        default_factory=list,
        description="The user's categories. Choose `category_id` from these or leave it null.",
    )
    payment_methods: list[str] = Field(
        default_factory=list,
        description="Names of the user's payment methods, e.g. ['Cash', 'bKash'].",
    )

    @field_validator("text")
    @classmethod
    def _text_not_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("text must not be blank")
        return v

    @field_validator("timezone")
    @classmethod
    def _timezone_is_iana(cls, v: str) -> str:
        try:
            ZoneInfo(v)
        except (ZoneInfoNotFoundError, ValueError, OSError) as exc:
            raise ValueError(f"unknown IANA time zone: {v}") from exc
        return v


class ProposedTransaction(BaseModel):
    """What the parser thinks the user meant. Every field is optional except `type` and `amount`."""

    type: TransactionType = Field(
        description="'expense' unless the text clearly describes money received (salary, refund)."
    )
    amount: str = Field(
        description="Amount in taka as a decimal string with at most 2 decimal places, e.g. "
        "'1250.50'. Read '5k' as '5000'. Never poisha, never a float (ADR-0004)."
    )
    occurred_on: date = Field(
        description="Local calendar date of the transaction. Defaults to the request's `today`."
    )
    category_id: str | None = Field(
        default=None,
        description="ID from the request's `categories`, or null when nothing fits well.",
    )
    merchant: str | None = Field(
        default=None, description="Shop, person or service paid, e.g. 'Pathao'. Null if unstated."
    )
    note: str | None = Field(
        default=None, description="Any remaining detail worth keeping. Null if nothing is left."
    )
    payment_method: str | None = Field(
        default=None,
        description="One of the request's `payment_methods`, spelled exactly, or null.",
    )
    tags: list[str] = Field(
        default_factory=list, description="Short labels the user wrote, e.g. '#eid'. Without '#'."
    )

    @field_validator("amount")
    @classmethod
    def _amount_is_taka_decimal(cls, v: str) -> str:
        if not _TAKA.fullmatch(v) or Decimal(v) <= 0:
            raise ValueError("amount must be a positive decimal string with at most 2 places")
        return v


class ParseResult(BaseModel):
    proposal: ProposedTransaction = Field(description="The proposed transaction, to be confirmed.")
    confidence: dict[str, Confidence] = Field(
        default_factory=dict,
        description="Per-field confidence from 0 to 1, keyed by ProposedTransaction field name. "
        "Kori highlights low-confidence fields for the user to check.",
    )
    missing_fields: list[str] = Field(
        default_factory=list,
        description="Names of fields the parser could not fill and the user should supply.",
    )
    raw_text: str = Field(description="The request's `text`, unchanged.")
