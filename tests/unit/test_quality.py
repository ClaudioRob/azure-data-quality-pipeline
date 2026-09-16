from azure_data_quality.quality.quality import is_valid_uf


def test_is_valid_uf_accepts_valid_uf():
    assert is_valid_uf("SP") is True


def test_is_valid_uf_rejects_invalid_uf():
    assert is_valid_uf("XX") is False