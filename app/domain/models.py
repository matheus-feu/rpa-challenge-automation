from pydantic import BaseModel, ConfigDict, EmailStr, Field


class ChallengeRecord(BaseModel):
	first_name: str = Field(alias="First Name")
	last_name: str = Field(alias="Last Name")
	company_name: str = Field(alias="Company Name")
	role_in_company: str = Field(alias="Role in Company")
	address: str = Field(alias="Address")
	email: EmailStr = Field(alias="Email")
	phone_number: str = Field(alias="Phone Number")
	challenge_id: str = ""

	model_config = ConfigDict(extra="ignore", populate_by_name=True, coerce_numbers_to_str=True)


class RPAResponse(BaseModel):
	success: bool
	message: str = ""
