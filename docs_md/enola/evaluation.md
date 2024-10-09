Module enola.evaluation
=======================

Classes
-------

`Evaluation(token, eval_type: enola.enola_types.EvalType = EvalType.AUTO, result_score: enola.enola_types.ResultScore = None, result_llm: enola.enola_types.ResultLLM = None, app_id=None, user_id=None, session_id=None, channel_id=None, ip=None, app_name: str = '', user_name: str = '', session_name: str = '', channel_name: str = '')`
:   Start Evaluation Execution
    
    token: jwt token, this is used to identify the agent, request from Admin App
    eval_type: type of evaluation, AUTO (ML or AI evaluator), USER (final user), INTERNAL (internal expert)
    result_score: reaactual results of score
    result_llm: actual results of llm
    app_id: id of app, this is used to identify the app who is calling
    app_name: name of app, this is used to identify the app who is calling
    user_id: id of external user, this is used to identify the user who is calling
    user_name: name of external user, this is used to identify the user who is calling
    session_id: id of session of user or application, this is used to identify the session who is calling
    channel_id: web, chat, whatsapp, etc, this is used to identify the channel who is calling
    channel_name: web, chat, whatsapp, etc, this is used to identify the channel who is calling
    ip: ip of user or application, this is used to identify the ip who is calling

    ### Methods

    `add_evaluation(self, enola_id: str, eval_id: str, value: float, comment: str)`
    :   Add Evaluation by value
        enola_id: id of enola
        eval_id: id of evaluation
        value: value of evaluation
        comment: comment of evaluation

    `add_evaluation_by_level(self, enola_id: str, eval_id: str, level: int, comment: str)`
    :   Add Evaluation by level
        enola_id: id of enola
        eval_id: id of evaluation
        level: 1 to 5
        comment: comment of evaluation

    `execute(self)`
    :   Execute Evaluations

    `execution_exists(self, enola_id: str)`
    :   Check if execution exists
        enola_id: id of enola

    `get(self, key, default=None)`
    :