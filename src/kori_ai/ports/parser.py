from typing import Protocol

from kori_ai.contracts.parse import ParseRequest, ParseResult


class ExpenseParser(Protocol):
    """Turns one line of free text into a proposal. Implementations must not write anything."""

    def parse(self, request: ParseRequest) -> ParseResult: ...
