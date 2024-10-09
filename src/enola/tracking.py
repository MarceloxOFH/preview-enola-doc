from typing import Any, Optional, List
from enola.base.common.huemul_functions import HuemulFunctions
from enola.base.internal.tracking.enola_tracking import create_tracking
from enola.base.common.auth.auth_model import AuthModel
from enola.enola_types import (
    EnolaSenderModel,
    KindType,
    DataListModel,
    DataType,
    ErrOrWarnKind,
    Info,
    Step,
    StepType,
    TokenInfo,
    TrackingModel,
)
from enola.base.connect import Connect


class Tracking:
    """
    The `Tracking` class provides methods to start and manage execution tracking in the Enola system.

    This class allows you to:

    - Initialize a tracking session.
    - Add data received from or sent to the user.
    - Register custom information, errors, warnings, and steps.
    - Execute the tracking and send the data to the Enola server.

    **Example usage:**

    ```python
    tracking = Tracking(
        token='your_jwt_token',
        name='ExecutionName',
        message_input='User input message',
        app_id='App123',
        user_id='User456',
        is_test=False
    )
    ```
    """

    def __init__(
        self,
        token: str,
        name: str,
        app_id: Optional[str] = None,
        user_id: Optional[str] = None,
        session_id: Optional[str] = None,
        channel_id: Optional[str] = None,
        ip: Optional[str] = None,
        external_id: Optional[str] = None,
        is_test: bool = False,
        message_input: str = "",
        enola_id_prev: str = "",
        app_name: str = "",
        user_name: str = "",
        session_name: str = "",
        channel_name: str = "",
        client_id: str = "",
        product_id: str = "",
    ):
        """
        Initializes a new `Tracking` instance to start tracking an execution.

        Args:
            token (str): JWT token used to identify the agent (request from Admin App).
            name (str): Name of this execution.
            app_id (str, optional): ID of the app that is calling.
            user_id (str, optional): External user ID.
            session_id (str, optional): ID of the user or application's session.
            channel_id (str, optional): Communication channel (e.g., 'web', 'chat', 'whatsapp').
            ip (str, optional): IP address of the user or application.
            external_id (str, optional): External unique record identifier.
            is_test (bool, optional): True if this call is for testing purposes.
            message_input (str, optional): Message received from the user or to explain the execution.
            enola_id_prev (str, optional): ID of the previous call to link agent sequences.
            app_name (str, optional): Name of the app.
            user_name (str, optional): Name of the user.
            session_name (str, optional): Name of the session.
            channel_name (str, optional): Name of the channel.
            client_id (str, optional): Client ID.
            product_id (str, optional): Product ID.
        """
        self.name = name
        self.enola_id_prev = enola_id_prev
        self.enola_id = ""  # Obtained after execution
        self.agent_deploy_id = ""
        self.message_input = message_input
        self.message_output = ""
        self.num_iteratons = 0
        self.hf = HuemulFunctions()
        self.url_evaluation_post = None
        self.url_evaluation_def_get = None

        # This execution information
        self.tracking_status = ""
        # Connection data

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
                url_service=self.token_info.service_account_url,
                org_id=self.token_info.org_id,
            )
        )

        # User information
        self.enola_sender = EnolaSenderModel(
            app_id=app_id,
            batch_id=None,
            app_name=app_name,
            user_id=user_id,
            user_name=user_name,
            session_id=session_id,
            session_name=session_name,
            channel_id=channel_id,
            channel_name=channel_name,
            ip=ip,
            external_id=external_id,
            client_id=client_id,
            product_id=product_id,
        )

        # If is empty or not exist assign false
        self.is_test = is_test

        # Save steps and information
        self.step_list: List[Step] = []
        self.steps = 0
        self.first_step = self.new_step(self.name, message_input=self.message_input)

    ########################################################################################
    ###############    A G E N T   M E T H O D S     #######################################
    ########################################################################################

    def add_data_received(self, name: str, data: Any, type: DataType) -> None:
        """
        Adds data received from the user.

        Args:
            name (str): The name of the data.
            data (Any): The data content.
            type (DataType): The type of data received.
        """
        self.first_step.agent_data_list.append(
            DataListModel(
                value=data, name=name, data_type=type, kind=KindType.RECEIVER
            )
        )

    def add_data_send(self, name: str, data: Any, type: DataType) -> None:
        """
        Adds data to send to the user.

        Args:
            name (str): The name of the data.
            data (Any): The data content.
            type (DataType): The type of data being sent.
        """
        self.first_step.agent_data_list.append(
            DataListModel(value=data, name=name, data_type=type, kind=KindType.SENDER)
        )

    def add_custom_info(self, key: str, value: Any) -> None:
        """
        Adds custom information to tracking.

        Args:
            key (str): The key for the custom information.
            value (Any): The value associated with the key.
        """
        self.first_step.info_list.append(Info(key, value))

    def add_file_link(
        self, name: str, url: str, type: str, size_kb: int
    ) -> None:
        """
        Adds a file link to tracking.

        Args:
            name (str): The name of the file.
            url (str): The URL of the file.
            type (str): The type of the file.
            size_kb (int): The size of the file in kilobytes.
        """
        self.first_step.add_file_link(
            name=name, url=url, type=type, size_kb=size_kb
        )

    def add_tag(self, key: str, value: Any) -> None:
        """
        Adds a tag to tracking, this tag is used to search in Enola App.

        Args:
            key (str): The tag key.
            value (Any): The tag value.
        """
        self.first_step.add_tag(key=key, value=value)

    def add_extra_info(self, key: str, value: Any) -> None:
        """
        Adds extra information to tracking, this can be used to test or debug.

        Args:
            key (str): The key for the extra information.
            value (Any): The value associated with the key.
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

    def execute(
        self,
        successfull: bool,
        message_output: str = "",
        num_iteratons: int = 0,
        score_value: float = 0,
        score_group: str = "",
        score_cluster: str = "",
        score_date: str = "",
        external_id: str = "",
    ) -> bool:
        """
        Registers tracking in the Enola server.

        Args:
            successfull (bool): True for your Agent execution OK, false for error in your Agent execution.
            message_output (str, optional): Message to user or to explain the execution results.
            num_iteratons (int, optional): Number of iterations.
            score_value (float, optional): Score value.
            score_group (str, optional): Score group.
            score_cluster (str, optional): Score cluster.
            score_date (str, optional): Date of score in ISO & UTC format (e.g., 'yyyy-MM-ddTHH:mm:ss:SSSz'). Empty for current date.
            external_id (str, optional): External unique identifier.

        Returns:
            bool: True if execution was successful, False otherwise.
        """
        self.first_step.num_iterations = num_iteratons
        if external_id != "":
            self.enola_sender.external_id = external_id

        self.close_step_others(
            step=self.first_step,
            successfull=successfull,
            others_cost=0,
            step_id="AGENT",
            message_output=message_output,
        )
        self.first_step.set_score(
            value=score_value, group=score_group, cluster=score_cluster, date=score_date
        )

        # Register in server
        print(f"{self.name}: sending to server... ")
        tracking_model = TrackingModel(
            enola_id_prev=self.enola_id_prev,
            enola_sender=self.enola_sender,
            isTest=self.is_test,
            step_list=self.step_list,
            steps=self.steps,
        )

        enola_result = create_tracking(
            tracking_model=tracking_model,
            connection=self.connection,
            raise_error_if_fail=True,
        )
        # Show results
        if enola_result.successfull:
            # Obtain Enola ID and evaluation URLs
            self.enola_id = enola_result.enola_id
            self.agent_deploy_id = enola_result.agent_deploy_id
            self.url_evaluation_post = enola_result.url_evaluation_post
            self.url_evaluation_def_get = enola_result.url_evaluation_def_get

            print(f"{self.name}: finish OK! ")

            return True
        else:
            print(f"{self.name}: finish with error: {enola_result.message}")
            self.tracking_status = enola_result.message

            return False

    ########################################################################################
    ###############    S T E P   I N F O     ###############################################
    ########################################################################################

    def new_step(self, name: str, message_input: str = "") -> Step:
        """
        Starts a new step.

        Args:
            name (str): Name of this step.
            message_input (str, optional): Message received from user or to explain the execution.

        Returns:
            Step: The newly created step object.
        """
        self.steps += 1
        return Step(name=name, message_input=message_input)

    def close_step_token(
        self,
        step: Step,
        successfull: bool,
        message_output: str = "",
        token_input_num: int = 0,
        token_output_num: int = 0,
        token_total_num: int = 0,
        token_input_cost: float = 0,
        token_output_cost: float = 0,
        token_total_cost: float = 0,
        enola_id: str = "",
        agent_deploy_id: str = "",
        step_id: str = "",
    ) -> None:
        """
        Closes a step with token information.

        Args:
            step (Step): The step to close.
            successfull (bool): True if the step was successful, False otherwise.
            message_output (str, optional): Message to user or to explain the execution results.
            token_input_num (int, optional): Number of input tokens.
            token_output_num (int, optional): Number of output tokens.
            token_total_num (int, optional): Total number of tokens.
            token_input_cost (float, optional): Cost of input tokens.
            token_output_cost (float, optional): Cost of output tokens.
            token_total_cost (float, optional): Total cost of tokens.
            enola_id (str, optional): If this step was a call to another Enola agent, this is the ID of that agent.
            agent_deploy_id (str, optional): Include this if you want to link this step to another agent of another company.
            step_id (str, optional): ID of this step, you can use it to link with external calls.
        """
        step.enola_id = enola_id
        step.agent_deploy_id = agent_deploy_id
        step.step_id = step_id
        step.message_output = message_output
        step.step_type = StepType.TOKEN
        step.token.token_input = token_input_num
        step.token.token_output = token_output_num
        step.token.token_total = token_total_num
        step.cost.token_input = token_input_cost
        step.cost.token_output = token_output_cost
        step.cost.token_total = token_total_cost

        step.date_end = self.hf.get_date_for_api()
        step.duration_in_ms = self.hf.get_dif_ms(
            step.date_start, step.date_end
        )
        step.successfull = successfull

        self.step_list.append(step)

    def close_step_video(
        self,
        step: Step,
        successfull: bool,
        message_output: str = "",
        video_num: int = 0,
        video_sec: int = 0,
        video_size: int = 0,
        video_cost: float = 0,
        enola_id_prev: str = "",
        agent_deploy_id: str = "",
        step_id: str = "",
    ) -> None:
        """
        Closes a step with video information.

        Args:
            step (Step): The step to close.
            successfull (bool): True if the step was successful, False otherwise.
            message_output (str, optional): Message to user or to explain the execution results.
            video_num (int, optional): Number of videos.
            video_sec (int, optional): Number of video seconds.
            video_size (int, optional): Video size.
            video_cost (float, optional): Video cost.
            enola_id_prev (str, optional): If this step was a call to another Enola agent, this is the ID of that agent.
            agent_deploy_id (str, optional): Include this if you want to link this step to another agent of another company.
            step_id (str, optional): ID of this step, you can use it to link with external calls.
        """
        step.enola_id_prev = enola_id_prev
        step.agent_deploy_id = agent_deploy_id
        step.step_id = step_id
        step.message_output = message_output
        step.step_type = StepType.VIDEO
        step.video.num_videos = video_num
        step.video.sec_videos = video_sec
        step.video.size_videos = video_size
        step.cost.videos = video_cost
        step.date_end = self.hf.get_date_for_api()
        step.duration_in_ms = self.hf.get_dif_ms(step.date_start, step.date_end)
        step.successfull = successfull

        self.step_list.append(step)

    def close_step_audio(
        self,
        step: Step,
        successfull: bool,
        message_output: str = "",
        audio_num: int = 0,
        audio_sec: int = 0,
        audio_size: int = 0,
        audio_cost: float = 0,
        enola_id_prev: str = "",
        agent_deploy_id: str = "",
        step_id: str = "",
    ) -> None:
        """
        Closes a step with audio information.

        Args:
            step (Step): The step to close.
            successfull (bool): True if the step was successful, False otherwise.
            message_output (str, optional): Message to user or to explain the execution results.
            audio_num (int, optional): Number of audio clips.
            audio_sec (int, optional): Number of audio seconds.
            audio_size (int, optional): Audio size.
            audio_cost (float, optional): Audio cost.
            enola_id_prev (str, optional): If this step was a call to another Enola agent, this is the ID of that agent.
            agent_deploy_id (str, optional): Include this if you want to link this step to another agent of another company.
            step_id (str, optional): ID of this step, you can use it to link with external calls.
        """
        step.enola_id_prev = enola_id_prev
        step.agent_deploy_id = agent_deploy_id
        step.step_id = step_id
        step.message_output = message_output
        step.step_type = StepType.AUDIO
        step.audio.num_audio = audio_num
        step.audio.sec_audio = audio_sec
        step.audio.size_audio = audio_size
        step.cost.audio = audio_cost
        step.date_end = self.hf.get_date_for_api()
        step.duration_in_ms = self.hf.get_dif_ms(step.date_start, step.date_end)
        step.successfull = successfull

        self.step_list.append(step)

    def close_step_image(
        self,
        step: Step,
        successfull: bool,
        message_output: str = "",
        image_num: int = 0,
        image_size: int = 0,
        image_cost: float = 0,
        enola_id_prev: str = "",
        agent_deploy_id: str = "",
        step_id: str = "",
    ) -> None:
        """
        Closes a step with image information.

        Args:
            step (Step): The step to close.
            successfull (bool): True if the step was successful, False otherwise.
            message_output (str, optional): Message to user or to explain the execution results.
            image_num (int, optional): Number of images.
            image_size (int, optional): Image size.
            image_cost (float, optional): Image cost.
            enola_id_prev (str, optional): If this step was a call to another Enola agent, this is the ID of that agent.
            agent_deploy_id (str, optional): Include this if you want to link this step to another agent of another company.
            step_id (str, optional): ID of this step, you can use it to link with external calls.
        """
        step.enola_id_prev = enola_id_prev
        step.agent_deploy_id = agent_deploy_id
        step.step_id = step_id
        step.message_output = message_output
        step.step_type = StepType.IMAGE
        step.image.num_images = image_num
        step.image.size_images = image_size
        step.cost.images = image_cost
        step.date_end = self.hf.get_date_for_api()
        step.duration_in_ms = self.hf.get_dif_ms(step.date_start, step.date_end)
        step.successfull = successfull

        self.step_list.append(step)

    def close_step_doc(
        self,
        step: Step,
        successfull: bool,
        message_output: str = "",
        doc_num: int = 0,
        doc_pages: int = 0,
        doc_size: int = 0,
        doc_char: int = 0,
        doc_cost: float = 0,
        enola_id_prev: str = "",
        agent_deploy_id: str = "",
        step_id: str = "",
    ) -> None:
        """
        Closes a step with document information.

        Args:
            step (Step): The step to close.
            successfull (bool): True if the step was successful, False otherwise.
            message_output (str, optional): Message to user or to explain the execution results.
            doc_num (int, optional): Number of documents.
            doc_pages (int, optional): Number of pages in the document.
            doc_size (int, optional): Document size.
            doc_char (int, optional): Number of characters in the document.
            doc_cost (float, optional): Document cost.
            enola_id_prev (str, optional): If this step was a call to another Enola agent, this is the ID of that agent.
            agent_deploy_id (str, optional): Include this if you want to link this step to another agent of another company.
            step_id (str, optional): ID of this step, you can use it to link with external calls.
        """
        step.enola_id_prev = enola_id_prev
        step.agent_deploy_id = agent_deploy_id
        step.step_id = step_id
        step.message_output = message_output
        step.step_type = StepType.DOCUMENT
        step.doc.num_docs = doc_num
        step.doc.num_pages = doc_pages
        step.doc.size_docs = doc_size
        step.doc.num_char = doc_char
        step.cost.docs = doc_cost
        step.date_end = self.hf.get_date_for_api()
        step.duration_in_ms = self.hf.get_dif_ms(step.date_start, step.date_end)
        step.successfull = successfull

        self.step_list.append(step)

    def close_step_others(
        self,
        step: Step,
        successfull: bool,
        message_output: str = "",
        others_cost: float = 0,
        enola_id_prev: str = "",
        agent_deploy_id: str = "",
        step_id: str = "",
    ) -> None:
        """
        Closes a step with other types of information.

        Args:
            step (Step): The step to close.
            successfull (bool): True if the step was successful, False otherwise.
            message_output (str, optional): Message to user or to explain the execution results.
            others_cost (float, optional): Cost of other types.
            enola_id_prev (str, optional): If this step was a call to another Enola agent, this is the ID of that agent.
            agent_deploy_id (str, optional): Include this if you want to link this step to another agent of another company.
            step_id (str, optional): ID of this step, you can use it to link with external calls.
        """
        step.enola_id_prev = enola_id_prev
        step.agent_deploy_id = agent_deploy_id
        step.step_id = step_id
        step.message_output = message_output
        step.step_type = StepType.OTHER
        step.cost.others = others_cost
        step.date_end = self.hf.get_date_for_api()
        step.duration_in_ms = self.hf.get_dif_ms(step.date_start, step.date_end)
        step.successfull = successfull

        self.step_list.append(step)

    def close_step_score(
        self,
        step: Step,
        successfull: bool,
        message_output: str = "",
        others_cost: float = 0,
        enola_id_prev: str = "",
        agent_deploy_id: str = "",
        step_id: str = "",
    ) -> None:
        """
        Closes a step for score information.

        Args:
            step (Step): The step to close.
            successfull (bool): True if the step was successful, False otherwise.
            message_output (str, optional): Message to user or to explain the execution results.
            others_cost (float, optional): Cost of other types.
            enola_id_prev (str, optional): If this step was a call to another Enola agent, this is the ID of that agent.
            agent_deploy_id (str, optional): Include this if you want to link this step to another agent of another company.
            step_id (str, optional): ID of this step, you can use it to link with external calls.
        """
        step.enola_id_prev = enola_id_prev
        step.agent_deploy_id = agent_deploy_id
        step.step_id = step_id
        step.message_output = message_output
        step.step_type = StepType.SCORE
        step.cost.others = others_cost
        step.successfull = successfull

        self.step_list.append(step)

    def __str__(self) -> str:
        return f"Agent/Model: {self.name}, Steps: {self.steps}"

    def __getitem__(self, key: str) -> Any:
        return self.__dict__[key]

    def __getattr__(self, key: str) -> Any:
        return self.__dict__[key]

    def get(self, key: str, default: Optional[Any] = None) -> Any:
        return self.__dict__.get(key, default)