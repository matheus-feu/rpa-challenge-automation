from abc import ABC, abstractmethod
from typing import Any

from app.browser import browser_manager
from app.core.config import Settings
from app.core.exceptions import RpaError
from app.core.logger import logger
from app.domain.enums import RPAOperator
from app.domain.models import RPAResponse


class BaseRPARunner(ABC):
	"""Contrato base para runners RPA."""

	def __init__(self, settings: Settings) -> None:
		self.settings = settings

	@property
	@abstractmethod
	def operator(self) -> RPAOperator:
		raise NotImplementedError

	@abstractmethod
	async def execute(self, driver: Any, body: Any, *args, **kwargs) -> RPAResponse:
		raise NotImplementedError

	async def run(self, body: Any, *args, **kwargs) -> RPAResponse:
		op = self.operator
		logger.info("rpa.start operator=%s", op)

		try:
			async with browser_manager as driver:
				result = await self.execute(driver, body, *args, **kwargs)
		except RpaError:
			logger.error("rpa.failed operator=%s", op)
			raise
		except Exception:
			logger.exception("rpa.failed operator=%s", op)
			raise

		logger.info(
			"rpa.finish operator=%s success=%s message=%s",
			op,
			result.success,
			result.message,
		)
		return result
