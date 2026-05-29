from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
	excel_file_path: Path = Path('data/challenge.xlsx')

	challenge_url: str = 'https://rpachallenge.com/'
	headless: bool = False
	timeout: int = 15000

	output_dir: Path = Path('output')
	screenshot_name: str = 'score.png'

	@property
	def screenshot_path(self) -> Path:
		return self.output_dir / self.screenshot_name

	model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')


@lru_cache
def get_settings() -> Settings:
	return Settings()


settings = get_settings()
