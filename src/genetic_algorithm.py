import random

def create_population(nodes, size=10):
    return [random.sample(nodes, len(nodes)) for _ in range(size)]

def fitness(route, profit_func):
    return profit_func(route)

def selection(population, profit_func):
    population.sort(key=lambda r: fitness(r, profit_func), reverse=True)
    return population[:5]

def crossover(p1, p2):
    cut = len(p1)//2
    child = p1[:cut]
    for city in p2:
        if city not in child:
            child.append(city)
    return child

def mutate(route):
    i, j = random.sample(range(len(route)), 2)
    route[i], route[j] = route[j], route[i]
    return route

def run_ga(nodes, profit_func, generations=20):
    population = create_population(nodes)

    for _ in range(generations):
        selected = selection(population, profit_func)
        new_pop = selected.copy()

        while len(new_pop) < len(population):
            p1, p2 = random.sample(selected, 2)
            child = crossover(p1, p2)
            child = mutate(child)
            new_pop.append(child)

        population = new_pop

    best = max(population, key=lambda r: fitness(r, profit_func))
    return best