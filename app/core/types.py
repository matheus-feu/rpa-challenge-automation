from pydantic import BaseModel, ConfigDict


class AppModel(BaseModel):
	"""Base Pydantic compartilhada por domain, schemas e inputs RPA."""

	model_config = ConfigDict(
		from_attributes=True,
		populate_by_name=True,
		str_strip_whitespace=True,
		use_enum_values=False,
	)
