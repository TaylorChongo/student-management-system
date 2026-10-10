"""CLI interaction tests using injected input and output functions."""

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from main import run_cli


class CliTests(unittest.TestCase):
    def test_cli_can_register_student_and_exit(self) -> None:
        # An iterator models a deterministic sequence of console responses.
        answers = iter(["1", "S001", "Alex", "alex@example.com", "U", "0"])
        output: list[str] = []

        def answer(prompt: str) -> str:
            return next(answers) if prompt is not None else next(answers)

        with TemporaryDirectory() as directory:
            run_cli(
                input_fn=answer,
                output=output.append,
                data_file=Path(directory) / "student_data.json",
            )

        self.assertTrue(any("Registered Alex successfully." in message for message in output))
        self.assertEqual(output[-1], "Goodbye.")

    def test_cli_reports_invalid_menu_choice(self) -> None:
        answers = iter(["invalid", "0"])
        output: list[str] = []

        def answer(prompt: str) -> str:
            return next(answers) if prompt is not None else next(answers)

        with TemporaryDirectory() as directory:
            run_cli(
                input_fn=answer,
                output=output.append,
                data_file=Path(directory) / "student_data.json",
            )

        self.assertTrue(any("Invalid option" in message for message in output))


if __name__ == "__main__":
    unittest.main()
