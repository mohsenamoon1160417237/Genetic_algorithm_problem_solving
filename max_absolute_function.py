import itertools
import random

NUM_BITS = 10
POPULATION_SIZE = 10
MIXING_NUMBER = 2
MUTATION_RATE = 0.05
MAX_GENS = 300


class MaxAbsoluteFunctionGeneticAlgorithm:

    max_score = 0
    max_generations = MAX_GENS
    selected_response = list()

    @classmethod
    def fitness_score(cls, seq: str):
        score = 0
        ind = 0
        bits: list = seq[::-1]
        for bit in bits:
            ind -= 1
            score += int(bit) * (2 ** ind)

        score = abs(score ** 3 - score * 3 + 2)
        return score

    @classmethod
    def selection(cls, popul):
        parents = []
        new_population = sorted(popul, key=lambda ind: cls.fitness_score(ind))
        for enum, chromosome in enumerate(new_population):
            # select parents with probability proportional to their fitness score
            if random.randrange(POPULATION_SIZE * 2) < enum:
                parents.append(chromosome)

        return parents

    @classmethod
    def crossover(cls, parents):
        # random indexes to to cross states with
        cross_points = random.sample(range(NUM_BITS), MIXING_NUMBER - 1)
        offsprings = []

        # all permutations of parents
        permutations = list(itertools.permutations(parents, MIXING_NUMBER))

        for perm in permutations:
            offspring = []

            # track starting index of sublist
            start_pt = 0

            for parent_idx, cross_point in enumerate(cross_points):  # doesn't account for last parent

                # sublist of parent to be crossed
                parent_part = perm[parent_idx][start_pt:cross_point]
                offspring.append(parent_part)

                # update index pointer
                start_pt = cross_point

            # last parent
            last_parent = perm[-1]
            parent_part = last_parent[cross_point:]
            offspring.append(parent_part)

            # flatten the list since append works kinda differently
            offsprings.append(list(itertools.chain(*offspring)))

        return offsprings

    @classmethod
    def mutate(cls, seq):
        for bit in range(len(seq)):
            if random.random() < MUTATION_RATE:
                seq[bit] = random.randrange(2)

        return seq

    @classmethod
    def print_found_goal(cls, population):
        for ind in population:
            score = cls.fitness_score(ind)
            if score > cls.max_score:
                cls.max_score = score
                cls.selected_response = ind
                cls.max_generations = MAX_GENS

            cls.max_generations = cls.max_generations - 1

            print(f'{ind}. Score: {score}')
            if cls.max_generations <= 0:
                print('Solution found')
                return True

        print('Solution not found')
        return False

    @classmethod
    def evolution(cls, popul):
        # select individuals to become parents
        parents = cls.selection(popul)

        # recombination. Create new offsprings
        offsprings = cls.crossover(parents)

        # mutation
        offsprings = list(map(cls.mutate, offsprings))

        # introduce top-scoring individuals from previous generation and keep top fitness individuals
        new_gen = offsprings

        for ind in popul:
            new_gen.append(ind)

        new_gen = sorted(new_gen, key=lambda ind: cls.fitness_score(ind), reverse=True)[:POPULATION_SIZE]

        return new_gen

    @classmethod
    def generate_population(cls) -> list:
        populate = []

        for individual in range(POPULATION_SIZE):
            new = [random.randrange(2) for idx in range(NUM_BITS)]
            populate.append(new)

        return populate

    @classmethod
    def start(cls):

        # generate random population
        population = cls.generate_population()

        while not cls.print_found_goal(population):
            cls.print_found_goal(population)
            population = cls.evolution(population)


if __name__ == "__main__":
    MaxAbsoluteFunctionGeneticAlgorithm.start()