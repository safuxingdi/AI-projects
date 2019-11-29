import random
from functools import lru_cache


class City(object):
    def __init__(self, number: int, weights: list):
        self.number = number
        self.neighbors = weights
        super().__init__()

    @lru_cache(maxsize=None)
    def get_closest(self, shops: tuple):
        """
        """
        d = []
        for city in shops:
            d.append(self.neighbors[city])
        return min(d)

    def __repr__(self):
        return f"c{self.number}"


class GeneticProblem(object):
    """
    """

    def __init__(self, genes: list, target_len: int, mutate_probability=0.1, fit_target=0, time_target=0, num_genrations=1000, population_num=100):
        self.mutate_probability = mutate_probability
        self.fit_target = fit_target
        self.time_target = time_target
        self.num_generation = num_genrations
        self.genes = genes
        self.target_len = target_len
        self.population_num = population_num
        self.population = self.build_population(population_num)
        super().__init__()

    def build_population(self, num=100, repeative=True):
        """
        """
        population = []
        for i in range(num):
            if repeative:
                p = random.choices(self.genes, k=self.target_len)
            else:
                p = random.sample(self.genes, k=self.target_len)
            population.append(p)
        return population

    def fitness_fn(self, sample: list):
        """
        """
        return 1

    def select(self, population: list, fitness_fn):
        """
        """
        fits = list(map(fitness_fn, population))
        chances = []
        for i, chance in enumerate(fits):
            for c in range(chance):
                chances.append(i)
        i = random.choice(chances)
        x = population[i]
        i = random.choice(chances)
        y = population[i]
        return (x, y)

    def reproduce(self, x: list, y: list):
        """
        """
        n = len(x)
        c = random.randint(0, n-1)
        child = x[:c] + y[c:]
        return child

    def mutate(self, child, genes: list):
        n = len(child)
        c = random.randint(0, n-1)
        new_gene = random.choice(genes)
        return child[:c] + [new_gene] + child[c + 1:]


class ShopsProblem(GeneticProblem):
    """
    """

    def __init__(self, file: str, target_len: int, mutate_probability=0.1, time_target=0, num_genrations=1000, population_num=100):
        self.cities = self.load_cities(file)
        self.longest = max([max(city.neighbors) for city in self.cities])
        super().__init__(genes=self.cities, target_len=target_len,
                         mutate_probability=mutate_probability, time_target=time_target, num_genrations=num_genrations, population_num=population_num)

    def load_cities(self, file: str):
        """
        """
        cities = []
        with open(file) as f:
            lines = f.readlines()
        f.close()
        for i, line in enumerate(lines):
            row = line.strip('\n').split()
            row = list(map(int, row))
            cities.append(City(number=i, weights=row))
        return cities

    def isValid(self, sample):
        if len(sample) != len(set(sample)):
            return False
        return True

    def fitness_fn(self, sample: list):
        """
        """
        @lru_cache(maxsize=None)
        def fn(shops):
            d = []
            for city in self.cities:
                if city.number not in shops:
                    d.append(city.get_closest(shops))
            worst = max(d)
            return self.longest - worst
        if len(sample) != len(set(sample)):
            return 0
        shops = [b.number for b in sample]
        return fn(tuple(shops))

    def build_population(self, num=100, repeative=False):
        return super().build_population(num, repeative=repeative)
