from typing import List

def gray_code(n: int) -> int:
    return n ^ (n >> 1)

def generate_kmap_indices() -> List[str]:
    """Генерирует 16 позиций в формате серого кода для карты 4x4"""
    indices = []
    for i in range(4):
        row = format(gray_code(i), '02b')
        for j in range(4):
            col = format(gray_code(j), '02b')
            indices.append(row + col)
    return indices

def bits_to_term(bits: str, vars: List[str], mode: str) -> str:
    term = []
    for i, b in enumerate(bits):
        if b == '-':
            continue
        var = vars[i]
        if mode == 'SOP':
            term.append(var if b == '1' else f"{var}̅")
        else:  # POS
            term.append(f"{var}̅" if b == '1' else var)
    return ''.join(term) if mode == 'SOP' else f"({' + '.join(term)})"

def minimize_sop(bits: List[str], values: List[int], vars: List[str]) -> str:
    used = [False] * len(values)
    terms = []

    for i in range(16):
        if values[i] != 1 or used[i]:
            continue
        for j in [1, 4]:  # horizontal (1) and vertical (4) neighbors
            ni = (i + j) % 16
            if values[ni] == 1 and not used[ni]:
                used[i] = used[ni] = True
                merged = ''.join(bits[i][k] if bits[i][k] == bits[ni][k] else '-' for k in range(4))
                terms.append(bits_to_term(merged, vars, 'SOP'))
                break
        else:
            terms.append(bits_to_term(bits[i], vars, 'SOP'))

    return ' + '.join(terms) if terms else '0'

def minimize_pos(bits: List[str], values: List[int], vars: List[str]) -> str:
    terms = []
    for i in range(16):
        if values[i] == 0:
            terms.append(bits_to_term(bits[i], vars, 'POS'))
    return ''.join(terms) if terms else '1'
