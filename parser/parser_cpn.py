import sys
sys.path.append('./')

from ParserSim import ParserCPN
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('--activities', type=list)
parser.add_argument('--variables', type=list)
parser.add_argument('--case_names', type=str)

args = parser.parse_args()

parameters = {
    'activities': args.activities,
    'variables': args.variables, 
    'case_names': args.case_names
}


for i in range(1,11):

    sim_path = f'cpn_sim/sim_{i}.txt'

    activities = parameters['activities']

    variables = parameters['variables']
    case_name = parameters['case_names']
    variables_to_delete = [x for x in variables if x!=case_name]

    parse = ParserCPN(sim_path, activities, variables, case_name, variables_to_delete)
    parse.to_csv(f'log_sim/LogSim_{i}.csv')