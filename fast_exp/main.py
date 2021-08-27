def square(x):
    return x * x


def fast_exp(a, n):
    if n == 0:
        return 1
    if n % 2 == 0:
        return square(fast_exp(a, n // 2))
    else:
        return a * fast_exp(a, n - 1)


def normal_exp(a, n):
    if n == 0:
        return 1

    return a * normal_exp(a, n - 1)


print(normal_exp(2, 500))
print(2**1000000)
print(fast_exp(2, 1000000))