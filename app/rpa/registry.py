from app.core.config import settings as default_settings
from app.core.exceptions import RpaError
from app.domain.enums import RPAOperator
from app.rpa.base import BaseRPARunner
from app.rpa.challenge.input import ChallengeInput
from app.rpa.challenge.runner import ChallengeRunner


class RpaRegistry:
	_by_slug: dict[str, tuple[RPAOperator, type]] = {
		"rpa-challenge": (RPAOperator.RPA_CHALLENGE, ChallengeInput),
	}

	_runners: dict[RPAOperator, type[BaseRPARunner]] = {
		RPAOperator.RPA_CHALLENGE: ChallengeRunner,
	}

	def __init__(self) -> None:
		self._settings = default_settings

	def get_rpa(self, slug: str) -> tuple[RPAOperator, type]:
		try:
			return self._by_slug[slug]
		except KeyError as exc:
			options = ", ".join(self._by_slug)
			raise ValueError(f"Portal '{slug}' não encontrado. Opções disponíveis: {options}") from exc

	def create_rpa(self, operator: RPAOperator) -> BaseRPARunner:
		try:
			return self._runners[operator](self._settings)
		except KeyError as exc:
			raise RpaError(f"RPA não registrado para: {operator}") from exc


registry = RpaRegistry()
