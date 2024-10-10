from enola.base.common.huemul_functions import HuemulFunctions
from enola.base.internal.tracking_batch.enola_tracking_batch import (
    create_tracking,
    create_tracking_batch_head,
)
from enola.base.common.auth.auth_model import AuthModel
from enola.enola_types import (
    EnolaSenderModel,
    KindType,
    DataListModel,
    DataType,
    ErrOrWarnKind,
    Info,
    TokenInfo,
    TrackingBatchHeadModel,
    TrackingModel,
    TrackingResponseModel,
    Step,
    StepType,
)
from enola.base.connect import Connect
from typing import List, Optional


class TrackingBatch:
    """
    The `TrackingBatch` class is used to perform batch tracking execution in Enola.

    This class allows you to send batch tracking data to the Enola server, handling large
    dataframes by sending them in batches. It manages authentication, data preparation,
    and communication with the Enola API.

    Example usage:

    ```python
    tracking_batch = TrackingBatch(
        token="your_jwt_token",
        name="BatchExecutionName",
        dataframe=df,
        period="2021-01-01T00:00:00Z",
        client_id_column_name="client_id",
        product_id_column_name="product_id",
        score_value_column_name="score_value",
        score_group_column_name="score_group",
        score_cluster_column_name="score_cluster",
        app_id="App123",
        user_id="User456",
        is_test=False
    )
    tracking_batch.execute()
    ```
    """

    def __init__(
        self,
        token: str,
        name: str,
        dataframe,
        period: str,
        client_id_column_name: str,
        product_id_column_name: str,
        score_value_column_name: Optional[str] = None,
        score_group_column_name: Optional[str] = None,
        score_cluster_column_name: Optional[str] = None,
        channel_id_column_name: Optional[str] = None,
        channel_name_column_name: Optional[str] = None,
        session_id_column_name: Optional[str] = None,
        session_name_column_name: Optional[str] = None,
        user_id_column_name: Optional[str] = None,
        user_name_column_name: Optional[str] = None,
        app_id_column_name: Optional[str] = None,
        app_name_column_name: Optional[str] = None,
        ip_column_name: Optional[str] = None,
        external_id_column_name: Optional[str] = None,
        app_id: Optional[str] = None,
        app_name: str = "",
        user_id: Optional[str] = None,
        user_name: str = "",
        session_id: Optional[str] = None,
        session_name: str = "",
        channel_id: Optional[str] = None,
        channel_name: str = "",
        ip: Optional[str] = None,
        is_test: bool = False,
    ):
        """
        Initializes a new instance of the TrackingBatch class.

        Args:
            token (str): JWT token used to identify the agent. Request this from the Admin App.
            name (str): Name of this execution.
            dataframe: Pandas DataFrame containing the data to track.
            period (str): Period of this execution in ISO format (e.g., '2021-01-01T00:00:00Z').
            client_id_column_name (str): Name of the column with client ID.
            product_id_column_name (str): Name of the column with product ID.
            score_value_column_name (str, optional): Name of the column with score value.
            score_group_column_name (str, optional): Name of the column with score group.
            score_cluster_column_name (str, optional): Name of the column with score cluster.
            channel_id_column_name (str, optional): Name of the column with channel ID.
            channel_name_column_name (str, optional): Name of the column with channel name.
            session_id_column_name (str, optional): Name of the column with session ID.
            session_name_column_name (str, optional): Name of the column with session name.
            user_id_column_name (str, optional): Name of the column with user ID.
            user_name_column_name (str, optional): Name of the column with user name.
            app_id_column_name (str, optional): Name of the column with app ID.
            app_name_column_name (str, optional): Name of the column with app name.
            ip_column_name (str, optional): Name of the column with IP address.
            external_id_column_name (str, optional): Name of the column with external ID.
            app_id (str, optional): ID of the app making the call.
            app_name (str, optional): Name of the app making the call.
            user_id (str, optional): ID of the external user.
            user_name (str, optional): Name of the external user.
            session_id (str, optional): ID of the user or application session.
            session_name (str, optional): Name of the session.
            channel_id (str, optional): ID of the communication channel (e.g., 'web', 'chat', 'whatsapp').
            channel_name (str, optional): Name of the communication channel.
            ip (str, optional): IP address of the user or application.
            is_test (bool, optional): True if this call is for testing purposes.
        """
        self.name = name
        self.hf = HuemulFunctions()
        self.dataframe = dataframe
        self.client_id_column_name = client_id_column_name
        self.product_id_column_name = product_id_column_name
        self.score_value_column_name = score_value_column_name
        self.score_group_column_name = score_group_column_name
        self.score_cluster_column_name = score_cluster_column_name
        self.channel_id_column_name = channel_id_column_name
        self.channel_name_column_name = channel_name_column_name
        self.session_id_column_name = session_id_column_name
        self.session_name_column_name = session_name_column_name
        self.user_id_column_name = user_id_column_name
        self.user_name_column_name = user_name_column_name
        self.app_id_column_name = app_id_column_name
        self.app_name_column_name = app_name_column_name
        self.ip_column_name = ip_column_name
        self.external_id_column_name = external_id_column_name
        self.period = period

        if dataframe is None:
            raise Exception("DataFrame is empty")
        if len(dataframe) == 0:
            raise Exception("DataFrame is empty (length is 0)")
        if score_value_column_name is None and score_group_column_name is None and score_cluster_column_name is None:
            raise Exception(
                "At least one of 'score_value_column_name', 'score_group_column_name', or 'score_cluster_column_name' must be provided"
            )
        if period is None or period == "":
            raise Exception("Period is empty")

        # Decode JWT token
        self.token_info = TokenInfo(token=token)

        if not self.token_info.is_service_account:
            raise Exception(
                "This token is not a service account. Only service accounts can execute tracking"
            )

        if not self.token_info.agent_deploy_id:
            raise Exception("agentDeployId is empty.")

        if not self.token_info.service_account_can_tracking:
            raise Exception("This service account can't execute tracking")

        self.agent_deploy_id = self.token_info.agent_deploy_id
        self.connection = Connect(
            AuthModel(
                jwt_token=token,
                url_service=self.token_info.service_account_url_backend,
                org_id=self.token_info.org_id,
            )
        )

        # User information
        self.enola_sender = EnolaSenderModel(
            app_id=app_id,
            app_name=app_name,
            user_id=user_id,
            user_name=user_name,
            session_id=session_id,
            session_name=session_name,
            channel_id=channel_id,
            channel_name=channel_name,
            ip=ip,
            external_id="",
            batch_id="",
            client_id="",
            product_id="",
        )

        # If is empty or not exist assign false
        self.is_test = is_test

        # Save steps and information
        self.batch_id = ""

    ########################################################################################
    ###############    A G E N T   M E T H O D S     #######################################
    ########################################################################################

    def add_data_received(self, name: str, data, type: DataType) -> None:
        """
        Adds data received from the user.

        Args:
            name (str): The name of the data.
            data: The data content.
            type (DataType): The type of data received.
        """
        self.first_step.agent_data_list.append(
            DataListModel(value=data, name=name, data_type=type, kind=KindType.RECEIVER)
        )

    def add_data_send(self, name: str, data, type: DataType) -> None:
        """
        Adds data to send to the user.

        Args:
            name (str): The name of the data.
            data: The data content.
            type (DataType): The type of data being sent.
        """
        self.first_step.agent_data_list.append(
            DataListModel(value=data, name=name, data_type=type, kind=KindType.SENDER)
        )

    def add_custom_info(self, key: str, value) -> None:
        """
        Adds custom information to tracking.

        Args:
            key (str): The key for the custom information.
            value: The value associated with the key.
        """
        self.first_step.info_list.append(Info(key, value))

    def add_tag(self, key: str, value) -> None:
        """
        Adds a tag to tracking, this tag is used to search in Enola App.

        Args:
            key (str): The tag key.
            value: The tag value.
        """
        self.first_step.add_tag(key=key, value=value)

    def add_extra_info(self, key: str, value) -> None:
        """
        Adds extra information to tracking, this can be used to test or debug.

        Args:
            key (str): The key for the extra information.
            value: The value associated with the key.
        """
        self.first_step.add_extra_info(key=key, value=value)

    def add_error(self, id: str, message: str, kind: ErrOrWarnKind) -> None:
        """
        Registers an error to tracking.

        Args:
            id (str): The error identifier.
            message (str): The error message.
            kind (ErrOrWarnKind): The kind of error.
        """
        self.first_step.add_error(id=id, message=message, kind=kind)

    def add_warning(self, id: str, message: str, kind: ErrOrWarnKind) -> None:
        """
        Registers a warning to tracking.

        Args:
            id (str): The warning identifier.
            message (str): The warning message.
            kind (ErrOrWarnKind): The kind of warning.
        """
        self.first_step.add_warning(id=id, message=message, kind=kind)

    def execute(self, batch_size: int = 200) -> List[TrackingResponseModel]:
        """
        Registers the tracking batch in the Enola server.

        Args:
            batch_size (int, optional): Number of records to send per batch. Defaults to 200.

        Returns:
            List[TrackingResponseModel]: List of tracking response models returned by the server.
        """

        # Create batch
        if self.batch_id == "":
            print(f"{self.name}: sending to server, create Batch... ")
            tracking_batch_model = TrackingBatchHeadModel(
                enola_sender=self.enola_sender,
                period=self.period,
                total_rows=len(self.dataframe),
                name=self.name,
                is_test=self.is_test,
            )

            tracking_batch = create_tracking_batch_head(
                tracking_batch_model=tracking_batch_model,
                connection=self.connection,
                raise_error_if_fail=False,
            )
            self.batch_id = tracking_batch.batch_id
            self.enola_sender.batch_id = self.batch_id

        # Start cycle to send all data
        print(f"{self.name}: sending to server, upload... ")
        # Show results
        if self.batch_id == "":
            print(f"{self.name}: finish with error, batch_id is empty")
            return []

        totalRows = len(self.dataframe)
        listToSend: List[TrackingModel] = []
        resultsList: List[TrackingResponseModel] = []
        # Iterate over the dataframe
        count_rows = 0
        for index, row in self.dataframe.iterrows():

            # Create step
            step = Step(
                name=self.name if (self.name != "") else "Prediction",
                message_input="",
            )

            # Add data to step in extra info
            for column in self.dataframe.columns:
                step.add_extra_info(column, row[column])

            if (
                self.score_cluster_column_name
                and self.score_cluster_column_name in self.dataframe.columns
            ):
                step.score_cluster = row[self.score_cluster_column_name]
                step.date_start = self.period
                step.date_end = self.period
            elif self.score_cluster_column_name:
                self.connection.huemul_logging.log_message_error(
                    message=f"{self.name}: column score_cluster_column_name '{self.score_cluster_column_name}' not found in dataframe"
                )
                raise Exception(
                    f"{self.name}: column score_cluster_column_name '{self.score_cluster_column_name}' not found in dataframe"
                )

            if (
                self.score_group_column_name
                and self.score_group_column_name in self.dataframe.columns
            ):
                step.score_group = row[self.score_group_column_name]
                step.date_start = self.period
                step.date_end = self.period
            elif self.score_group_column_name:
                self.connection.huemul_logging.log_message_error(
                    message=f"{self.name}: column score_group_column_name '{self.score_group_column_name}' not found in dataframe"
                )
                raise Exception(
                    f"{self.name}: column score_group_column_name '{self.score_group_column_name}' not found in dataframe"
                )

            if (
                self.score_value_column_name
                and self.score_value_column_name in self.dataframe.columns
            ):
                step.score_value = row[self.score_value_column_name]
                step.date_start = self.period
                step.date_end = self.period
            elif self.score_value_column_name:
                self.connection.huemul_logging.log_message_error(
                    message=f"{self.name}: column score_value_column_name '{self.score_value_column_name}' not found in dataframe"
                )
                raise Exception(
                    f"{self.name}: column score_value_column_name '{self.score_value_column_name}' not found in dataframe"
                )

            if (
                self.client_id_column_name
                and self.client_id_column_name in self.dataframe.columns
            ):
                self.enola_sender.client_id = row[self.client_id_column_name]
            elif self.client_id_column_name:
                self.connection.huemul_logging.log_message_error(
                    message=f"{self.name}: column client_id_column_name '{self.client_id_column_name}' not found in dataframe"
                )
                raise Exception(
                    f"{self.name}: column client_id_column_name '{self.client_id_column_name}' not found in dataframe"
                )

            if (
                self.product_id_column_name
                and self.product_id_column_name in self.dataframe.columns
            ):
                step.product_id = row[self.product_id_column_name]
            elif self.product_id_column_name:
                self.connection.huemul_logging.log_message_error(
                    message=f"{self.name}: column product_id_column_name '{self.product_id_column_name}' not found in dataframe"
                )
                raise Exception(
                    f"{self.name}: column product_id_column_name '{self.product_id_column_name}' not found in dataframe"
                )

            if (
                self.channel_id_column_name
                and self.channel_id_column_name in self.dataframe.columns
            ):
                self.enola_sender.channel_id = row[self.channel_id_column_name]
            elif self.channel_id_column_name:
                self.connection.huemul_logging.log_message_error(
                    message=f"{self.name}: column channel_id_column_name '{self.channel_id_column_name}' not found in dataframe"
                )
                raise Exception(
                    f"{self.name}: column channel_id_column_name '{self.channel_id_column_name}' not found in dataframe"
                )

            if (
                self.channel_name_column_name
                and self.channel_name_column_name in self.dataframe.columns
            ):
                self.enola_sender.channel_name = row[self.channel_name_column_name]
            elif self.channel_name_column_name:
                self.connection.huemul_logging.log_message_error(
                    message=f"{self.name}: column channel_name_column_name '{self.channel_name_column_name}' not found in dataframe"
                )
                raise Exception(
                    f"{self.name}: column channel_name_column_name '{self.channel_name_column_name}' not found in dataframe"
                )

            if (
                self.session_id_column_name
                and self.session_id_column_name in self.dataframe.columns
            ):
                self.enola_sender.session_id = row[self.session_id_column_name]
            elif self.session_id_column_name:
                self.connection.huemul_logging.log_message_error(
                    message=f"{self.name}: column session_id_column_name '{self.session_id_column_name}' not found in dataframe"
                )
                raise Exception(
                    f"{self.name}: column session_id_column_name '{self.session_id_column_name}' not found in dataframe"
                )

            if (
                self.session_name_column_name
                and self.session_name_column_name in self.dataframe.columns
            ):
                self.enola_sender.session_name = row[self.session_name_column_name]
            elif self.session_name_column_name:
                self.connection.huemul_logging.log_message_error(
                    message=f"{self.name}: column session_name_column_name '{self.session_name_column_name}' not found in dataframe"
                )
                raise Exception(
                    f"{self.name}: column session_name_column_name '{self.session_name_column_name}' not found in dataframe"
                )

            if (
                self.user_id_column_name
                and self.user_id_column_name in self.dataframe.columns
            ):
                self.enola_sender.user_id = row[self.user_id_column_name]
            elif self.user_id_column_name:
                self.connection.huemul_logging.log_message_error(
                    message=f"{self.name}: column user_id_column_name '{self.user_id_column_name}' not found in dataframe"
                )
                raise Exception(
                    f"{self.name}: column user_id_column_name '{self.user_id_column_name}' not found in dataframe"
                )

            if (
                self.user_name_column_name
                and self.user_name_column_name in self.dataframe.columns
            ):
                self.enola_sender.user_name = row[self.user_name_column_name]
            elif self.user_name_column_name:
                self.connection.huemul_logging.log_message_error(
                    message=f"{self.name}: column user_name_column_name '{self.user_name_column_name}' not found in dataframe"
                )
                raise Exception(
                    f"{self.name}: column user_name_column_name '{self.user_name_column_name}' not found in dataframe"
                )

            if (
                self.app_id_column_name
                and self.app_id_column_name in self.dataframe.columns
            ):
                self.enola_sender.app_id = row[self.app_id_column_name]
            elif self.app_id_column_name:
                self.connection.huemul_logging.log_message_error(
                    message=f"{self.name}: column app_id_column_name '{self.app_id_column_name}' not found in dataframe"
                )
                raise Exception(
                    f"{self.name}: column app_id_column_name '{self.app_id_column_name}' not found in dataframe"
                )

            if (
                self.app_name_column_name
                and self.app_name_column_name in self.dataframe.columns
            ):
                self.enola_sender.app_name = row[self.app_name_column_name]
            elif self.app_name_column_name:
                self.connection.huemul_logging.log_message_error(
                    message=f"{self.name}: column app_name_column_name '{self.app_name_column_name}' not found in dataframe"
                )
                raise Exception(
                    f"{self.name}: column app_name_column_name '{self.app_name_column_name}' not found in dataframe"
                )

            if (
                self.ip_column_name
                and self.ip_column_name in self.dataframe.columns
            ):
                self.enola_sender.ip = row[self.ip_column_name]
            elif self.ip_column_name:
                self.connection.huemul_logging.log_message_error(
                    message=f"{self.name}: column ip_column_name '{self.ip_column_name}' not found in dataframe"
                )
                raise Exception(
                    f"{self.name}: column ip_column_name '{self.ip_column_name}' not found in dataframe"
                )

            if (
                self.external_id_column_name
                and self.external_id_column_name in self.dataframe.columns
            ):
                self.enola_sender.external_id = row[self.external_id_column_name]
            elif self.external_id_column_name:
                self.connection.huemul_logging.log_message_error(
                    message=f"{self.name}: column external_id_column_name '{self.external_id_column_name}' not found in dataframe"
                )
                raise Exception(
                    f"{self.name}: column external_id_column_name '{self.external_id_column_name}' not found in dataframe"
                )

            step.step_type = StepType.SCORE
            step.successfull = True
            step.set_score(
                value=step.score_value,
                group=step.score_group,
                cluster=step.score_cluster,
                date=step.date_start,
            )

            # Create tracking model
            tracking_model = TrackingModel(
                isTest=self.is_test,
                enola_sender=self.enola_sender,
                enola_id_prev="",
                steps=1,
                step_list=[step],
            )

            # Add to list
            listToSend.append(tracking_model)

            # Send in batches
            if len(listToSend) == batch_size or count_rows == totalRows - 1:
                # Send to Enola
                tracking_batch = create_tracking(
                    tracking_list_model=listToSend,
                    connection=self.connection,
                    raise_error_if_fail=False,
                )

                if not tracking_batch.successfull:
                    print(f"{self.name}: finish with error, batch_id is empty")
                    return []

                resultsList.extend(tracking_batch.tracking_list)
                self.connection.huemul_logging.log_message_info(
                    message=f"{self.name} sent {len(resultsList)} of {totalRows}..."
                )

                # Clean and continue
                listToSend = []

            count_rows += 1

        self.connection.huemul_logging.log_message_info(
            message=f"{self.name} finish OK with batch_id: {self.batch_id}"
        )

        return resultsList

    def __str__(self) -> str:
        return f"Agent/Model: {self.name}"

    def __getitem__(self, key):
        return self.__dict__[key]

    def __getattr__(self, key):
        return self.__dict__[key]

    def get(self, key, default=None):
        return self.__dict__.get(key, default)
