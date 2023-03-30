from tqdm import tqdm
import re
import pandas as pd

class ParserCPN:
    def __init__(self, sim_path, activities, variables, case_names ,variables_to_delete):
        self.sim_path = sim_path
        with open(sim_path) as f:
            lines = f.readlines()
        self.lines = lines[4:]
        self.events = self.DivideInEvents()
        self.variables = variables
        self.variables_to_delete = variables_to_delete
        self.activities = activities
        self.case_names = case_names
        self.data_table = self.CreateDataFrame()

    def DivideInEvents(self):

        events = []
        start = True

        print('Parsing Cases')
        for line in tqdm(self.lines):
            if line[0] != ' ':
                if not start:
                    events.append(event)
                else:
                    start = False
                event = []
                event.append(line)
            else:
                event.append(line)

        return events

    def CreateDataFrame(self):
        log_dict = {'concept:name': []} | {var: [] for var in self.variables}

        for event in tqdm(self.events):
            t = int(event[0].split('\t')[1])
            act = re.split("[\t@ ]",event[0])[2]
            log_dict['concept:name'].append(act)
            ev_variables = []
            for i in range(1, len(event)):
                variable = re.split('[{ = }{\n}]', event[i])
                variable_name = variable[2]
                variable_value = variable[-2]
                log_dict[variable_name].append(variable_value)
                ev_variables.append(variable_name)
            for v in self.variables:
                if v not in ev_variables:
                    log_dict[v].append(None)

        data_table = pd.DataFrame(log_dict)
        data_table['concept:name'] = data_table['concept:name'].apply(lambda x: ' '.join(x.split('_')[:-1]) if x.split('_')[-1].isnumeric() else x.replace('_', ' '))        
        data_table = data_table.loc[data_table['concept:name'].apply(lambda x: x in self.activities),:]

        for v in self.variables_to_delete:
            del data_table[v]

        cases = data_table[self.case_names].apply(lambda x: None if x==None else int(x[3:-1]))
        data_table['case:concept:name'] = cases

        del data_table[self.case_names]

        data_table.index = range(len(data_table))

        return data_table
    
    def to_csv(self, path_name):
        self.data_table.to_csv(path_name, index = False)