COMPLEX_KEY_PATTERN = '{prefix}_{base}'


def create_key(base: str, prefix: str | None = None) -> str:
    key = base.upper()
    if prefix:
        key = COMPLEX_KEY_PATTERN.format(prefix=prefix.upper(), base=key)

    return key
