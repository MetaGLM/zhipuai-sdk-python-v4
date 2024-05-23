from __future__ import annotations

from ._legacy_binary_response import HttpxBinaryResponseContent
import httpx
import pandas as pd

from typing import Iterator, AsyncIterator, Any, List


class HttpxXlsxBinaryResponseContent(HttpxBinaryResponseContent):
    response: httpx.Response

    def __init__(self, response: httpx.Response):
        super().__init__(response)
        self.response = response
        self.xlsx_file = self._parse_xlsx()

    def _parse_xlsx(self) -> pd.ExcelFile:
        """Parses the response content as an Excel file."""
        return pd.ExcelFile(self.response.content)

    def text(self) -> str:
        """Returns the response content as text."""
        # Converting all sheets to CSV formatted text
        all_text = []
        sheet_name = next(iter(self.xlsx_file.sheet_names))
        df = pd.read_excel(self.xlsx_file, sheet_name=sheet_name)
        all_text.append(df.to_csv(index=False))
        return "\n".join(all_text)

    def json(self, **kwargs: Any) -> Any:
        """Returns the response content as JSON."""
        # Converting all sheets to JSON
        sheet_name = next(iter(self.xlsx_file.sheet_names))
        df = pd.read_excel(self.xlsx_file, sheet_name=sheet_name)
        return df.to_dict(orient='records')

    def iter_text(self, chunk_size: int | None = None) -> Iterator[str]:
        """Iterates over the response content as text."""

        sheet_name = next(iter(self.xlsx_file.sheet_names))
        df = pd.read_excel(self.xlsx_file, sheet_name=sheet_name)
        for chunk in df.to_csv(index=False, chunksize=chunk_size):
            yield chunk

    def iter_lines(self) -> Iterator[str]:
        """Iterates over the response content line by line."""

        sheet_name = next(iter(self.xlsx_file.sheet_names))
        df = pd.read_excel(self.xlsx_file, sheet_name=sheet_name)
        for line in df.to_csv(index=False).splitlines():
            yield line

    async def aiter_text(self, chunk_size: int | None = None) -> AsyncIterator[str]:
        """Asynchronously iterates over the response content as text."""

        sheet_name = next(iter(self.xlsx_file.sheet_names))
        df = pd.read_excel(self.xlsx_file, sheet_name=sheet_name)
        for chunk in df.to_csv(index=False, chunksize=chunk_size):
            yield chunk

    async def aiter_lines(self) -> AsyncIterator[str]:
        """Asynchronously iterates over the response content line by line."""

        sheet_name = next(iter(self.xlsx_file.sheet_names))
        df = pd.read_excel(self.xlsx_file, sheet_name=sheet_name)
        for line in df.to_csv(index=False).splitlines():
            yield line
