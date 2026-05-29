from pathlib import Path

from app.browser.driver import BrowserDriver
from app.core.config import settings
from app.domain.models import ChallengeRecord


class ChallengePage:
	"""Page Object do RPA Challenge — cada record é um round após Start."""

	START_BUTTON = "button.uiColorButton"
	SUBMIT_BUTTON = "input[type='submit']"
	RESULT_MESSAGE = ".message2"
	ROUND_READY_SELECTOR = "input[ng-reflect-name='labelFirstName']"

	FIELD_SELECTORS: dict[str, str] = {
		"first_name": "input[ng-reflect-name='labelFirstName']",
		"last_name": "input[ng-reflect-name='labelLastName']",
		"company_name": "input[ng-reflect-name='labelCompanyName']",
		"role_in_company": "input[ng-reflect-name='labelRole']",
		"address": "input[ng-reflect-name='labelAddress']",
		"email": "input[ng-reflect-name='labelEmail']",
		"phone_number": "input[ng-reflect-name='labelPhone']",
	}

	def __init__(self, driver: BrowserDriver):
		self.driver = driver

	async def open(self) -> None:
		"""Abre o challenge e inicia o round."""
		await self.driver.goto(settings.challenge_url, wait_until="networkidle")

		await self.driver.wait_for_selector(self.START_BUTTON, state="visible")
		await self.driver.click(self.START_BUTTON)
		await self.wait_for_round()

	async def wait_for_round(self) -> None:
		"""Aguarda o formulário do round atual (campos reposicionados)."""
		await self.driver.wait_for_selector(self.ROUND_READY_SELECTOR, state="visible")

	async def fill_record(self, record: ChallengeRecord) -> None:
		"""Preenche o round atual e envia para avançar ao próximo."""
		await self.wait_for_round()

		for field, selector in self.FIELD_SELECTORS.items():
			value = getattr(record, field)
			await self.driver.wait_for_selector(selector, state="visible")
			await self.driver.fill(selector, str(value))

		await self.driver.wait_for_selector(self.SUBMIT_BUTTON, state="visible")
		await self.driver.click(self.SUBMIT_BUTTON)

	async def get_result_message(self) -> str:
		return await self.driver.get_text(self.RESULT_MESSAGE)

	async def take_screenshot(self, path: Path | None = None) -> None:
		await self.driver.screenshot(path or settings.screenshot_path)
