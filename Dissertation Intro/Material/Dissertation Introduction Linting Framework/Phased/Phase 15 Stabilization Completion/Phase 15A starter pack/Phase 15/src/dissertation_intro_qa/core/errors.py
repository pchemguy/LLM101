class IntroQAError(Exception):
  """Base package error."""


class SchemaError(IntroQAError):
  """Artifact schema / contract error."""


class ArtifactTypeError(IntroQAError):
  """Unexpected artifact type."""


class MissingArtifactError(IntroQAError):
  """Missing file or required artifact."""


class ContractViolation(IntroQAError):
  """Workflow contract violation."""
