def count_change(a, kinds=(50, 25, 10, 5, 1)):
    """Return the number of ways to change amount a using coin kinds."""
    if a == 0:
        return 1
    if a < 0 or len(kinds) == 0:
        return 0
    d = kinds[0]
    return count_change(a, kinds[1:]) + count_change(a - d, kinds)


def memo(f):
    cache = {}

    def memoize(a, kinds):
        key = "{},{}".format(a, len(kinds))
        if key not in cache.keys():
            cache[key] = f(a, kinds)
        return cache[key]
    return memoize


count_change = memo(count_change)
print(count_change(200, (50, 25, 10, 5, 1)))
