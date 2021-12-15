from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Citation:
    citation_wos_id: str
    citation_year: int


@dataclass
class Publication:
    wos_id: str
    title: str
    authors: List[str]
    publication_source: str
    year: int
    volume: str
    issue: str
    citations: List[Citation]


@dataclass
class Author:
    author_name: str
    publications: List[Publication]


@dataclass
class Pagination:
    page: int
    totalPages: int


@dataclass
class BaseResponse:
    statusCode: int
    message: Optional[str] = None
    exceptionDetail: Optional[str] = None
    data: Optional[Author] = None
    page: Optional[Pagination] = None

    def __post_init__(self):
        if self.statusCode == 200:
            self.statusCode = "OK-200"
        elif self.statusCode == 201:
            self.statusCode = "CREATED-201"
        elif self.statusCode >= 400:
            self.statusCode = f"EX-{self.statusCode}"
