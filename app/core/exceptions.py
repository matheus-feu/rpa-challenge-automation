class ChallengeError(Exception):
	"""Erro base da aplicação."""


class BrowserError(ChallengeError):
	"""Falha na automação de browser."""


class RpaError(ChallengeError):
	"""Erro de adapter ao rpa"""


class WorkflowError(ChallengeError):
	"""Falha em workflow RPA."""

	def __init__(self, workflow: str, message: str, *, recoverable: bool = False):
		self.workflow = workflow
		self.recoverable = recoverable
		super().__init__(f"[{workflow}] {message}")
