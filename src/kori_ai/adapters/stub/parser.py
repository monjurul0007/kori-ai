from kori_ai.common.errors import NotImplementedProblem
from kori_ai.contracts.parse import ParseRequest, ParseResult


class NotImplementedParser:
    """Placeholder until the real parser lands in M4."""

    def parse(self, request: ParseRequest) -> ParseResult:
        raise NotImplementedProblem("ExpenseParser has no implementation yet (M4)")
