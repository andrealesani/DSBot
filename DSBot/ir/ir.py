
def run(ir, results):
    if len(ir) == 1:
        ir[0].run(results)
    else:
        run(ir[1:], ir[0].run(results))


def create_IR(pipeline):
    dict_pipeline = []
    package = importlib.import_module('ir')
    for i in pipeline:
        dict_pipeline.append(getattr(package, pipeline[i])(results))

