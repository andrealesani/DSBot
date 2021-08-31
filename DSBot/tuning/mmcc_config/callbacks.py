from mmcc_framework import Response


# TODO(giubots): implement

def start(data, kb, context, activity):
    return Response(kb, context, True)


def choose_problem(data, kb, context, activity):
    return Response(kb, context, True)


def edit_param(data, kb, context, activity):
    return Response(kb, context, True)


my_callbacks = {
    "start": start,
    "choose_problem": choose_problem,
    "edit_param": edit_param,
}
