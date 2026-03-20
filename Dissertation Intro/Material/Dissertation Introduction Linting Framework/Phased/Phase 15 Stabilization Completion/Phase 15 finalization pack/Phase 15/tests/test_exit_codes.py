from dissertation_intro_qa.core import exit_codes


def test_exit_code_constants():
  assert exit_codes.SUCCESS == 0
  assert exit_codes.USER_ERROR == 1
  assert exit_codes.SCHEMA_ERROR == 2
  assert exit_codes.INTERNAL_ERROR == 3
