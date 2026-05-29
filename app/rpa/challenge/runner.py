from app.browser.driver import BrowserDriver
from app.core.logger import logger
from app.domain.enums import RPAOperator
from app.domain.models import RPAResponse
from app.rpa.base import BaseRPARunner
from app.rpa.challenge.input import ChallengeInput
from app.rpa.challenge.pages import ChallengePage


class ChallengeRunner(BaseRPARunner):

	def __init__(self, app_settings):
		super().__init__(app_settings)

	@property
	def operator(self) -> RPAOperator:
		return RPAOperator.RPA_CHALLENGE

	async def execute(self, driver: BrowserDriver, body: ChallengeInput, *args, **kwargs) -> RPAResponse:
		page_challenge = ChallengePage(driver)
		records = body.records
		total = len(records)

		await page_challenge.open()

		ok = 0
		for i, record in enumerate(records, 1):
			logger.info("Round %d/%d — %s %s", i, total, record.first_name, record.last_name)
			try:
				await page_challenge.fill_record(record)
				ok += 1
			except Exception as exc:
				logger.error("NOK: %s", exc)

		self.settings.output_dir.mkdir(parents=True, exist_ok=True)
		await page_challenge.take_screenshot()

		try:
			score = await page_challenge.get_result_message()
		except Exception:
			score = "nao capturado"
		return RPAResponse(
			success=ok == total,
			message=f"{ok}/{total} preenchidos - {score}"
		)
