import os.path


def check_config():
    if os.path.isfile('ga.config'):
        return True
    else:
        return False


def gen_config():
    config_file = open('ga.config', 'w+')
    config_file.write(
        "populationSize:100\rmaximumGens:1000\rminBoundsSolutionConstraint:-5\rmaxBoundsSolutionConstraint:5")
    config_file.close()
    print('Generated default config file - please re-run this script')
    exit(0)


def parse_config():
    if check_config() is True:
        configuration = {}
        with open('ga.config', 'r') as configFile:
            for line in configFile:
                fields = line.split(':')
                if len(fields) == 2:
                    configuration[fields[0].strip()] = int(fields[1])
        print('Config file found - values loaded: ' + str(configuration))
        return configuration
    elif check_config() is False:
        print('Config file was not found - Generating...')
        gen_config()


config = parse_config()

population_size = config['populationSize']
maximum_gens = config['maximumGens']
min_solution_constraint = config['minBoundsSolutionConstraint']
max_solution_constraint = config['maxBoundsSolutionConstraint']
min_mutation_rate = config['minBoundsSolutionConstraint'] / config['maximumGens']
max_mutation_rate = config['maxBoundsSolutionConstraint'] / config['maximumGens']

current_gen = 0
