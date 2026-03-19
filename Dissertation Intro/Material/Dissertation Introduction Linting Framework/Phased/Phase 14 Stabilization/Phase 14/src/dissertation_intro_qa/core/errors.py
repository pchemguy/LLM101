"""Canonical error classes."""

class IntroQAError(Exception):
  """Base package error."""


class SchemaError(IntroQAError):
  """Schema validation failure."""


class ArtifactTypeError(IntroQAError):
  """Unexpected artifact type."""


class MissingArtifactError(IntroQAError):
  """Missing required artifact."""


class ContractViolation(IntroQAError):
  """Artifact or workflow contract violation."""


class ConfigurationError(IntroQAError):
  """Configuration error."""
