from __future__ import annotations

from pathlib import Path
from unittest import mock

import pytest

from sweagent import REPO_ROOT
from sweagent.utils.config import Config, convert_path_to_abspath, convert_paths_to_abspath


def test_config_retrieval_fails():
    config = Config()
    with pytest.raises(KeyError):
        config["DOESNTEXIST"]


def test_config_retrieval_get():
    config = Config()
    assert config.get("asdfasdf", "default") == "default"


def test_retrieve_from_file(tmp_path):
    tmp_keys_cfg = tmp_path / "keys.cfg"
    tmp_keys_cfg.write_text("MY_KEY: 'VALUE'\n")
    config = Config(keys_cfg_path=tmp_keys_cfg)
    assert config["MY_KEY"] == "VALUE"


def test_retrieve_from_env(tmp_path):
    with mock.patch.dict("os.environ", {"MY_KEY": "VALUE"}):
        tmp_keys_cfg = tmp_path / "keys.cfg"
        tmp_keys_cfg.write_text("MY_KEY: 'other VALUE'\n")
        config = Config(keys_cfg_path=tmp_keys_cfg)
        assert config["MY_KEY"] == "VALUE"


def test_convert_path_to_abspath():
    assert convert_path_to_abspath("sadf") == REPO_ROOT / "sadf"
    assert convert_path_to_abspath("/sadf") == Path("/sadf")


def test_convert_paths_to_abspath():
    assert convert_paths_to_abspath([Path("sadf"), "/sadf"]) == [REPO_ROOT / "sadf", Path("/sadf")]
