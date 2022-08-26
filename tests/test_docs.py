import re
from pathlib import Path

import pytest

repo_root = Path(__file__).parent.parent


readme = (repo_root / "README.md").read_text()
tox_config = (repo_root / "tox.ini").read_text()

example_files_expected_to_appear_in_readme = [
    repo_root / "examples/simple_server/example_server.py",
    repo_root / "examples/simple_server/example_binary_request.sh",
    repo_root / "examples/simple_server/example_structured_request.sh",
    repo_root / "examples/simple_server/example_response.txt",
    repo_root / "examples/structured_response_server/example_server.py",
    repo_root / "examples/structured_response_server/example_request.sh",
    repo_root / "examples/structured_response_server/example_response.txt",
    repo_root / "examples/type_routing/example_server.py",
]


@pytest.mark.parametrize(
    "example_file",
    [
        pytest.param(path.read_text(), id=str(path))
        for path in example_files_expected_to_appear_in_readme
    ],
)
def test_certain_examples_should_appear_in_readme(example_file: str):
    assert example_file in readme


def test_coverage_badge_must_represent_correct_coverage():
    """
    It is easier to enforce a strict coverage in our tests and project it into
    the documentation rather then to relay on third party Coverage calculation systems.

    This test exists to make sure that future developers will not update one thing and
    not the other.
    """
    enforced_coverage = int(
        re.search(r"--cov-fail-under=(?P<percent>[0-9]+)", tox_config).groupdict()[
            "percent"
        ]
    )

    badge_coverage = int(
        re.search(
            r"https://img.shields.io/badge/"
            r"coverage-(?P<percent>[0-9]+)%25-brightgreen",
            readme,
        ).groupdict()["percent"]
    )
    assert badge_coverage == enforced_coverage
