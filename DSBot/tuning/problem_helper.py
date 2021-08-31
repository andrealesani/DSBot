import pandas as pd


class SolutionDetails:
    def __init__(self, problem, pipeline, relevant_param, sentence):
        self.problem = problem
        self.pipeline = pipeline
        self.relevant_param = relevant_param
        self.sentence = sentence


def get_data(problem, pipeline) -> SolutionDetails:
    # TODO(giubots): refine, and handle errors
    df = pd.read_csv("problem_kb.csv", sep=";")
    query = df.query(f'problemKeyword == "{problem}" & pipeline == "{pipeline}"')
    param = query["param"]
    sentence = query["sentence"]
    return SolutionDetails(problem, pipeline, param.values[0], sentence.values[0])
