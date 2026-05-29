from app.core.logger import setup_logger
from app.rpa.challenge.input import ChallengeInput
from app.services.rpa_service import RpaService


async def main() -> None:
	setup_logger()
	result = await RpaService.run("rpa-challenge", ChallengeInput.build_payload())
	print(f"success={result.success} message={result.message}")


if __name__ == "__main__":
	import asyncio

	asyncio.run(main())
