
from dissertation_intro_qa.core.exit_codes import ExitCode

def main():
    try:
        # simulate logic
        return ExitCode.SUCCESS
    except ValueError:
        return ExitCode.USAGE_ERROR
    except Exception:
        return ExitCode.RUNTIME_ERROR

if __name__ == "__main__":
    raise SystemExit(main())
