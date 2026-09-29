from typing import Annotated

from fastapi import APIRouter, Depends

from kori_ai.adapters.stub.parser import NotImplementedParser
from kori_ai.contracts.parse import ParseRequest, ParseResult
from kori_ai.ports.parser import ExpenseParser

router = APIRouter(tags=["parse"])


def get_parser() -> ExpenseParser:
    """The configured parser. Tests swap it with `app.dependency_overrides`."""
    return NotImplementedParser()


@router.post("/parse")
def parse(
    request: ParseRequest, parser: Annotated[ExpenseParser, Depends(get_parser)]
) -> ParseResult:
    return parser.parse(request)
