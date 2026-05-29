from pathlib import Path
from typing import List

import pandas as pd

from app.domain.models import ChallengeRecord


class ExcelService:
	def __init__(self, file_path: str | Path):
		path = Path(file_path)
		if not path.is_file():
			raise FileNotFoundError(f"Planilha não encontrada: {path.resolve()}")
		self.file_path = path

	def read_excel(self) -> List[ChallengeRecord]:
		df = pd.read_excel(self.file_path)
		df.columns = [c.strip() for c in df.columns]
		return [ChallengeRecord(**row) for row in df.to_dict(orient='records')]
