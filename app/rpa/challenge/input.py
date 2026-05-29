from pathlib import Path

from pydantic import Field

from app.core.config import settings
from app.core.types import AppModel
from app.domain.models import ChallengeRecord
from app.services.excel_service import ExcelService


class ChallengeInput(AppModel):
	"""Dados de entrada do RPA — registros extraídos do Excel."""

	records: list[ChallengeRecord] = Field(min_length=1)

	@classmethod
	def from_excel(cls, file_path: str | Path | None = None) -> ChallengeInput:
		path = Path(file_path) if file_path else settings.excel_file_path
		return cls(records=ExcelService(path).read_excel())

	@classmethod
	def build_payload(cls, file_path: str | None = None) -> dict:
		return cls.from_excel(file_path).model_dump(mode="python")
