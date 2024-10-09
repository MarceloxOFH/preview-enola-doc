Module enola.enola_types
========================

Classes
-------

`ApiDataModel(name: str, method: str, url: str, body: str, header: str, payload: str, description: str)`
:   

    ### Methods

    `get(self, key, default=None)`
    :

    `to_json(self)`
    :

`CompareType(*args, **kwds)`
:   Create a collection of name/value pairs.
    
    Example enumeration:
    
    >>> class Color(Enum):
    ...     RED = 1
    ...     BLUE = 2
    ...     GREEN = 3
    
    Access them by:
    
    - attribute access:
    
      >>> Color.RED
      <Color.RED: 1>
    
    - value lookup:
    
      >>> Color(1)
      <Color.RED: 1>
    
    - name lookup:
    
      >>> Color['RED']
      <Color.RED: 1>
    
    Enumerations can be iterated over, and know how many members they have:
    
    >>> len(Color)
    3
    
    >>> list(Color)
    [<Color.RED: 1>, <Color.BLUE: 2>, <Color.GREEN: 3>]
    
    Methods can be added to enumerations, and members can have their own
    attributes -- see the documentation for details.

    ### Ancestors (in MRO)

    * enum.Enum

    ### Class variables

    `CONTAINS`
    :

    `EQUAL`
    :

    `GREATER`
    :

    `GREATER_EQUAL`
    :

    `LESS`
    :

    `LESS_EQUAL`
    :

    `NOT_EQUAL`
    :

`DataListModel(kind: enola.enola_types.KindType, name: str, data_type: enola.enola_types.DataType, value)`
:   

    ### Methods

    `get(self, key, default=None)`
    :

    `to_json(self)`
    :

`DataType(*args, **kwds)`
:   Create a collection of name/value pairs.
    
    Example enumeration:
    
    >>> class Color(Enum):
    ...     RED = 1
    ...     BLUE = 2
    ...     GREEN = 3
    
    Access them by:
    
    - attribute access:
    
      >>> Color.RED
      <Color.RED: 1>
    
    - value lookup:
    
      >>> Color(1)
      <Color.RED: 1>
    
    - name lookup:
    
      >>> Color['RED']
      <Color.RED: 1>
    
    Enumerations can be iterated over, and know how many members they have:
    
    >>> len(Color)
    3
    
    >>> list(Color)
    [<Color.RED: 1>, <Color.BLUE: 2>, <Color.GREEN: 3>]
    
    Methods can be added to enumerations, and members can have their own
    attributes -- see the documentation for details.

    ### Ancestors (in MRO)

    * enum.Enum

    ### Class variables

    `BOOLEAN`
    :

    `DATE`
    :

    `NUMBER`
    :

    `TEXT`
    :

`EnolaSenderModel(app_id: str, app_name: str, user_id: str, user_name: str, session_id: str, session_name: str, channel_id: str, channel_name: str, client_id: str, product_id: str, external_id: str, batch_id: str, ip: str)`
:   EnolaSenderModel

    ### Methods

    `get(self, key, default=None)`
    :

`Environtment(*args, **kwds)`
:   Create a collection of name/value pairs.
    
    Example enumeration:
    
    >>> class Color(Enum):
    ...     RED = 1
    ...     BLUE = 2
    ...     GREEN = 3
    
    Access them by:
    
    - attribute access:
    
      >>> Color.RED
      <Color.RED: 1>
    
    - value lookup:
    
      >>> Color(1)
      <Color.RED: 1>
    
    - name lookup:
    
      >>> Color['RED']
      <Color.RED: 1>
    
    Enumerations can be iterated over, and know how many members they have:
    
    >>> len(Color)
    3
    
    >>> list(Color)
    [<Color.RED: 1>, <Color.BLUE: 2>, <Color.GREEN: 3>]
    
    Methods can be added to enumerations, and members can have their own
    attributes -- see the documentation for details.

    ### Ancestors (in MRO)

    * enum.Enum

    ### Class variables

    `DEV`
    :

    `PROD`
    :

    `QA`
    :

`ErrOrWarnKind(*args, **kwds)`
:   EXTERNAL: external agent call generate an unexpected error or warning

    ### Ancestors (in MRO)

    * enum.Enum

    ### Class variables

    `EXTERNAL`
    :   INTERNAL_CONTROLLED: internal agent call generate an unexpected error or warning

    `INTERNAL_CONTROLLED`
    :   INTERNAL_TOUSER: controlled error or warning to send to user

    `INTERNAL_TOUSER`
    :

`ErrorOrWarnModel(id: str, message: str, error_type: enola.enola_types.ErrorType, kind: enola.enola_types.ErrOrWarnKind)`
:   

    ### Methods

    `get(self, key, default=None)`
    :

    `to_json(self)`
    :

`ErrorType(*args, **kwds)`
:   Create a collection of name/value pairs.
    
    Example enumeration:
    
    >>> class Color(Enum):
    ...     RED = 1
    ...     BLUE = 2
    ...     GREEN = 3
    
    Access them by:
    
    - attribute access:
    
      >>> Color.RED
      <Color.RED: 1>
    
    - value lookup:
    
      >>> Color(1)
      <Color.RED: 1>
    
    - name lookup:
    
      >>> Color['RED']
      <Color.RED: 1>
    
    Enumerations can be iterated over, and know how many members they have:
    
    >>> len(Color)
    3
    
    >>> list(Color)
    [<Color.RED: 1>, <Color.BLUE: 2>, <Color.GREEN: 3>]
    
    Methods can be added to enumerations, and members can have their own
    attributes -- see the documentation for details.

    ### Ancestors (in MRO)

    * enum.Enum

    ### Class variables

    `ERROR`
    :

    `WARNING`
    :

`EvalType(*args, **kwds)`
:   Create a collection of name/value pairs.
    
    Example enumeration:
    
    >>> class Color(Enum):
    ...     RED = 1
    ...     BLUE = 2
    ...     GREEN = 3
    
    Access them by:
    
    - attribute access:
    
      >>> Color.RED
      <Color.RED: 1>
    
    - value lookup:
    
      >>> Color(1)
      <Color.RED: 1>
    
    - name lookup:
    
      >>> Color['RED']
      <Color.RED: 1>
    
    Enumerations can be iterated over, and know how many members they have:
    
    >>> len(Color)
    3
    
    >>> list(Color)
    [<Color.RED: 1>, <Color.BLUE: 2>, <Color.GREEN: 3>]
    
    Methods can be added to enumerations, and members can have their own
    attributes -- see the documentation for details.

    ### Ancestors (in MRO)

    * enum.Enum

    ### Class variables

    `AUTO`
    :

    `INTERNAL`
    :

    `USER`
    :

`EvaluationDetailModel(eval_id: str, comment: str, value: float = None, level: int = None)`
:   EvaluationDetailModel

    ### Methods

    `get(self, key, default=None)`
    :

`EvaluationModel(enola_id: str, eval_type: enola.enola_types.EvalType, enola_sender: enola.enola_types.EnolaSenderModel, result_score: enola.enola_types.ResultScore = None, result_llm: enola.enola_types.ResultLLM = None)`
:   EvaluationModel

    ### Methods

    `add_eval(self, eval: enola.enola_types.EvaluationDetailModel)`
    :

    `get(self, key, default=None)`
    :

    `to_json(self)`
    :

`EvaluationResponseModel(enola_id: str = '', agent_deploy_id: str = '', enola_eval_id: str = '', successfull: bool = True, message: str = '', **args)`
:   

    ### Methods

    `get(self, key, default=None)`
    :

    `to_json(self)`
    :

`EvaluationResultModel(total_evals: int, total_errors: int, total_success: int, errors: list)`
:   

    ### Methods

    `get(self, key, default=None)`
    :

`ExecutionDataFilter(name: str, value, type: enola.enola_types.DataType = DataType.TEXT, compare: enola.enola_types.CompareType = CompareType.EQUAL)`
:   

    ### Methods

    `get(self, key, default=None)`
    :

    `to_json(self)`
    :

`ExecutionEvalFilter(eval_id: list, include: bool = True)`
:   

    ### Methods

    `get(self, key, default=None)`
    :

`ExecutionModel(data: list, successfull: bool, message: str, **args)`
:   

    ### Methods

    `get(self, key, default=None)`
    :

`ExecutionQueryModel(date_from: str, date_to: str, chamber_id_list: list = [], agent_id_list: list = [], agent_deploy_id_list: list = [], user_id_list: list = [], session_id_list: list = [], channel_id_list: list = [], data_filter_list: list = [], eval_id_user: enola.enola_types.ExecutionEvalFilter = None, eval_id_internal: enola.enola_types.ExecutionEvalFilter = None, eval_id_auto: enola.enola_types.ExecutionEvalFilter = None, environment_id: enola.enola_types.Environtment = None, is_test_plan: bool = None, finished: bool = None, limit: int = 100, page_number: int = 1, include_tags: bool = False, include_data: bool = False, include_errors: bool = False, include_evals: bool = False)`
:   

    ### Methods

    `get(self, key, default=None)`
    :

`ExecutionResponseModel(agentExecId: str, agentExecIdRelated: str, agentDeployId: str, agentDeployName: str, agentId: str, agentName: str, agentExecName: str, agentExecStartDT: str, agentExecEndDT: str, agentExecDurationMs: int, agentExecNumTracking: str, agentExecIsTest: bool, environmentId: str, agentExecCliAppId: str, agentExecCliAppName: str, agentExecCliUserId: str, agentExecCliUserName: str, agentExecCliSessionId: str, agentExecCliSessionName: str, agentExecCliChannel: str, agentExecCliChannelName: str, agentExecMessageInput: str, agentExecMessageOutput: str, agentExecTagJson: <module 'json' from 'C:\\Users\\Marcelo\\AppData\\Local\\Programs\\Python\\Python312\\Lib\\json\\__init__.py'>, agentExecFileInfoJson: <module 'json' from 'C:\\Users\\Marcelo\\AppData\\Local\\Programs\\Python\\Python312\\Lib\\json\\__init__.py'>, agentExecDataJson: <module 'json' from 'C:\\Users\\Marcelo\\AppData\\Local\\Programs\\Python\\Python312\\Lib\\json\\__init__.py'>, agentExecErrorOrWarningJson: <module 'json' from 'C:\\Users\\Marcelo\\AppData\\Local\\Programs\\Python\\Python312\\Lib\\json\\__init__.py'>, agentExecStepApiDataJson: <module 'json' from 'C:\\Users\\Marcelo\\AppData\\Local\\Programs\\Python\\Python312\\Lib\\json\\__init__.py'>, agentExecInfoJson: <module 'json' from 'C:\\Users\\Marcelo\\AppData\\Local\\Programs\\Python\\Python312\\Lib\\json\\__init__.py'>, agentExecEvals: <module 'json' from 'C:\\Users\\Marcelo\\AppData\\Local\\Programs\\Python\\Python312\\Lib\\json\\__init__.py'>, agentExecCliIP: str, agentExecCliNumIter: int, agentExecCliCodeApi: str, agentExecSuccessfull: bool, **args)`
:   

    ### Methods

    `get(self, key, default=None)`
    :

`FileInfoModel(name: str, url: str, type: str, sizeKb: int, description: str)`
:   

    ### Methods

    `get(self, key, default=None)`
    :

    `to_json(self)`
    :

`Info(type: str, key: str, value)`
:   

    ### Methods

    `get(self, key, default=None)`
    :

    `is_dict(self, value)`
    :

    `is_numeric(self, value)`
    :

    `is_string(self, value)`
    :

    `to_json(self)`
    :

`KindType(*args, **kwds)`
:   Create a collection of name/value pairs.
    
    Example enumeration:
    
    >>> class Color(Enum):
    ...     RED = 1
    ...     BLUE = 2
    ...     GREEN = 3
    
    Access them by:
    
    - attribute access:
    
      >>> Color.RED
      <Color.RED: 1>
    
    - value lookup:
    
      >>> Color(1)
      <Color.RED: 1>
    
    - name lookup:
    
      >>> Color['RED']
      <Color.RED: 1>
    
    Enumerations can be iterated over, and know how many members they have:
    
    >>> len(Color)
    3
    
    >>> list(Color)
    [<Color.RED: 1>, <Color.BLUE: 2>, <Color.GREEN: 3>]
    
    Methods can be added to enumerations, and members can have their own
    attributes -- see the documentation for details.

    ### Ancestors (in MRO)

    * enum.Enum

    ### Class variables

    `RECEIVER`
    :

    `SENDER`
    :

`ResultLLM(message_output_best: str)`
:   

    ### Methods

    `get(self, key, default=None)`
    :

    `to_json(self)`
    :

`ResultScore(value_actual: float, group_actual: str, cluster_actual: str, value_dif: float, group_dif: str, cluster_dif: str)`
:   

    ### Methods

    `get(self, key, default=None)`
    :

    `to_json(self)`
    :

`Step(name: str, message_input: str = '')`
:   

    ### Methods

    `add_api_data(self, bodyToSend: str, payloadReceived: str, name: str, method: str, url: str, description: str = '', headerToSend: str = '')`
    :

    `add_error(self, id: str, message: str, kind: enola.enola_types.ErrOrWarnKind)`
    :

    `add_extra_info(self, key: str, value)`
    :

    `add_file_link(self, name: str, url: str, type: str, size_kb: int, description: str = '')`
    :

    `add_tag(self, key: str, value)`
    :

    `add_warning(self, id: str, message: str, kind: enola.enola_types.ErrOrWarnKind)`
    :

    `get(self, key, default=None)`
    :

    `set_score(self, value: int, group: str, cluster: str, date: str = '')`
    :   Set score for step
        value: score value
        group: score group
        cluster: score cluster
        date: date of score in ISO & UTC format (example: yyyy-MM-ddTHH:mm:ss:SSSz). Empty for current date

    `to_json(self)`
    :

`StepAudio()`
:   

    ### Methods

    `get(self, key, default=None)`
    :

`StepCost()`
:   

    ### Methods

    `get(self, key, default=None)`
    :

`StepDoc()`
:   

    ### Methods

    `get(self, key, default=None)`
    :

`StepImage()`
:   

    ### Methods

    `get(self, key, default=None)`
    :

`StepToken()`
:   

    ### Methods

    `get(self, key, default=None)`
    :

`StepType(*args, **kwds)`
:   Create a collection of name/value pairs.
    
    Example enumeration:
    
    >>> class Color(Enum):
    ...     RED = 1
    ...     BLUE = 2
    ...     GREEN = 3
    
    Access them by:
    
    - attribute access:
    
      >>> Color.RED
      <Color.RED: 1>
    
    - value lookup:
    
      >>> Color(1)
      <Color.RED: 1>
    
    - name lookup:
    
      >>> Color['RED']
      <Color.RED: 1>
    
    Enumerations can be iterated over, and know how many members they have:
    
    >>> len(Color)
    3
    
    >>> list(Color)
    [<Color.RED: 1>, <Color.BLUE: 2>, <Color.GREEN: 3>]
    
    Methods can be added to enumerations, and members can have their own
    attributes -- see the documentation for details.

    ### Ancestors (in MRO)

    * enum.Enum

    ### Class variables

    `AUDIO`
    :

    `DOCUMENT`
    :

    `IMAGE`
    :

    `OTHER`
    :

    `SCORE`
    :

    `TOKEN`
    :

    `VIDEO`
    :

`StepVideo()`
:   

    ### Methods

    `get(self, key, default=None)`
    :

`TokenInfo(token: str)`
:   

    ### Methods

    `get(self, key, default=None)`
    :

`TrackingBatchDetailResponseModel(agent_deploy_id: str = '', successfull: bool = None, message: str = '', tracking_list: List[enola.enola_types.TrackingResponseModel] = [], **args)`
:   

    ### Methods

    `get(self, key, default=None)`
    :

`TrackingBatchHeadModel(name: str, period: str, total_rows: int, is_test: bool, enola_sender: enola.enola_types.EnolaSenderModel)`
:   TrackingBatchHeadModel

    ### Methods

    `get(self, key, default=None)`
    :

    `to_json(self)`
    :

`TrackingBatchHeadResponseModel(batch_id: str = '', agent_deploy_id: str = '', successfull: bool = None, message: str = '', **args)`
:   

    ### Methods

    `get(self, key, default=None)`
    :

    `to_json(self)`
    :

`TrackingModel(isTest: bool, step_list: List[enola.enola_types.Step], steps: int, enola_id_prev: str, enola_sender: enola.enola_types.EnolaSenderModel)`
:   TrackingModel

    ### Methods

    `get(self, key, default=None)`
    :

    `to_json(self)`
    :

`TrackingResponseModel(successfull: bool = None, enola_id: str = '', agent_deploy_id: str = '', message: str = '', url_evaluation_def_get: str = '', url_evaluation_post: str = '', **args)`
:   

    ### Methods

    `get(self, key, default=None)`
    :

    `to_json(self)`
    :