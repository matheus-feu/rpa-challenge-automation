from app.core.logger import logger
from app.domain.models import RPAResponse
from app.rpa.registry import registry


class RpaService:
	"""Despacha a execução para o runner registrado do operator informado."""

	@staticmethod
	async def run(rpa: str, payload: dict) -> RPAResponse:
		operator, input_cls = registry.get_rpa(rpa)
		body = input_cls.model_validate(payload)

		try:
			rpa = registry.create_rpa(operator)
			result = await rpa.run(body)

			return RPAResponse(
				success=True,
				message=result.message,
			)
		except Exception as exc:
			logger.exception("rpa.run_failed: %s", exc)
			return RPAResponse(
				success=False,
			)


rpa_Service = RpaService()
