from watchfiles import run_process


def main() -> None:
    run_process(
        "./proof_business_api",
        "./tests",
        target="poetry run pytest --record-mode=once -rP",
    )
