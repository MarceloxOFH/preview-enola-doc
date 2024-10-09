Module enola.tracking
=====================

Classes
-------

`Tracking(token, name, app_id=None, user_id=None, session_id=None, channel_id=None, ip=None, external_id=None, is_test=False, message_input: str = '', enola_id_prev: str = '', app_name: str = '', user_name: str = '', session_name: str = '', channel_name: str = '', client_id: str = '', product_id: str = '')`
:   Start tracking Execution
    
    token: jwt token, this is used to identify the agent, request from Admin App
    name: name of this execution
    message_input: message received from user or to explain the execution
    app_id: id of app, this is used to identify the app who is calling
    user_id: id of external user, this is used to identify the user who is calling
    session_id: id of session of user or application, this is used to identify the session who is calling
    channel_id: web, chat, whatsapp, etc, this is used to identify the channel who is calling
    ip: ip of user or application, this is used to identify the ip who is calling
    external_id: external id, this is used to identify unique records
    is_test: true if this call is for testing purposes
    enola_id_prev: id of previous call, this is used to link agents sequence

    ### Methods

    `add_custom_info(self, key, value)`
    :   add custom information to tracking

    `add_data_received(self, name: str, data, type: enola.enola_types.DataType)`
    :   add data received from user

    `add_data_send(self, name: str, data, type: enola.enola_types.DataType)`
    :   add data to send to user

    `add_error(self, id: str, message: str, kind: enola.enola_types.ErrOrWarnKind)`
    :   register error to tracking

    `add_extra_info(self, key: str, value)`
    :   add extra information to tracking, this can be used to test or debug

    `add_file_link(self, name: str, url: str, type: str, size_kb: int)`
    :   add file link to tracking

    `add_tag(self, key: str, value)`
    :   add tag to tracking, this tag is used to search in Enola App

    `add_warning(self, id: str, message: str, kind: enola.enola_types.ErrOrWarnKind)`
    :   register warning to tracking

    `close_step_audio(self, step: enola.enola_types.Step, successfull: bool, message_output: str = '', audio_num: int = 0, audio_sec: int = 0, audio_size: int = 0, audio_cost: float = 0, enola_id_prev: str = '', agent_deploy_id: str = '', step_id: str = '')`
    :   close step with audio information
        
        enola_id_prev: If this step was a call to another Enola agent, whether from your own company or another, this is the ID of that agent
        agent_deploy_id: include this if you want to link this step to another agent of another company
        step_id: id of this step, you can use it to link with external calls
        message_output: message to user or to explain the execution results

    `close_step_doc(self, step: enola.enola_types.Step, successfull: bool, message_output: str = '', doc_num: int = 0, doc_pages: int = 0, doc_size: int = 0, doc_char: int = 0, doc_cost: float = 0, enola_id_prev: str = '', agent_deploy_id: str = '', step_id: str = '')`
    :   close step with doc information
        
        enola_id_prev: If this step was a call to another Enola agent, whether from your own company or another, this is the ID of that agent
        agent_deploy_id: include this if you want to link this step to another agent of another company
        step_id: id of this step, you can use it to link with external calls
        message_output: message to user or to explain the execution results

    `close_step_image(self, step: enola.enola_types.Step, successfull: bool, message_output: str = '', image_num: int = 0, image_size: int = 0, image_cost: float = 0, enola_id_prev: str = '', agent_deploy_id: str = '', step_id: str = '')`
    :   close step with image information
        
        enola_id_prev: If this step was a call to another Enola agent, whether from your own company or another, this is the ID of that agent
        agent_deploy_id: include this if you want to link this step to another agent of another company
        step_id: id of this step, you can use it to link with external calls
        message_output: message to user or to explain the execution results

    `close_step_others(self, step: enola.enola_types.Step, successfull: bool, message_output: str = '', others_cost: float = 0, enola_id_prev: str = '', agent_deploy_id: str = '', step_id: str = '')`
    :   close step with others information
        
        enola_id_prev: If this step was a call to another Enola agent, whether from your own company or another, this is the ID of that agent
        agent_deploy_id: include this if you want to link this step to another agent of another company
        step_id: id of this step, you can use it to link with external calls
        message_output: message to user or to explain the execution results

    `close_step_score(self, step: enola.enola_types.Step, successfull: bool, message_output: str = '', others_cost: float = 0, enola_id_prev: str = '', agent_deploy_id: str = '', step_id: str = '')`
    :   close step for Score
        
        enola_id_prev: If this step was a call to another Enola agent, whether from your own company or another, this is the ID of that agent
        agent_deploy_id: include this if you want to link this step to another agent of another company
        step_id: id of this step, you can use it to link with external calls
        message_output: message to user or to explain the execution results

    `close_step_token(self, step: enola.enola_types.Step, successfull: bool, message_output: str = '', token_input_num: int = 0, token_output_num: int = 0, token_total_num: int = 0, token_input_cost: float = 0, token_output_cost: float = 0, token_total_cost: float = 0, enola_id: str = '', agent_deploy_id: str = '', step_id: str = '')`
    :   close step with token information
        enola_id: If this step was a call to another Enola agent, whether from your own company or another, this is the ID of that agent
        agent_deploy_id: include this if you want to link this step to another agent of another company
        step_id: id of this step, you can use it to link with external calls
        message_output: message to user or to explain the execution results

    `close_step_video(self, step: enola.enola_types.Step, successfull: bool, message_output: str = '', video_num: int = 0, video_sec: int = 0, video_size: int = 0, video_cost: float = 0, enola_id_prev: str = '', agent_deploy_id: str = '', step_id: str = '')`
    :   close step with video information
        
        enola_id_prev: If this step was a call to another Enola agent, whether from your own company or another, this is the ID of that agent
        agent_deploy_id: include this if you want to link this step to another agent of another company
        step_id: id of this step, you can use it to link with external calls
        message_output: message to user or to explain the execution results

    `execute(self, successfull: bool, message_output: str = '', num_iteratons: int = 0, score_value=0, score_group='', score_cluster='', score_date='', external_id='') ‑> bool`
    :   register tracking in Enola server
        successfull: true for your Agent execution OK, false for error in your Agent execution
        message_output: message to user or to explain the execution results
        num_iteratons: number of iterations
        score_value: score value
        score_group: score group
        score_cluster: score cluster
        score_date: date of score in ISO & UTC format (example: yyyy-MM-ddTHH:mm:ss:SSSz). Empty for current date

    `get(self, key, default=None)`
    :

    `new_step(self, name: str, message_input: str = '')`
    :   start new step
        name: name of this step
        message_input: message received from user or to explain the execution