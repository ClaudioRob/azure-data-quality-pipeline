def is_valid_uf(uf: str) -> bool:
    valid_ufs = {"SP", "RJ", "MG", "ES", "PR", "SC", "RS"}

    return uf in valid_ufs