"""Solver for Advent of Code 2024, day 5."""

import functools
import textwrap


def run_tests():
    test_input = textwrap.dedent(
        """\
        47|53
        97|13
        97|61
        97|47
        75|29
        61|13
        75|53
        29|13
        97|29
        53|29
        61|53
        97|53
        61|29
        47|13
        75|47
        97|75
        47|61
        75|61
        47|29
        75|13
        53|13

        75,47,61,53,29
        97,61,53,29,13
        75,29,13
        75,97,47,61,53
        61,13,29
        97,13,75,29,47
    """
    )
    assert 143 == solve_part_1(test_input)
    assert 123 == solve_part_2(test_input)


class Update:
    def __init__(self, text):
        self.idx_lookup = {}
        update = []
        for idx, page_text in enumerate(text.split(",")):
            page = int(page_text)
            if page in self.idx_lookup:
                raise ValueError(f"Update contains a repeated page: {page}\n{text}")
            self.idx_lookup[page] = idx
            update.append(page)
        
        self.update = tuple(update)
 
    def __getitem__(self, item):
            return self.idx_lookup[item]
    
    def __contains__(self, item):
        return item in self.idx_lookup


def parse_input(input_text):
    rules_text, updates_text = input_text.split("\n\n")
    rules_lines = rules_text.splitlines()
    updates_lines = updates_text.splitlines()

    rules = {}
    for line in rules_lines:
        former_text, latter_text = line.split("|")
        former = int(former_text)
        latter = int(latter_text)
        if former not in rules:
            rules[former] = set()
        rules[former].add(latter)

    updates = tuple(Update(l) for l in updates_lines)

    return rules, updates


def is_valid_update(rules, update):
    for page, subsequents in rules.items():
            if page in update:
                for subsequent in subsequents:
                    if subsequent not in update:
                        continue
                    if update[subsequent] < update[page]:
                        return False
    return True


def page_comparison(rules, page_a, page_b):
    if page_a in rules:
        if page_b in rules[page_a]:
            return -1
    if page_b in rules:
        if page_a in rules[page_b]:
            return 1
    return 0


def solve_part_1(puzzle_input):
    rules, updates = parse_input(puzzle_input)

    valid_updates = tuple(u for u in updates if is_valid_update(rules, u))
    return sum(v.update[len(v.update) // 2] for v in valid_updates)


def solve_part_2(puzzle_input):
    rules, updates = parse_input(puzzle_input)

    invalid_updates = tuple(u for u in updates if not is_valid_update(rules, u))
    key_func = functools.cmp_to_key(functools.partial(page_comparison, rules))
    fixed_updates = tuple(sorted(v.update, key=key_func) for v in invalid_updates)
    return sum(f[len(f) // 2] for f in fixed_updates)
