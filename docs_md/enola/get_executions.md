Module enola.get_executions
===========================

Classes
-------

`GetExecutions(token: str, raise_error_if_fail=True)`
:   Start Executions Execution
    
    token: jwt token, this is used to identify the agent, request from Admin App

    ### Methods

    `get(self, key, default=None)`
    :

    `get_next_page(self)`
    :

    `get_page_number(self)`
    :

    `query(self, date_from: str, date_to: str, chamber_id_list: list = [], agent_id_list: list = [], agent_deploy_id_list: list = [], user_id_list: list = [], session_id_list: list = [], channel_id_list: list = [], data_filter_list: list = [], eval_id_user: enola.enola_types.ExecutionEvalFilter = None, eval_id_internal: enola.enola_types.ExecutionEvalFilter = None, eval_id_auto: enola.enola_types.ExecutionEvalFilter = None, environment_id: enola.enola_types.Environtment = None, is_test_plan: bool = None, finished: bool = None, limit: int = 100, include_tags: bool = False, include_data: bool = False, include_errors: bool = False, include_evals: bool = False) ‑> enola.enola_types.ExecutionModel`
    :   Get Items by Chamber
        
        date_from: str, date from
        date_to: str, date to
        chamber_id: list, chamber id
        agent_id: list, agent id
        agent_deploy_id: list, agent deploy id
        user_id: list, user id
        session_id: list, session id
        channel_id: list, channel id
        data_filter: list, data filter
        eval_id_user: ExecutionEvalFilter, eval id user
        eval_id_internal: ExecutionEvalFilter, eval id internal
        eval_id_auto: ExecutionEvalFilter, eval id auto
        environment_id: Environtment, environment id
        is_test_plan: bool, is test plan
        finished: bool, finished
        limit: int, 100 is default limit
        include_tags: bool, include tags
        include_data: bool, include data
        include_errors: bool, include errors
        include_evals: bool, include evals