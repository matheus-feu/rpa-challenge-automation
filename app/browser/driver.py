from abc import ABC, abstractmethod
import asyncio
from pathlib import Path
from typing import Any

from app.core.config import settings
from app.core.logger import logger


class BrowserDriver(ABC):
	"""Contrato das pages — seletores Playwright (text=, >>) + métodos abstratos."""

	@abstractmethod
	async def prepare_run(self) -> None:
		"""Sessão limpa antes de cada execução RPA."""

	@abstractmethod
	async def goto(self, url: str, *, wait_until: str = "domcontentloaded") -> None:
		"""Navega para uma URL."""
		pass

	@abstractmethod
	async def click(self, selector: str, *, timeout_ms: int | None = None) -> None:
		"""Clica em um seletor."""
		pass

	@abstractmethod
	async def hover(self, selector: str, *, timeout_ms: int | None = None) -> None:
		"""Move o cursor sobre um seletor."""
		pass

	@abstractmethod
	async def click_opens_new_tab(self, selector: str, *, timeout_ms: int | None = None) -> None:
		"""Clica em um link e passa a operar na nova aba aberta."""

	@abstractmethod
	async def fill(self, selector: str, value: str, *, timeout_ms: int | None = None) -> None:
		"""Preenche um campo de texto."""
		pass

	@abstractmethod
	async def type_text(self, selector: str, value: str, *, delay_ms: int = 50, timeout_ms: int | None = None) -> None:
		"""Simula digitação tecla por tecla (para campos que bloqueiam paste/fill)."""

	@abstractmethod
	async def select_option(self, selector: str, value: str) -> None:
		"""Seleciona uma opção de um seletor."""
		pass

	@abstractmethod
	async def select_option_by_label(self, selector: str, label: str) -> None:
		"""Seleciona uma opção de um seletor pelo label."""
		pass

	@abstractmethod
	async def wait_for_selector(self, selector: str, *, timeout_ms: int | None = None, state: str = "visible") -> None:
		"""Aguarda um seletor aparecer na página."""
		pass

	@abstractmethod
	async def wait_for_navigation(self, *, timeout_ms: int | None = None) -> None:
		"""Aguarda a navegação da página."""
		pass

	@abstractmethod
	async def upload_file(self, selector: str, file_path: Path) -> None:
		"""Faz o upload de um arquivo para um seletor."""
		pass

	@abstractmethod
	async def get_text(self, selector: str) -> str:
		"""Obtém o texto de um seletor."""
		pass

	@abstractmethod
	async def is_visible(self, selector: str) -> bool:
		"""Verifica se um seletor está visível na página."""
		pass

	@abstractmethod
	async def screenshot(self, path: Path) -> None:
		"""Tira um screenshot da página."""
		pass

	@abstractmethod
	async def evaluate(self, script: str, arg: Any = None) -> Any:
		"""Executa um script JavaScript na página."""
		pass

	@abstractmethod
	async def click_in_frame(
			self, frame_selector: str, element_selector: str, *, timeout_ms: int | None = None
	) -> None:
		"""Clica em um elemento dentro de um iframe."""

	@abstractmethod
	async def wait_for_function(self, expression: str, *, timeout_ms: int | None = None) -> None:
		"""Aguarda uma expressão JS retornar truthy."""

	@abstractmethod
	async def close(self) -> None:
		"""Fecha o navegador."""
		pass

	def pop_last_dialog_message(self) -> str | None:
		"""Mensagem de alert/confirm nativo capturada pelo browser, se houver."""
		return None

	@abstractmethod
	async def try_click_by_text(self, *texts: str, timeout_ms: int = 5_000) -> bool:
		"""Clica no primeiro texto visível encontrado."""
		pass


class BrowserManager:
	"""Abre Chromium (Playwright) sob demanda — no primeiro RPA."""

	def __init__(self) -> None:
		self._driver: BrowserDriver | None = None
		self._lock = asyncio.Lock()

	@property
	def is_running(self) -> bool:
		return self._driver is not None

	async def start(self) -> BrowserDriver:
		"""Inicia o navegador."""
		if self._driver is not None:
			return self._driver

		from app.browser.playwright import PlaywrightDriver

		self._driver = await PlaywrightDriver.start(settings)
		logger.info("browser.started headless=%s", settings.headless)
		return self._driver

	async def stop(self) -> None:
		"""Para o navegador."""
		if self._driver is None:
			return
		await self._driver.close()
		self._driver = None
		logger.info("browser.stopped")

	async def __aenter__(self):
		return await self.prepare_run()

	async def __aexit__(self, *exc):
		await self.stop()

	async def prepare_run(self) -> BrowserDriver:
		"""Prepara a sessão para uma nova execução RPA."""
		async with self._lock:
			if self._driver is None:
				self._driver = await self.start()
			await self._driver.prepare_run()
			return self._driver

	def release(self) -> None:
		"""Libera o lock após a execução do RPA."""
		if self._lock.locked():
			self._lock.release()


browser_manager = BrowserManager()
