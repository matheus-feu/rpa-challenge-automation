from pathlib import Path
from typing import Any

from playwright.async_api import Browser, BrowserContext, Page, async_playwright

from app.browser.driver import BrowserDriver
from app.core.config import Settings


def _normalize_selector(selector: str) -> str:
	selector = selector.strip()
	if selector.startswith(("xpath=", "text=", "#", ".", "[", "role=")):
		return selector
	if selector.startswith("//") or selector.startswith("/html"):
		return f"xpath={selector}"
	return selector


class PlaywrightDriver(BrowserDriver):

	@classmethod
	async def start(cls, settings: Settings) -> "PlaywrightDriver":
		"""Inicia o navegador."""
		pw = await async_playwright().start()
		try:
			browser = await pw.chromium.launch(headless=settings.headless)
		except Exception as exc:
			await pw.stop()
			raise BrowserError(f"Falha ao iniciar Chromium: {exc}") from exc

		driver = cls(browser, settings)
		driver._playwright = pw
		return driver

	def __init__(self, browser: Browser, settings: Settings):
		self._browser = browser
		self._settings = settings
		self._context: BrowserContext | None = None
		self._page: Page | None = None
		self._playwright = None

	async def prepare_run(self, *, fresh: bool = True) -> None:
		if not fresh and self._page and self._context:
			return
		if self._context:
			await self._context.close()
		self._context = await self._browser.new_context(
			accept_downloads=True,
			viewport={"width": 1920, "height": 1080},
			locale="pt-BR",
		)
		self._page = await self._context.new_page()
		self._page.set_default_timeout(self._settings.timeout)

	async def goto(self, url: str, *, wait_until: str = "domcontentloaded") -> None:
		await self._page.goto(url, wait_until=wait_until)

	async def click(self, selector: str, *, timeout_ms: int | None = None) -> None:
		await self._page.click(_normalize_selector(selector), timeout=timeout_ms)

	async def hover(self, selector: str, *, timeout_ms: int | None = None) -> None:
		await self._page.locator(_normalize_selector(selector)).first.hover(timeout=timeout_ms)

	async def click_opens_new_tab(self, selector: str, *, timeout_ms: int | None = None) -> None:
		async with self._page.context.expect_page() as new_page_info:
			await self._page.click(_normalize_selector(selector), timeout=timeout_ms)
		self._page = await new_page_info.value

	async def fill(self, selector: str, value: str, *, timeout_ms: int | None = None) -> None:
		await self._page.fill(_normalize_selector(selector), value, timeout=timeout_ms)

	async def type_text(self, selector: str, value: str, *, delay_ms: int = 50, timeout_ms: int | None = None) -> None:
		loc = self._page.locator(_normalize_selector(selector))
		if timeout_ms:
			await loc.wait_for(timeout=timeout_ms)
		await loc.type(value, delay=delay_ms)

	async def select_option(self, selector: str, value: str) -> None:
		await self._page.select_option(_normalize_selector(selector), value)

	async def select_option_by_label(self, selector: str, label: str) -> None:
		await self._page.select_option(_normalize_selector(selector), label=label)

	async def wait_for_selector(self, selector: str, *, timeout_ms: int | None = None, state: str = "visible") -> None:
		await self._page.wait_for_selector(_normalize_selector(selector), timeout=timeout_ms, state=state)

	async def wait_for_navigation(self, *, timeout_ms: int | None = None) -> None:
		await self._page.wait_for_load_state("domcontentloaded", timeout=timeout_ms)

	async def upload_file(self, selector: str, file_path: Path) -> None:
		await self._page.set_input_files(_normalize_selector(selector), str(file_path))

	async def get_text(self, selector: str) -> str:
		return await self._page.locator(_normalize_selector(selector)).inner_text()

	async def is_visible(self, selector: str) -> bool:
		return await self._page.locator(_normalize_selector(selector)).is_visible()

	async def screenshot(self, path: Path) -> None:
		await self._page.screenshot(path=path, full_page=True)

	async def evaluate(self, script: str, arg: Any = None) -> Any:
		return await self._page.evaluate(script, arg)

	async def click_in_frame(self, frame_selector: str, element_selector: str, *,
	                         timeout_ms: int | None = None) -> None:
		frame = self._page.frame_locator(frame_selector)
		await frame.locator(element_selector).click(timeout=timeout_ms)

	async def wait_for_function(self, expression: str, *, timeout_ms: int | None = None) -> None:
		await self._page.wait_for_function(expression, timeout=timeout_ms)

	async def try_click_by_text(self, *texts: str, timeout_ms: int = 5_000) -> bool:
		for text in texts:
			try:
				await self._page.get_by_text(text, exact=False).first.click(timeout=timeout_ms)
				return True
			except Exception:
				continue
		return False

	async def close(self) -> None:
		try:
			if self._context:
				await self._context.close()
		except Exception:
			pass
		try:
			await self._browser.close()
		except Exception:
			pass
		try:
			if self._playwright:
				await self._playwright.stop()
		except Exception:
			pass
