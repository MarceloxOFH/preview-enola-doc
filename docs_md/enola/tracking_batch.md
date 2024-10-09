Module enola.tracking_batch
===========================

Classes
-------

`TrackingBatch(token, name, dataframe, period: str, client_id_column_name: str, product_id_column_name: str, score_value_column_name: str, score_group_column_name: str, score_cluster_column_name: str, channel_id_column_name: str = None, channel_name_column_name: str = None, session_id_column_name: str = None, session_name_column_name: str = None, user_id_column_name: str = None, user_name_column_name: str = None, app_id_column_name: str = None, app_name_column_name: str = None, ip_column_name: str = None, external_id_column_name: str = None, app_id=None, app_name: str = '', user_id=None, user_name: str = '', session_id=None, session_name: str = '', channel_id=None, channel_name: str = '', ip=None, is_test=False)`
:   Start tracking Batch Execution
    
    token: jwt token, this is used to identify the agent, request from Admin App
    name: name of this execution
    dataframe: dataframe to track
    period: period of this execution in iso-format (2021-01-01T00:00:00Z)
    client_id_column_name: name of column with client id
    product_id_column_name: name of column with product id
    score_value_column_name: name of column with score value
    score_group_column_name: name of column with score group
    score_cluster_column_name: name of column with score cluster
    channel_id_column_name: name of column with channel id
    channel_name_column_name: name of column with channel name
    session_id_column_name: name of column with session id
    session_name_column_name: name of column with session name
    user_id_column_name: name of column with user id
    user_name_column_name: name of column with user name
    app_id_column_name: name of column with app id
    app_name_column_name: name of column with app name
    ip_column_name: name of column with ip
    app_id: id of app, this is used to identify the app who is calling
    app_name: name of app, this is used to identify the app who is calling
    user_id: id of external user, this is used to identify the user who is calling
    user_name: name of external user, this is used to identify the user who is calling
    session_id: id of session of user or application, this is used to identify the session who is calling
    session_name: name of session of user or application, this is used to identify the session who is calling
    channel_id: web, chat, whatsapp, etc, this is used to identify the channel who is calling
    channel_name: web, chat, whatsapp, etc, this is used to identify the channel who is calling
    ip: ip of user or application, this is used to identify the ip who is calling
    is_test: true if this call is for testing purposes

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

    `add_tag(self, key: str, value)`
    :   add tag to tracking, this tag is used to search in Enola App

    `add_warning(self, id: str, message: str, kind: enola.enola_types.ErrOrWarnKind)`
    :   register warning to tracking

    `execute(self, batch_size=200) ‑> List[enola.enola_types.TrackingResponseModel]`
    :   register tracking batch in Enola server

    `get(self, key, default=None)`
    :