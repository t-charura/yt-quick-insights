import pytest
import yaml

from yt_quick_insights import utils


@pytest.mark.parametrize(
    "input_title, expected_output",
    [
        ("Simple Title", "simple_title"),
        ("Title with UPPERCASE and 123", "title_with_uppercase_and_123"),
        ("  Title with spaces  ", "title_with_spaces"),
        ("Title with special chars !@#$%^&*()", "title_with_special_chars"),
        ("A" * 250, "a" * 200),  # Test truncation
        ("", ""),  # Test empty string
    ],
)
def test_clean_youtube_video_title_basic_functionality(input_title, expected_output):
    assert utils.clean_youtube_video_title(input_title) == expected_output


@pytest.fixture
def mock_yaml_file():
    return """
    key1: value1
    key2: value2
    """


def test_load_yaml_file_success(tmp_path, mock_yaml_file):
    # Create a temporary YAML file
    file_name = "test.yaml"
    file_path = tmp_path / file_name
    file_path.write_text(mock_yaml_file)

    # Test loading the YAML file
    result = utils.load_yaml_file(file_name, tmp_path)
    assert result == {"key1": "value1", "key2": "value2"}


def test_load_yaml_file_not_found(tmp_path):
    # Test with a non-existent file
    with pytest.raises(FileNotFoundError):
        utils.load_yaml_file("non_existent.yaml", tmp_path)


def test_load_yaml_file_invalid_yaml(tmp_path):
    # Create an invalid YAML file
    file_name = "invalid.yaml"
    file_path = tmp_path / file_name
    file_path.write_text("invalid: yaml: content")

    # Test loading an invalid YAML file
    with pytest.raises(yaml.YAMLError):
        utils.load_yaml_file(file_name, tmp_path)
