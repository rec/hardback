from attr import dataclass, Factory
from . import raw_codes


@dataclass(slots=True)
class ECC:
    L: int = 0
    M: int = 0
    Q: int = 0
    H: int = 0


@dataclass(slots=True)
class CodeInfo:
    size: int = 0
    data: ECC = Factory(ECC)
    numeric: ECC = Factory(ECC)
    alphanumeric: ECC = Factory(ECC)
    binary: ECC = Factory(ECC)
    kanji: ECC = Factory(ECC)


def _read_codes():
    def to_q_dict(L, M, Q, H):
        return locals()

    for size, *eccs in raw_codes.RAW_CODES:
        yield CodeInfo(size, *(ECC(*i) for i in eccs))


CODES = tuple(_read_codes())
