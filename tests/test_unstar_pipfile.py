import json
from pathlib import Path

from unstar_pipfile.unstar_pipfile import (
    PIPFILE,
    PIPFILE_LOCK,
    check_files,
    get_packages_and_versions,
    amend_pipfile,
)


def test_checkfiles(tmp_path, monkeypatch):
    """Test that files checks are performed correctly."""
    monkeypatch.chdir(tmp_path)
    assert check_files() == (False, "Can't find Pipfile")
    (tmp_path / PIPFILE).write_text(" ")
    assert check_files() == (False, "Can't find Pipfile.lock")
    (tmp_path / PIPFILE_LOCK).write_text(" ")
    assert check_files() == (True, "")


def test_get_packages_and_versions_when_empty(tmp_path, monkeypatch):
    """Test parsing packags and versions when there are none."""
    monkeypatch.chdir(tmp_path)
    (tmp_path / "Pipfile.lock").write_text(json.dumps({"default": {}}))
    assert get_packages_and_versions() == {}


def test_get_packages_and_versions(tmp_path, monkeypatch):
    """Test parsing packags and versions when there are none."""
    monkeypatch.chdir(tmp_path)
    (tmp_path / "Pipfile.lock").write_text(
        json.dumps({"default": {"package-foo": {"version": "version-bar"}}})
    )
    assert get_packages_and_versions() == {"package-foo": "version-bar"}


def test_amend_pipfile(tmp_path, monkeypatch):
    """Test replacing stars with precise versions end ot end."""
    monkeypatch.chdir(tmp_path)
    # prepare mock data for processing
    mock_data_path = Path(__file__).parent / "mock_data"
    with open(mock_data_path / PIPFILE, "r") as mock_pipfile:
        (tmp_path / PIPFILE).write_text(mock_pipfile.read())
    with open(mock_data_path / PIPFILE_LOCK, "r") as mock_pipfile_lock:
        (tmp_path / PIPFILE_LOCK).write_text(mock_pipfile_lock.read())

    with open(mock_data_path / "Pipfile_processed", "r") as expected_output:
        amend_pipfile()
        assert (tmp_path / PIPFILE).read_text() == expected_output.read()
