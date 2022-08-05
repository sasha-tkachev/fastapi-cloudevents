from pathlib import Path

import pytest

repo_root = Path(__file__).parent.parent


readme = (repo_root / "README.md").read_text()

example_files_expected_to_appear_in_readme = [
    repo_root / "examples/simple_server/example_server.py",
    repo_root / "examples/simple_server/example_binary_request.sh",
    repo_root / "examples/simple_server/example_structured_request.sh",
    repo_root / "examples/simple_server/example_response.txt",
    repo_root / "examples/binary_response_server/example_server.py",
    repo_root / "examples/binary_response_server/example_request.sh",
    repo_root / "examples/binary_response_server/example_response.txt",
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
