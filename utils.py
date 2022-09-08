def get_params_from_strategy_result(strategy_result):
    params = strategy_result.params
    return dict(params._getkwargs())
