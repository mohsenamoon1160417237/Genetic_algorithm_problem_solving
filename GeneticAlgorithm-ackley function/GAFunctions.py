import random
import math as mt
from GAConfig import population_size, min_mutation_rate, max_mutation_rate, min_solution_constraint, \
    max_solution_constraint


def ackley_fitness_func(x, y):
    ackley_component_a = -0.2 * mt.sqrt(0.5 * (x * x + y * y))
    ackley_component_b = 0.5 * (mt.cos(2 * mt.pi * x) + mt.cos(2 * mt.pi * y))
    fitness = (-20 * mt.exp(ackley_component_a)) - mt.exp(ackley_component_b) + mt.exp(1) + 20
    return fitness


def init_population(pop_size):
    initial_population = []
    count = 0
    for x in range(pop_size):
        individual = [0, 0]
        individual[0] = random.uniform(min_solution_constraint, max_solution_constraint)
        individual[1] = random.uniform(min_solution_constraint, max_solution_constraint)
        initial_population.append(individual)
        count += 1
    return initial_population


def eval_fitness(population):
    fitnesses = []
    for i in range(population_size):
        fitness = ackley_fitness_func(population[i][0], population[i][1])
        fitnesses.append(fitness)
    return fitnesses


def pick_parents(population):
    parents = []
    for k in range(population_size):
        first_parent = random.choice(population)
        second_parent = random.choice(population)
        first_parent_fit = abs(ackley_fitness_func(float(first_parent[0]), float(first_parent[1])))
        second_parent_fit = abs(ackley_fitness_func(float(second_parent[0]), float(second_parent[1])))
        if second_parent_fit < first_parent_fit:
            parents.append(second_parent)
        else:
            parents.append(first_parent)
    return parents


def gen_rand_coors(min_bound, max_bound):
    rand_coors = random.uniform(min_bound, max_bound)
    return rand_coors


def cross_over_func(first_parent, second_parent):
    if random.randint(0, 1):
        child_x_coors = first_parent[0]
        child_x_coors += gen_rand_coors(min_mutation_rate, max_mutation_rate)
        child_y_coors = second_parent[1]
        child_y_coors += gen_rand_coors(min_mutation_rate, max_mutation_rate)
        child = [child_x_coors, child_y_coors]
    else:
        child_x_coors = first_parent[1]
        child_x_coors += gen_rand_coors(min_mutation_rate, max_mutation_rate)
        child_y_coors = second_parent[0]
        child_y_coors += gen_rand_coors(min_mutation_rate, max_mutation_rate)
        child = [child_x_coors, child_y_coors]
    return child


def gen_children(parents):
    children = []
    for y in range(population_size):
        rand_selected_first_parent = random.choice(parents)
        rand_selected_second_parent = random.choice(parents)
        child = cross_over_func(rand_selected_first_parent, rand_selected_second_parent)
        children.append(child)
    return children
