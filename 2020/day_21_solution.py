import argparse
import collections


def _parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument('infile',
                        type=argparse.FileType('r'),
                        help='Input text file for this puzzle')
    args = parser.parse_args()
    return args.infile.read().splitlines()


Food = collections.namedtuple('Food', ('ingredients', 'allergens'))
AllergenInfo = collections.namedtuple(
    'AllergenInfo', ('allergen_map', 'inert_set'))


class EliminationMap:
    def __init__(self):
        self._map = {}

    def __getitem__(self, key):
        if key not in self._map:
            raise ValueError(f'{key} not in EliminationMap')
        if 1 == len(self._map[key]):
            return self._map[key].copy().pop()
        return self._map[key].copy()

    def __contains__(self, key):
        return key in self._map

    def __iter__(self):
        for key, vals in self._map.items():
            if len(vals) == 1:
                yield key

    def items(self):
        """Iterator over only the solved items."""
        for key, vals in self._map.items():
            if len(vals) == 1:
                yield key, vals.copy().pop()

    def feed(self, key, values):
        if key not in self._map:
            self._map[key] = set(values)
            return
        try:
            self._map[key] = set(values) & self._map[key]
        except:
            breakpoint()
        if len(self._map[key]) == 1:
            self.uniquefy(self[key])

    def uniquefy(self, value):
        to_uniquefy = [value]
        while to_uniquefy:
            for key, values in self._map.items():
                if len(values) == 1:
                    continue
                if to_uniquefy[0] in values:
                    values.remove(to_uniquefy[0])
                    if len(values) == 1:
                        to_uniquefy.append(self[key])
            to_uniquefy.pop(0)


def parse_foods(input_lines):
    """Returns a tuple of Food objects parsed from the input lines."""
    result = []
    for line in input_lines:
        ingredient_part, allergen_part = line.split("(contains ")
        ingredients = ingredient_part.split()
        allergens = allergen_part[:-1].split(', ')
        result.append(Food(ingredients, allergens))
    return tuple(result)


def allergen_info_for_foods(foods):
    inert_set = set([ingr for food in foods for ingr in food.ingredients])
    allergen_map = EliminationMap()
    for food in foods:
        for allergen in food.allergens:
            allergen_map.feed(allergen, food.ingredients)
    for _, ingredient in allergen_map.items():
        inert_set.remove(ingredient)
    return AllergenInfo(allergen_map, inert_set)


def canonical_dangerous(allergen_info):
    allergens = sorted([a for a in allergen_info.allergen_map])
    return ','.join([allergen_info.allergen_map[a] for a in allergens])

def run_tests():
    sample_input = ('mxmxvkd kfcds sqjhc nhms (contains dairy, fish)',
                    'trh fvjkl sbzzf mxmxvkd (contains dairy)',
                    'sqjhc fvjkl (contains soy)',
                    'sqjhc mxmxvkd sbzzf (contains fish)')
    foods = parse_foods(sample_input)
    all_ingredients = [ingr for food in foods for ingr in food.ingredients]
    allergen_info = allergen_info_for_foods(foods)
    assert 5 == sum(
        (all_ingredients.count(ingr) for ingr in allergen_info.inert_set))
    foo = canonical_dangerous(allergen_info)
    assert 'mxmxvkd,sqjhc,fvjkl' == canonical_dangerous(allergen_info)


def main(input_lines):
    run_tests()
    foods = parse_foods(input_lines)
    all_ingredients = [ingr for food in foods for ingr in food.ingredients]
    allergen_info = allergen_info_for_foods(foods)
    answer_one = sum(
        (all_ingredients.count(ingr) for ingr in allergen_info.inert_set))
    answer_two = canonical_dangerous(allergen_info)
    return answer_one, answer_two


if __name__ == '__main__':
    answer_one, answer_two = main(_parse_args())
    print(f'Part One: {answer_one}')
    print(f'Part Two: {answer_two}')
