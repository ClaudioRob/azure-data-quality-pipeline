from azure_data_quality.quality.quality import is_valid_uf


def test_is_valid_uf_accepts_valid_uf():
    assert is_valid_uf("SP") is True


def test_is_valid_uf_rejects_invalid_uf():
    assert is_valid_uf("XX") is False


def test_is_valid_uf_accepts_valid_ufs():
    ufs = ["SP", "RJ", "MG"]

    for uf in ufs:
        assert is_valid_uf(uf) is True


def test_all_ufs_are_valid():
    ufs = ["SP", "RJ", "MG", "ES", "PR", "SC", "RS"]

    for uf in ufs:
        assert is_valid_uf(uf), f"UF inválida: {uf}"