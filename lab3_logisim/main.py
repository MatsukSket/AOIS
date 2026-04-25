def combine(term1, term2):
    """Объединяет два терма, если отличаются на 1 символ."""
    diffs = 0
    res = []
    for c1, c2 in zip(term1, term2):
        if c1 != c2:
            diffs += 1
            res.append('-')
        else:
            res.append(c1)
    return "".join(res) if diffs == 1 else None


def find_prime_terms(num_vars, dont_cares_terms, target_terms):
    """Функция минимизации"""
    terms = {format(m, f'0{num_vars}b') for m in (target_terms, dont_cares_terms)}
    primes = set()

    while terms:
        new_terms = set()
        marked = set()
        term_list = list(terms)
        for i in range(len(term_list)):
            for j in range(i+1, len(term_list)):
                combined = combine(term_list[i], term_list[j])
                if combined:
                    new_terms.add(combined)
                    marked.add(term_list[i])
                    marked.add(term_list[j])
        primes.update(terms - marked)
        terms = new_terms

    uncovered = {format(m, f'0{num_vars}b') for m in target_terms}
    covers = {}
    for p in primes:
        covers[p] = {m for m in uncovered if all(pc =='-'  or pc == mc for pc, mc in zip(p, m))}

    selected_primes = []
    while uncovered:
        best_p = max(covers.keys(), key=lambda p: len(covers[p] & uncovered))
        if len(covers[best_p] & uncovered) == 0:
            break
        selected_primes.append(best_p)
        uncovered -= covers[best_p]

        return selected_primes


def