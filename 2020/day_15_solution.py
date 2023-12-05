def recitation(start, n):
    seen = {}
    for i, x in enumerate(start[:-1]):
        seen[x] = i

    last = start[-1]
    for i in range(len(start) - 1, n - 1):
        if last in seen:
            cur = i - seen[last]
        else:
            cur = 0
        seen[last] = i
        last = cur
    return last


def main():
    assert recitation((0, 3, 6), 8) == 0
    assert recitation((0, 3, 6), 2020) == 436
    assert recitation((1, 3, 2), 2020) == 1
    assert recitation((2, 1, 3), 2020) == 10
    assert recitation((1, 2, 3), 2020) == 27
    assert recitation((2, 3, 1), 2020) == 78
    assert recitation((3, 2, 1), 2020) == 438
    assert recitation((3, 1, 2), 2020) == 1836
    answer_one = recitation((7, 12, 1, 0, 16, 2), 2020)
    assert recitation((0, 3, 6), 30000000) == 175594
    assert recitation((1, 3, 2), 30000000) == 2578
    assert recitation((2, 1, 3), 30000000) == 3544142
    assert recitation((1, 2, 3), 30000000) == 261214
    assert recitation((2, 3, 1), 30000000) == 6895259
    assert recitation((3, 2, 1), 30000000) == 18
    assert recitation((3, 1, 2), 30000000) == 362
    answer_two = recitation((7, 12, 1, 0, 16, 2), 30000000)
    return answer_one, answer_two


if __name__ == '__main__':
    answer_one, answer_two = main()
    print(f'Part One: {answer_one}')
    print(f'Part Two: {answer_two}')
