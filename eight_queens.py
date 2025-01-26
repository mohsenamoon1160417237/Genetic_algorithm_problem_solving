import itertools
import random

from scipy import special as sc

NUM_QUEENS = 8
POPULATION_SIZE = 10
MIXING_NUMBER = 2
MUTATION_RATE = 0.05


class EightQueensGeneticAlgorithm:

    @classmethod
    def fitness_score(cls, seq):
        score = 0

        for row in range(NUM_QUEENS):
            col = seq[row]

            for other_row in range(NUM_QUEENS):

                # queens cannot pair with itself
                if other_row == row:
                    continue
                if seq[other_row] == col:
                    continue
                if other_row + seq[other_row] == row + col:
                    continue
                if other_row - seq[other_row] == row - col:
                    continue
                # score++ if every pair of queens are non-attacking.
                score += 1

        # divide by 2 as pairs of queens are commutative
        return score / 2

    @classmethod
    def selection(cls, popul):
        parents = []

        for ind in popul:
            # select parents with probability proportional to their fitness score
            if random.randrange(sc.comb(NUM_QUEENS, 2) * 2) < cls.fitness_score(ind):
                parents.append(ind)

        return parents

    @classmethod
    def crossover(cls, parents):
        # random indexes to to cross states with
        cross_points = random.sample(range(NUM_QUEENS), MIXING_NUMBER - 1)
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
        for row in range(len(seq)):
            if random.random() < MUTATION_RATE:
                seq[row] = random.randrange(NUM_QUEENS)

        return seq

    @classmethod
    def print_found_goal(cls, population, to_print=True):
        for ind in population:
            score = cls.fitness_score(ind)
            if to_print:
                print(f'{ind}. Score: {score}')
            if score == sc.comb(NUM_QUEENS, 2):
                if to_print:
                    print('Solution found')
                return True

        if to_print:
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
            new = [random.randrange(NUM_QUEENS) for idx in range(NUM_QUEENS)]
            populate.append(new)

        return populate

    @classmethod
    def start(cls):

        generation = 0

        # generate random population
        population = cls.generate_population()

        while not cls.print_found_goal(population):
            print(f'Generation: {generation}')
            cls.print_found_goal(population)
            population = cls.evolution(population)
            generation += 1


if __name__ == "__main__":
    EightQueensGeneticAlgorithm.start()
