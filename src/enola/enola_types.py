from enola.base.common.huemul_functions import HuemulFunctions
from enum import Enum
import json
import jwt
from typing import Any, Dict, Optional, List

class Environtment(Enum):
    DEV = "DEV"
    QA = "QA"
    PROD = "PROD"

class DataType(Enum):
    TEXT = "TEXT"
    NUMBER = "NUMBER"
    DATE = "DATE"
    BOOLEAN = "BOOLEAN"

class CompareType(Enum):
    EQUAL = "EQUAL"
    GREATER = "GREATER"
    LESS = "LESS"
    GREATER_EQUAL = "GREATER_EQUAL"
    LESS_EQUAL = "LESS_EQUAL"
    NOT_EQUAL = "NOT_EQUAL"
    CONTAINS = "CONTAINS"

class TokenInfo:
    def __init__(self, token: str):

        if token == "":
                raise Exception("token is empty.")
        
        try:
            decoded = jwt.decode(token, algorithms=['none'], options={'verify_signature': False})
            self.agent_deploy_id = decoded.get("agentDeployId", None)
            self.org_id = decoded.get("orgId", None)
            self.service_account_id = decoded.get("id", None)
            self.service_account_name = decoded.get("displayName", None)
            self.service_account_url = decoded.get("url", None)
            self.service_account_url_backend = decoded.get("urlBackend", None)
            self.service_account_can_tracking = decoded.get("canTracking", False)
            self.service_account_can_evaluate = decoded.get("canEvaluate", False)
            self.is_service_account = decoded.get("isServiceAccount", False)
            self.service_account_can_get_executions = decoded.get("canGetExecutions", False)

            #verify if serviceAccountUrl is empty, return error
            if not self.service_account_url:
                raise Exception("serviceAccountUrl is empty.")
            if not self.service_account_url_backend:
                raise Exception("serviceAccountUrlBackend is empty.")
            if not self.org_id:
                raise Exception("orgId is empty.")
            
        except jwt.ExpiredSignatureError:
            print("token expired.")
        except jwt.DecodeError:
            print("Error decoding token.")
        except jwt.InvalidTokenError:
            print("Invalid Token.")


    def __getitem__(self, key):
        return self.__dict__[key]

    def __getattr__(self, key):
        return self.__dict__[key]

    def get(self, key, default=None):
        return self.__dict__.get(key, default)

class KindType(Enum):
    RECEIVER = "RECEIVER"
    SENDER = "SENDER"

class ErrorType(Enum):
    ERROR = "ERROR"
    WARNING = "WARNING"

class ErrOrWarnKind(Enum):
    """
    EXTERNAL: external agent call generate an unexpected error or warning
    """
    EXTERNAL = "EXTERNAL"
    """
    INTERNAL_CONTROLLED: internal agent call generate an unexpected error or warning
    """
    INTERNAL_CONTROLLED = "INTERNAL_CONTROLLED"
    """
    INTERNAL_TOUSER: controlled error or warning to send to user
    """
    INTERNAL_TOUSER = "INTERNAL_TOUSER"

class ErrorOrWarnModel:
    def __init__(self, id: str, message: str, error_type: ErrorType, kind: ErrOrWarnKind):
        self.id = id
        self.error = message
        self.error_type: ErrorType = error_type
        self.kind: ErrOrWarnKind = kind

    def to_json(self):
        return {
            "id": self.id,
            "error": self.error,
            "error_type": self.error_type.value,
            "kind": self.kind.value
        }
    
    def __getitem__(self, key):
        return self.__dict__[key]

    def __getattr__(self, key):
        return self.__dict__[key]

    def get(self, key, default=None):
        return self.__dict__.get(key, default)
    
class DataListModel:
    """
    Represents a data item in the agent's data list.

    Attributes:
        kind (KindType): Indicates whether the data is received or sent.
        name (str): The name of the data item.
        data_type (DataType): The type of the data item.
        value (Any): The value of the data item.
    """

    def __init__(self, kind: 'KindType', name: str, data_type: 'DataType', value: Any):
        """
        Initializes a new instance of DataListModel.

        Args:
            kind (KindType): Indicates whether the data is received or sent.
            name (str): The name of the data item.
            data_type (DataType): The type of the data item.
            value (Any): The value of the data item.
        """
        self.kind = kind
        self.name = name
        self.data_type = data_type
        self.value = value

    def to_json(self) -> Dict[str, Any]:
        """
        Converts the DataListModel instance to a JSON-serializable dictionary.

        Returns:
            Dict[str, Any]: A dictionary representation of the DataListModel.
        """
        return {
            "kind": self.kind.value,
            "name": self.name,
            "data_type": self.data_type.value,
            "value": self.value
        }

    def __getitem__(self, key: str) -> Any:
        return self.__dict__[key]

    def __getattr__(self, key: str) -> Any:
        return self.__dict__[key]

    def get(self, key: str, default: Optional[Any] = None) -> Any:
        return self.__dict__.get(key, default)


class Info:
    """
    Represents an information item, which can be a tag or extra information.

    Attributes:
        type (str): The type of information ('tag' or 'info').
        key (str): The key of the information item.
        value (Any): The value of the information item.
    """

    def __init__(self, type: str, key: str, value: Any):
        """
        Initializes a new instance of Info.

        Args:
            type (str): The type of information ('tag' or 'info').
            key (str): The key of the information item.
            value (Any): The value of the information item.
        """
        self.type = type
        self.key = key
        if self.is_numeric(value):
            self.value = value
        elif self.is_string(value):
            if self.is_dict(value):
                self.value = json.dumps(value)
            else:
                self.value = value
        else:
            self.value = value

    def is_numeric(self, value: Any) -> bool:
        """
        Checks if the value is numeric.

        Args:
            value (Any): The value to check.

        Returns:
            bool: True if the value is numeric, False otherwise.
        """
        return isinstance(value, (int, float, complex))

    def is_string(self, value: Any) -> bool:
        """
        Checks if the value is a string.

        Args:
            value (Any): The value to check.

        Returns:
            bool: True if the value is a string, False otherwise.
        """
        return isinstance(value, str)

    def is_dict(self, value: Any) -> bool:
        """
        Checks if the value is a dictionary.

        Args:
            value (Any): The value to check.

        Returns:
            bool: True if the value is a dictionary, False otherwise.
        """
        return isinstance(value, dict)

    def to_json(self) -> Dict[str, Any]:
        """
        Converts the Info instance to a JSON-serializable dictionary.

        Returns:
            Dict[str, Any]: A dictionary representation of the Info.
        """
        return {
            "type": self.type,
            "key": self.key,
            "value": self.value
        }

    def __getitem__(self, key: str) -> Any:
        return self.__dict__[key]

    def __getattr__(self, key: str) -> Any:
        return self.__dict__[key]

    def get(self, key: str, default: Optional[Any] = None) -> Any:
        return self.__dict__.get(key, default)


class ApiDataModel:
    """
    Represents API data related to a step.

    Attributes:
        name (str): The name of the API call.
        method (str): The HTTP method used (e.g., GET, POST).
        url (str): The URL of the API endpoint.
        body (str): The request body sent.
        header (str): The request headers sent.
        payload (str): The response payload received.
        description (str): A description of the API call.
    """

    def __init__(self, name: str, method: str, url: str, body: str, header: str, payload: str, description: str):
        """
        Initializes a new instance of ApiDataModel.

        Args:
            name (str): The name of the API call.
            method (str): The HTTP method used (e.g., GET, POST).
            url (str): The URL of the API endpoint.
            body (str): The request body sent.
            header (str): The request headers sent.
            payload (str): The response payload received.
            description (str): A description of the API call.
        """
        self.name = name
        self.method = method
        self.url = url
        self.description = description
        self.body = body
        self.header = header
        self.payload = payload

    def to_json(self) -> Dict[str, Any]:
        """
        Converts the ApiDataModel instance to a JSON-serializable dictionary.

        Returns:
            Dict[str, Any]: A dictionary representation of the ApiDataModel.
        """
        return {
            "name": self.name,
            "method": self.method,
            "url": self.url,
            "description": self.description,
            "body": self.body,
            "header": self.header,
            "payload": self.payload
        }

    def __getitem__(self, key: str) -> Any:
        return self.__dict__[key]

    def __getattr__(self, key: str) -> Any:
        return self.__dict__[key]

    def get(self, key: str, default: Optional[Any] = None) -> Any:
        return self.__dict__.get(key, default)


class FileInfoModel:
    """
    Represents information about a file related to a step.

    Attributes:
        name (str): The name of the file.
        url (str): The URL where the file is located.
        type (str): The type of the file (e.g., 'image/png').
        size (int): The size of the file in kilobytes.
        description (str): A description of the file.
    """

    def __init__(self, name: str, url: str, type: str, sizeKb: int, description: str):
        """
        Initializes a new instance of FileInfoModel.

        Args:
            name (str): The name of the file.
            url (str): The URL where the file is located.
            type (str): The type of the file (e.g., 'image/png').
            sizeKb (int): The size of the file in kilobytes.
            description (str): A description of the file.
        """
        self.name = name
        self.url = url
        self.type = type
        self.size = sizeKb
        self.description = description

    def to_json(self) -> Dict[str, Any]:
        """
        Converts the FileInfoModel instance to a JSON-serializable dictionary.

        Returns:
            Dict[str, Any]: A dictionary representation of the FileInfoModel.
        """
        return {
            "name": self.name,
            "url": self.url,
            "type": self.type,
            "size": self.size,
            "description": self.description
        }

    def __getitem__(self, key: str) -> Any:
        return self.__dict__[key]

    def __getattr__(self, key: str) -> Any:
        return self.__dict__[key]

    def get(self, key: str, default: Optional[Any] = None) -> Any:
        return self.__dict__.get(key, default)


class EnolaSenderModel:
    """
    Represents the sender information for Enola tracking.

    Attributes:
        app_id (str): ID of the application.
        app_name (str): Name of the application.
        user_id (str): ID of the user.
        user_name (str): Name of the user.
        session_id (str): ID of the session.
        session_name (str): Name of the session.
        channel_id (str): ID of the channel.
        channel_name (str): Name of the channel.
        client_id (str): ID of the client.
        product_id (str): ID of the product.
        external_id (str): External ID for tracking.
        batch_id (str): ID of the batch if batch tracking is used.
        ip (str): IP address of the sender.
    """

    def __init__(
        self,
        app_id: str,
        app_name: str,
        user_id: str,
        user_name: str,
        session_id: str,
        session_name: str,
        channel_id: str,
        channel_name: str,
        client_id: str,
        product_id: str,
        external_id: str,
        batch_id: str,
        ip: str,
    ):
        """
        Initializes a new instance of EnolaSenderModel.

        Args:
            app_id (str): ID of the application.
            app_name (str): Name of the application.
            user_id (str): ID of the user.
            user_name (str): Name of the user.
            session_id (str): ID of the session.
            session_name (str): Name of the session.
            channel_id (str): ID of the channel.
            channel_name (str): Name of the channel.
            client_id (str): ID of the client.
            product_id (str): ID of the product.
            external_id (str): External ID for tracking.
            batch_id (str): ID of the batch if batch tracking is used.
            ip (str): IP address of the sender.
        """
        self.app_id = app_id
        self.app_name = app_name
        self.user_id = user_id
        self.user_name = user_name
        self.session_id = session_id
        self.session_name = session_name
        self.channel_id = channel_id
        self.channel_name = channel_name
        self.client_id = client_id
        self.product_id = product_id
        self.external_id = external_id
        self.batch_id = batch_id
        self.ip = ip

    def __getitem__(self, key: str) -> Any:
        return self.__dict__[key]

    def __getattr__(self, key: str) -> Any:
        return self.__dict__[key]

    def get(self, key: str, default: Optional[Any] = None) -> Any:
        return self.__dict__.get(key, default)


class EvalType(Enum):
    """
    Enumeration of evaluation types.

    Attributes:
        AUTO (str): Automatic evaluation.
        USER (str): User evaluation.
        INTERNAL (str): Internal evaluation.
    """
    AUTO = "AUTO"
    USER = "USER"
    INTERNAL = "INTERNAL"


# ***********************************************************************************
# *************   S T E P S    T Y P E S     ***********************************
# ***********************************************************************************

class StepCost:
    """
    Represents the cost information for a step.

    Attributes:
        token_input (float): Cost of input tokens.
        token_output (float): Cost of output tokens.
        token_total (float): Total cost of tokens.
        videos (float): Cost associated with videos.
        audio (float): Cost associated with audio.
        images (float): Cost associated with images.
        docs (float): Cost associated with documents.
        infra (float): Infrastructure cost.
        others (float): Other costs.
        total (float): Total cost.
    """

    def __init__(self):
        """
        Initializes a new instance of StepCost.
        """
        self.token_input = 0.0
        self.token_output = 0.0
        self.token_total = 0.0
        self.videos = 0.0
        self.audio = 0.0
        self.images = 0.0
        self.docs = 0.0
        self.infra = 0.0
        self.others = 0.0
        self.total = 0.0

    def __getitem__(self, key: str) -> Any:
        return self.__dict__[key]

    def __getattr__(self, key: str) -> Any:
        return self.__dict__[key]

    def get(self, key: str, default: Optional[Any] = None) -> Any:
        return self.__dict__.get(key, default)


class StepVideo:
    """
    Represents video-related information for a step.

    Attributes:
        num_videos (int): Number of videos processed.
        size_videos (int): Total size of videos in kilobytes.
        sec_videos (int): Total duration of videos in seconds.
    """

    def __init__(self):
        """
        Initializes a new instance of StepVideo.
        """
        self.num_videos = 0
        self.size_videos = 0
        self.sec_videos = 0

    def __getitem__(self, key: str) -> Any:
        return self.__dict__[key]

    def __getattr__(self, key: str) -> Any:
        return self.__dict__[key]

    def get(self, key: str, default: Optional[Any] = None) -> Any:
        return self.__dict__.get(key, default)


class StepAudio:
    """
    Represents audio-related information for a step.

    Attributes:
        num_audio (int): Number of audio files processed.
        size_audio (int): Total size of audio files in kilobytes.
        sec_audio (int): Total duration of audio files in seconds.
    """

    def __init__(self):
        """
        Initializes a new instance of StepAudio.
        """
        self.num_audio = 0
        self.size_audio = 0
        self.sec_audio = 0

    def __getitem__(self, key: str) -> Any:
        return self.__dict__[key]

    def __getattr__(self, key: str) -> Any:
        return self.__dict__[key]

    def get(self, key: str, default: Optional[Any] = None) -> Any:
        return self.__dict__.get(key, default)


class StepImage:
    """
    Represents image-related information for a step.

    Attributes:
        num_images (int): Number of images processed.
        size_images (int): Total size of images in kilobytes.
    """

    def __init__(self):
        """
        Initializes a new instance of StepImage.
        """
        self.num_images = 0
        self.size_images = 0

    def __getitem__(self, key: str) -> Any:
        return self.__dict__[key]

    def __getattr__(self, key: str) -> Any:
        return self.__dict__[key]

    def get(self, key: str, default: Optional[Any] = None) -> Any:
        return self.__dict__.get(key, default)


class StepDoc:
    """
    Represents document-related information for a step.

    Attributes:
        num_docs (int): Number of documents processed.
        num_pages (int): Total number of pages in documents.
        size_docs (int): Total size of documents in kilobytes.
        num_char (int): Total number of characters in documents.
    """

    def __init__(self):
        """
        Initializes a new instance of StepDoc.
        """
        self.num_docs = 0
        self.num_pages = 0
        self.size_docs = 0
        self.num_char = 0

    def __getitem__(self, key: str) -> Any:
        return self.__dict__[key]

    def __getattr__(self, key: str) -> Any:
        return self.__dict__[key]

    def get(self, key: str, default: Optional[Any] = None) -> Any:
        return self.__dict__.get(key, default)


class StepToken:
    """
    Represents token-related information for a step.

    Attributes:
        num_char (int): Number of characters processed.
        token_input (int): Number of input tokens.
        token_output (int): Number of output tokens.
        token_total (int): Total number of tokens.
    """

    def __init__(self):
        """
        Initializes a new instance of StepToken.
        """
        self.num_char = 0
        self.token_input = 0
        self.token_output = 0
        self.token_total = 0

    def __getitem__(self, key: str) -> Any:
        return self.__dict__[key]

    def __getattr__(self, key: str) -> Any:
        return self.__dict__[key]

    def get(self, key: str, default: Optional[Any] = None) -> Any:
        return self.__dict__.get(key, default)


class StepType(Enum):
    """
    Enumeration of step types.

    Attributes:
        TOKEN (str): Token-related step.
        VIDEO (str): Video-related step.
        AUDIO (str): Audio-related step.
        IMAGE (str): Image-related step.
        DOCUMENT (str): Document-related step.
        OTHER (str): Other types of step.
        SCORE (str): Score-related step.
    """
    TOKEN = "TOKEN"
    VIDEO = "VIDEO"
    AUDIO = "AUDIO"
    IMAGE = "IMAGE"
    DOCUMENT = "DOCUMENT"
    OTHER = "OTHER"
    SCORE = "SCORE"


class Step:
    """
    Represents a step in the agent execution.

    Attributes:
        name (str): Name of the step.
        enola_id (str): Enola ID of the step.
        agent_deploy_id (str): Agent deployment ID.
        step_id (str): Unique identifier for the step.
        message_input (str): Input message for the step.
        message_output (str): Output message from the step.
        num_iterations (int): Number of iterations.
        step_id_prev (str): Previous step ID.
        date_start (str): Start date and time of the step.
        date_end (str): End date and time of the step.
        agent_data_list (List[DataListModel]): List of agent data items.
        errOrWarn_list (List[ErrorOrWarnModel]): List of errors or warnings.
        extra_info_list (List[Info]): List of extra information items.
        file_info_list (List[FileInfoModel]): List of file information items.
        step_api_data_list (List[ApiDataModel]): List of API data items.
        step_type (StepType): Type of the step.
        successfull (bool): Indicates if the step was successful.
        num_errors (int): Number of errors.
        num_warnings (int): Number of warnings.
        score_value (float): Score value.
        score_group (str): Score group.
        score_cluster (str): Score cluster.
        video (StepVideo): Video-related information.
        audio (StepAudio): Audio-related information.
        image (StepImage): Image-related information.
        doc (StepDoc): Document-related information.
        token (StepToken): Token-related information.
        cost (StepCost): Cost-related information.
        income_total (float): Total income.
        duration_in_ms (int): Duration of the step in milliseconds.
    """

    def __init__(self, name: str, message_input: str = ""):
        """
        Initializes a new instance of Step.

        Args:
            name (str): Name of the step.
            message_input (str, optional): Input message for the step.
        """
        self.hf = HuemulFunctions()
        self.name = name
        self.enola_id = ""
        self.agent_deploy_id = ""
        self.step_id = ""
        self.message_input = message_input
        self.message_output = ""
        self.num_iterations = 0
        self.step_id_prev = ""
        self.date_start = self.hf.get_date_for_api()
        self.date_end = self.date_start
        self.agent_data_list: List[DataListModel] = []  # only for first step
        self.errOrWarn_list: List['ErrorOrWarnModel'] = []
        self.extra_info_list: List[Info] = []
        self.file_info_list: List[FileInfoModel] = []
        self.step_api_data_list: List[ApiDataModel] = []
        self.step_type: StepType = StepType.OTHER

        self.successfull = False
        self.num_errors = 0
        self.num_warnings = 0

        self.score_value = 0.0
        self.score_group = ""
        self.score_cluster = ""

        self.video = StepVideo()
        self.audio = StepAudio()
        self.image = StepImage()
        self.doc = StepDoc()
        self.token = StepToken()
        self.cost = StepCost()
        self.income_total = 0.0
        self.duration_in_ms = 0

    def set_score(self, value: float, group: str, cluster: str, date: str = "") -> None:
        """
        Sets the score for the step.

        Args:
            value (float): Score value.
            group (str): Score group.
            cluster (str): Score cluster.
            date (str, optional): Date of the score in ISO & UTC format (e.g., 'yyyy-MM-ddTHH:mm:ss:SSSz'). Empty for current date.
        """
        self.score_value = value
        self.score_group = group
        self.score_cluster = cluster
        if date != "":
            self.date_start = date
            self.date_end = date

    def add_api_data(
        self,
        bodyToSend: str,
        payloadReceived: str,
        name: str,
        method: str,
        url: str,
        description: str = "",
        headerToSend: str = "",
    ) -> None:
        """
        Adds API data related to the step.

        Args:
            bodyToSend (str): The request body sent.
            payloadReceived (str): The response payload received.
            name (str): The name of the API call.
            method (str): The HTTP method used.
            url (str): The URL of the API endpoint.
            description (str, optional): A description of the API call.
            headerToSend (str, optional): The request headers sent.
        """
        self.step_api_data_list.append(
            ApiDataModel(
                name=name,
                method=method,
                url=url,
                body=bodyToSend,
                header=headerToSend,
                payload=payloadReceived,
                description=description,
            )
        )

    def add_file_link(
        self,
        name: str,
        url: str,
        type: str,
        size_kb: int,
        description: str = "",
    ) -> None:
        """
        Adds file information related to the step.

        Args:
            name (str): The name of the file.
            url (str): The URL where the file is located.
            type (str): The type of the file.
            size_kb (int): The size of the file in kilobytes.
            description (str, optional): A description of the file.
        """
        self.file_info_list.append(
            FileInfoModel(
                name=name,
                url=url,
                type=type,
                sizeKb=size_kb,
                description=description,
            )
        )

    def add_tag(self, key: str, value: Any) -> None:
        """
        Adds a tag to the step.

        Args:
            key (str): The key of the tag.
            value (Any): The value of the tag.
        """
        self.extra_info_list.append(Info(type="tag", key=key, value=value))

    def add_extra_info(self, key: str, value: Any) -> None:
        """
        Adds extra information to the step.

        Args:
            key (str): The key of the extra information.
            value (Any): The value of the extra information.
        """
        self.extra_info_list.append(Info(type="info", key=key, value=value))

    def add_error(self, id: str, message: str, kind: 'ErrOrWarnKind') -> None:
        """
        Adds an error to the step.

        Args:
            id (str): The error identifier.
            message (str): The error message.
            kind (ErrOrWarnKind): The kind of error.
        """
        self.num_errors += 1
        self.errOrWarn_list.append(
            ErrorOrWarnModel(
                id=id,
                message=message,
                error_type=ErrorType.ERROR,
                kind=kind,
            )
        )

    def add_warning(self, id: str, message: str, kind: 'ErrOrWarnKind') -> None:
        """
        Adds a warning to the step.

        Args:
            id (str): The warning identifier.
            message (str): The warning message.
            kind (ErrOrWarnKind): The kind of warning.
        """
        self.num_warnings += 1
        self.errOrWarn_list.append(
            ErrorOrWarnModel(
                id=id,
                message=message,
                error_type=ErrorType.WARNING,
                kind=kind,
            )
        )

    def to_json(self) -> Dict[str, Any]:
        """
        Converts the Step instance to a JSON-serializable dictionary.

        Returns:
            Dict[str, Any]: A dictionary representation of the Step.
        """
        return {
            "stepId": self.step_id,
            "stepIdPrev": self.step_id_prev,
            "stepDateStart": self.date_start,
            "stepDateEnd": self.date_end,
            "agentDeployId": self.agent_deploy_id,
            "agentExecName": self.name,
            "agentExecDurationMs": self.duration_in_ms,
            "agentExecSuccessfull": self.successfull,
            "agentExecNumErrors": self.num_errors,
            "agentExecNumWarnings": self.num_warnings,
            "agentExecNumVideos": self.video.num_videos,
            "agentExecSecVideos": self.video.sec_videos,
            "agentExecSizeVideos": self.video.size_videos,
            "agentExecNumAudio": self.audio.num_audio,
            "agentExecSecAudio": self.audio.sec_audio,
            "agentExecSizeAudio": self.audio.size_audio,
            "agentExecNumImages": self.image.num_images,
            "agentExecSizeImages": self.image.size_images,
            "agentExecNumDocs": self.doc.num_docs,
            "agentExecNumPages": self.doc.num_pages,
            "agentExecSizeDocs": self.doc.size_docs,
            "agentExecNumChar": self.doc.num_char + self.token.num_char,
            "agentExecTokenInput": self.token.token_input,
            "agentExecTokenOutput": self.token.token_output,
            "agentExecTokenTotal": self.token.token_total,
            "agentExecCostTokenInput": self.cost.token_input,
            "agentExecCostTokenOutput": self.cost.token_output,
            "agentExecCostTokenTotal": self.cost.token_total,
            "agentExecCostVideos": self.cost.videos,
            "agentExecCostAudio": self.cost.audio,
            "agentExecCostImages": self.cost.images,
            "agentExecCostDocs": self.cost.docs,
            "agentExecCostInfra": self.cost.infra,
            "agentExecCostOthers": self.cost.others,
            "agentExecCostTotal": self.cost.total,
            "agentExecIncomeTotal": self.income_total,
            "agentExecScoreValue": self.score_value,
            "agentExecScoreGroup": self.score_group,
            "agentExecScoreCluster": self.score_cluster,
            "agentExecType": self.step_type.value,
            "agentExecMessageInput": self.message_input,
            "agentExecMessageOutput": self.message_output,
            "agentExecCliNumIter": self.num_iterations,
            "agentData": [item.to_json() for item in self.agent_data_list],
            "errorOrWarning": [item.to_json() for item in self.errOrWarn_list],
            "extraInfo": [item.to_json() for item in self.extra_info_list],
            "fileInfo": [item.to_json() for item in self.file_info_list],
            "stepApiData": [item.to_json() for item in self.step_api_data_list],
        }

    def __str__(self) -> str:
        duration_seconds = self.duration_in_ms / 1000
        return f'Step: {self.name}, Duration: {duration_seconds} seconds'

    def __getitem__(self, key: str) -> Any:
        return self.__dict__[key]

    def __getattr__(self, key: str) -> Any:
        return self.__dict__[key]

    def get(self, key: str, default: Optional[Any] = None) -> Any:
        return self.__dict__.get(key, default)


# ***********************************************************************************
# *************   T R A C K I N G   T Y P E S     ***********************************
# ***********************************************************************************

class TrackingModel:
    """
    Represents a tracking model for agent execution.

    Attributes:
        enola_sender (EnolaSenderModel): The sender information.
        is_test (bool): Indicates if the execution is a test.
        step_list (List[Step]): List of steps in the execution.
        steps (int): Total number of steps.
        enola_id_prev (str): Previous Enola ID.
    """

    def __init__(
        self,
        is_test: bool,
        step_list: List['Step'],
        steps: int,
        enola_id_prev: str,
        enola_sender: 'EnolaSenderModel',
    ):
        """
        Initializes a new instance of TrackingModel.

        Args:
            is_test (bool): Indicates if the execution is a test.
            step_list (List[Step]): List of steps in the execution.
            steps (int): Total number of steps.
            enola_id_prev (str): Previous Enola ID.
            enola_sender (EnolaSenderModel): The sender information.
        """
        self.enola_sender = enola_sender
        self.is_test = is_test
        self.step_list = step_list
        self.steps = steps
        self.enola_id_prev = enola_id_prev

    def to_json(self) -> Dict[str, Any]:
        """
        Converts the TrackingModel instance to a JSON-serializable dictionary.

        Returns:
            Dict[str, Any]: A dictionary representation of the TrackingModel.
        """
        return {
            "app_id": self.enola_sender.app_id,
            "app_name": self.enola_sender.app_name,
            "user_id": self.enola_sender.user_id,
            "user_name": self.enola_sender.user_name,
            "session_id": self.enola_sender.session_id,
            "channel_id": self.enola_sender.channel_id,
            "session_name": self.enola_sender.session_name,
            "client_id": self.enola_sender.client_id,
            "product_id": self.enola_sender.product_id,
            "agentExecBatchId": self.enola_sender.batch_id,
            "ip": self.enola_sender.ip,
            "code_api": self.enola_sender.external_id,
            "isTest": self.is_test,
            "step_list": [step.to_json() for step in self.step_list],
            "steps": self.steps,
            "enola_id_prev": self.enola_id_prev,
        }

    def __getitem__(self, key: str) -> Any:
        return self.__dict__[key]

    def __getattr__(self, key: str) -> Any:
        return self.__dict__[key]

    def get(self, key: str, default: Any = None) -> Any:
        return self.__dict__.get(key, default)


class TrackingResponseModel:
    """
    Represents the response model for tracking.

    Attributes:
        enola_id (str): Enola ID of the execution.
        agent_deploy_id (str): Agent deployment ID.
        url_evaluation_def_get (str): URL to get evaluation definitions.
        url_evaluation_post (str): URL to post evaluations.
        successfull (bool): Indicates if the tracking was successful.
        message (str): Response message.
        args (Dict[str, Any]): Additional arguments.
    """

    def __init__(
        self,
        successfull: Optional[bool] = None,
        enola_id: str = "",
        agent_deploy_id: str = "",
        message: str = "",
        url_evaluation_def_get: str = "",
        url_evaluation_post: str = "",
        **args,
    ):
        """
        Initializes a new instance of TrackingResponseModel.

        Args:
            successfull (bool, optional): Indicates if the tracking was successful.
            enola_id (str, optional): Enola ID of the execution.
            agent_deploy_id (str, optional): Agent deployment ID.
            message (str, optional): Response message.
            url_evaluation_def_get (str, optional): URL to get evaluation definitions.
            url_evaluation_post (str, optional): URL to post evaluations.
            **args: Additional keyword arguments.
        """
        self.enola_id = enola_id or args.get("agentExecuteId", "")
        self.agent_deploy_id = agent_deploy_id or args.get("agentDeployId", "")
        self.url_evaluation_def_get = url_evaluation_def_get or args.get("urlEvaluationDefGet", "")
        self.url_evaluation_post = url_evaluation_post or args.get("urlEvaluationPost", "")
        self.successfull = successfull if successfull is not None else args.get("isSuccessful", False)
        self.message = message or args.get("message", "")
        self.args = args

    def to_json(self) -> Dict[str, Any]:
        """
        Converts the TrackingResponseModel instance to a JSON-serializable dictionary.

        Returns:
            Dict[str, Any]: A dictionary representation of the TrackingResponseModel.
        """
        return {
            "enolaId": self.enola_id,
            "agentDeployId": self.agent_deploy_id,
            "successfull": self.successfull,
            "message": self.message,
            "args": self.args,
        }

    def __getitem__(self, key: str) -> Any:
        return self.__dict__[key]

    def __getattr__(self, key: str) -> Any:
        return self.__dict__[key]

    def get(self, key: str, default: Any = None) -> Any:
        return self.__dict__.get(key, default)


# ***********************************************************************************
# *************   T R A C K I N G   B A T C H   T Y P E S     ***********************
# ***********************************************************************************

class TrackingBatchHeadModel:
    """
    Represents the header model for batch tracking.

    Attributes:
        enola_sender (EnolaSenderModel): The sender information.
        name (str): Name of the batch execution.
        period (str): Period of the batch execution.
        total_rows (int): Total number of rows in the batch.
        is_test (bool): Indicates if the batch execution is a test.
    """

    def __init__(
        self,
        name: str,
        period: str,
        total_rows: int,
        is_test: bool,
        enola_sender: 'EnolaSenderModel',
    ):
        """
        Initializes a new instance of TrackingBatchHeadModel.

        Args:
            name (str): Name of the batch execution.
            period (str): Period of the batch execution.
            total_rows (int): Total number of rows in the batch.
            is_test (bool): Indicates if the batch execution is a test.
            enola_sender (EnolaSenderModel): The sender information.
        """
        self.enola_sender = enola_sender
        self.name = name
        self.period = period
        self.total_rows = total_rows
        self.is_test = is_test

    def to_json(self) -> Dict[str, Any]:
        """
        Converts the TrackingBatchHeadModel instance to a JSON-serializable dictionary.

        Returns:
            Dict[str, Any]: A dictionary representation of the TrackingBatchHeadModel.
        """
        return {
            "agentExecBatchCliAppId": self.enola_sender.app_id,
            "agentExecBatchCliAppName": self.enola_sender.app_name,
            "agentExecBatchCliUserId": self.enola_sender.user_id,
            "agentExecBatchCliUserName": self.enola_sender.user_name,
            "agentExecBatchCliSessionId": self.enola_sender.session_id,
            "agentExecBatchCliChannel": self.enola_sender.channel_id,
            "agentExecBatchCliChannelName": self.enola_sender.channel_name,
            "agentExecBatchCliSessionName": self.enola_sender.session_name,
            "agentExecBatchCliIP": self.enola_sender.ip,
            "agentExecBatchName": self.name,
            "agentExecBatchPeriodData": self.period,
            "agentExecBatchIsTest": self.is_test,
            "agentExecBatchNumRowsTotal": self.total_rows,
        }

    def __getitem__(self, key: str) -> Any:
        return self.__dict__[key]

    def __getattr__(self, key: str) -> Any:
        return self.__dict__[key]

    def get(self, key: str, default: Any = None) -> Any:
        return self.__dict__.get(key, default)


class TrackingBatchHeadResponseModel:
    """
    Represents the response model for batch tracking head.

    Attributes:
        batch_id (str): ID of the batch.
        agent_deploy_id (str): Agent deployment ID.
        successfull (bool): Indicates if the batch creation was successful.
        message (str): Response message.
        args (Dict[str, Any]): Additional arguments.
    """

    def __init__(
        self,
        batch_id: str = "",
        agent_deploy_id: str = "",
        successfull: Optional[bool] = None,
        message: str = "",
        **args,
    ):
        """
        Initializes a new instance of TrackingBatchHeadResponseModel.

        Args:
            batch_id (str, optional): ID of the batch.
            agent_deploy_id (str, optional): Agent deployment ID.
            successfull (bool, optional): Indicates if the batch creation was successful.
            message (str, optional): Response message.
            **args: Additional keyword arguments.
        """
        self.batch_id = batch_id or args.get("agentExecBatchId", "")
        self.agent_deploy_id = agent_deploy_id or args.get("agentDeployId", "")
        self.successfull = successfull if successfull is not None else args.get("agentExecBatchSuccessfull", False)
        self.message = message or args.get("message", "")
        self.args = args

    def to_json(self) -> Dict[str, Any]:
        """
        Converts the TrackingBatchHeadResponseModel instance to a JSON-serializable dictionary.

        Returns:
            Dict[str, Any]: A dictionary representation of the TrackingBatchHeadResponseModel.
        """
        return {
            "batch_id": self.batch_id,
            "agentDeployId": self.agent_deploy_id,
            "successfull": self.successfull,
            "message": self.message,
            "args": self.args,
        }

    def __getitem__(self, key: str) -> Any:
        return self.__dict__[key]

    def __getattr__(self, key: str) -> Any:
        return self.__dict__[key]

    def get(self, key: str, default: Any = None) -> Any:
        return self.__dict__.get(key, default)


class TrackingBatchDetailResponseModel:
    """
    Represents the detailed response model for batch tracking.

    Attributes:
        tracking_list (List[TrackingResponseModel]): List of tracking responses.
        agent_deploy_id (str): Agent deployment ID.
        successfull (bool): Indicates if the batch tracking was successful.
        message (str): Response message.
        args (Dict[str, Any]): Additional arguments.
    """

    def __init__(
        self,
        agent_deploy_id: str = "",
        successfull: Optional[bool] = None,
        message: str = "",
        tracking_list: Optional[List[TrackingResponseModel]] = None,
        **args,
    ):
        """
        Initializes a new instance of TrackingBatchDetailResponseModel.

        Args:
            agent_deploy_id (str, optional): Agent deployment ID.
            successfull (bool, optional): Indicates if the batch tracking was successful.
            message (str, optional): Response message.
            tracking_list (List[TrackingResponseModel], optional): List of tracking responses.
            **args: Additional keyword arguments.
        """
        tracking_list_data = tracking_list or args.get("trackingList", [])
        self.tracking_list: List[TrackingResponseModel] = [
            TrackingResponseModel(**item) if isinstance(item, dict) else item for item in tracking_list_data
        ]
        self.agent_deploy_id = agent_deploy_id or args.get("agentDeployId", "")
        self.successfull = successfull if successfull is not None else args.get("isSuccessful", False)
        self.message = message or args.get("message", "")
        self.args = args

    def __getitem__(self, key: str) -> Any:
        return self.__dict__[key]

    def __getattr__(self, key: str) -> Any:
        return self.__dict__[key]

    def get(self, key: str, default: Any = None) -> Any:
        return self.__dict__.get(key, default)


# ***********************************************************************************
# *************   E X E C U T I O N   T Y P E S     ***********************************
# ***********************************************************************************

class ExecutionModel:
    """
    Represents an execution model containing data and status.

    Attributes:
        data (List[Any]): The execution data.
        successfull (bool): Indicates if the execution was successful.
        message (str): Response message.
        args (Dict[str, Any]): Additional arguments.
    """

    def __init__(self, data: List[Any], successfull: bool, message: str, **args):
        """
        Initializes a new instance of ExecutionModel.

        Args:
            data (List[Any]): The execution data.
            successfull (bool): Indicates if the execution was successful.
            message (str): Response message.
            **args: Additional keyword arguments.
        """
        self.data = data
        self.successfull = successfull
        self.message = message
        self.args = args

    def __getitem__(self, key: str) -> Any:
        return self.__dict__[key]
    
    def __getattr__(self, key: str) -> Any:
        return self.__dict__[key]
    
    def get(self, key: str, default: Any = None) -> Any:
        return self.__dict__.get(key, default)


class ExecutionEvalFilter:
    """
    Represents a filter for execution evaluations.

    Attributes:
        eval_id (List[str]): List of evaluation IDs.
        include (bool): Indicates if the evaluations should be included or excluded.
    """

    def __init__(self, eval_id: List[str], include: bool = True):
        """
        Initializes a new instance of ExecutionEvalFilter.

        Args:
            eval_id (List[str]): List of evaluation IDs.
            include (bool, optional): Indicates if the evaluations should be included or excluded.
        """
        self.eval_id = eval_id
        self.include = include

    def __getitem__(self, key: str) -> Any:
        return self.__dict__[key]
    
    def __getattr__(self, key: str) -> Any:
        return self.__dict__[key]
    
    def get(self, key: str, default: Any = None) -> Any:
        return self.__dict__.get(key, default)


class ExecutionDataFilter:
    """
    Represents a data filter for execution queries.

    Attributes:
        name (str): Name of the data field.
        value (Any): Value to filter on.
        type (DataType): Type of the data field.
        compare (CompareType): Comparison operator to use.
    """

    def __init__(
        self,
        name: str,
        value: Any,
        type: 'DataType' = 'DataType.TEXT',
        compare: 'CompareType' = 'CompareType.EQUAL',
    ):
        """
        Initializes a new instance of ExecutionDataFilter.

        Args:
            name (str): Name of the data field.
            value (Any): Value to filter on.
            type (DataType, optional): Type of the data field.
            compare (CompareType, optional): Comparison operator to use.
        """
        self.name = name
        self.value = value
        self.type = type
        self.compare = compare

    def to_json(self) -> Dict[str, Any]:
        """
        Converts the ExecutionDataFilter instance to a JSON-serializable dictionary.

        Returns:
            Dict[str, Any]: A dictionary representation of the ExecutionDataFilter.
        """
        return {
            "name": self.name,
            "value": self.value,
            "type": self.type.value,
            "compare": self.compare.value,
        }

    def __getitem__(self, key: str) -> Any:
        return self.__dict__[key]
    
    def __getattr__(self, key: str) -> Any:
        return self.__dict__[key]
    
    def get(self, key: str, default: Any = None) -> Any:
        return self.__dict__.get(key, default)


class ExecutionQueryModel:
    """
    Represents a query model for fetching executions.

    Attributes:
        date_from (str): Start date for the query.
        date_to (str): End date for the query.
        chamber_id_list (List[str]): List of chamber IDs.
        agent_id_list (List[str]): List of agent IDs.
        agent_deploy_id_list (List[str]): List of agent deployment IDs.
        user_id_list (List[str]): List of user IDs.
        session_id_list (List[str]): List of session IDs.
        channel_id_list (List[str]): List of channel IDs.
        data_filter_list (List[ExecutionDataFilter]): List of data filters.
        eval_id_user (ExecutionEvalFilter): User evaluation filter.
        eval_id_internal (ExecutionEvalFilter): Internal evaluation filter.
        eval_id_auto (ExecutionEvalFilter): Automatic evaluation filter.
        environment_id (Environtment): Environment identifier.
        is_test_plan (bool): Indicates if it's a test plan.
        finished (bool): Indicates if the execution is finished.
        limit (int): Limit of records per page.
        page_number (int): Page number for pagination.
        include_tags (bool): Include tags in the response.
        include_data (bool): Include data in the response.
        include_errors (bool): Include errors in the response.
        include_evals (bool): Include evaluations in the response.
    """

    def __init__(
        self,
        date_from: str,
        date_to: str,
        chamber_id_list: List[str] = None,
        agent_id_list: List[str] = None,
        agent_deploy_id_list: List[str] = None,
        user_id_list: List[str] = None,
        session_id_list: List[str] = None,
        channel_id_list: List[str] = None,
        data_filter_list: List[ExecutionDataFilter] = None,
        eval_id_user: Optional[ExecutionEvalFilter] = None,
        eval_id_internal: Optional[ExecutionEvalFilter] = None,
        eval_id_auto: Optional[ExecutionEvalFilter] = None,
        environment_id: Optional['Environtment'] = None,
        is_test_plan: Optional[bool] = None,
        finished: Optional[bool] = None,
        limit: int = 100,
        page_number: int = 1,
        include_tags: bool = False,
        include_data: bool = False,
        include_errors: bool = False,
        include_evals: bool = False,
    ):
        """
        Initializes a new instance of ExecutionQueryModel.

        Args:
            date_from (str): Start date for the query.
            date_to (str): End date for the query.
            chamber_id_list (List[str], optional): List of chamber IDs.
            agent_id_list (List[str], optional): List of agent IDs.
            agent_deploy_id_list (List[str], optional): List of agent deployment IDs.
            user_id_list (List[str], optional): List of user IDs.
            session_id_list (List[str], optional): List of session IDs.
            channel_id_list (List[str], optional): List of channel IDs.
            data_filter_list (List[ExecutionDataFilter], optional): List of data filters.
            eval_id_user (ExecutionEvalFilter, optional): User evaluation filter.
            eval_id_internal (ExecutionEvalFilter, optional): Internal evaluation filter.
            eval_id_auto (ExecutionEvalFilter, optional): Automatic evaluation filter.
            environment_id (Environtment, optional): Environment identifier.
            is_test_plan (bool, optional): Indicates if it's a test plan.
            finished (bool, optional): Indicates if the execution is finished.
            limit (int, optional): Limit of records per page.
            page_number (int, optional): Page number for pagination.
            include_tags (bool, optional): Include tags in the response.
            include_data (bool, optional): Include data in the response.
            include_errors (bool, optional): Include errors in the response.
            include_evals (bool, optional): Include evaluations in the response.
        """
        self.date_from = date_from
        self.date_to = date_to
        self.chamber_id_list = chamber_id_list or []
        self.agent_id_list = agent_id_list or []
        self.agent_deploy_id_list = agent_deploy_id_list or []
        self.user_id_list = user_id_list or []
        self.session_id_list = session_id_list or []
        self.channel_id_list = channel_id_list or []
        self.data_filter_list = data_filter_list or []
        self.eval_id_user = eval_id_user
        self.eval_id_internal = eval_id_internal
        self.eval_id_auto = eval_id_auto
        self.environment_id = environment_id
        self.is_test_plan = is_test_plan
        self.finished = finished
        self.limit = limit
        self.page_number = page_number
        self.include_tags = include_tags
        self.include_data = include_data
        self.include_errors = include_errors
        self.include_evals = include_evals

        if not date_from:
            raise ValueError("date_from is empty.")
        if not date_to:
            raise ValueError("date_to is empty.")
        if limit <= 0:
            raise ValueError("limit must be greater than 0.")
        if page_number < 0:
            raise ValueError("page_number must be 0 or greater.")

    def __getitem__(self, key: str) -> Any:
        return self.__dict__[key]
    
    def __getattr__(self, key: str) -> Any:
        return self.__dict__[key]
    
    def get(self, key: str, default: Any = None) -> Any:
        return self.__dict__.get(key, default)


class ExecutionResponseModel:
    """
    Represents the response model for an execution.

    Attributes:
        enola_id (str): Enola execution ID.
        enola_id_related (str): Related Enola execution ID.
        agent_deploy_id (str): Agent deployment ID.
        agent_deploy_name (str): Agent deployment name.
        agent_id (str): Agent ID.
        agent_name (str): Agent name.
        name (str): Execution name.
        start_dt (str): Start date and time of execution.
        end_dt (str): End date and time of execution.
        duration_ms (int): Duration in milliseconds.
        num_tracking (str): Number of tracking entries.
        is_test (bool): Indicates if the execution is a test.
        environment_id (str): Environment identifier.
        app_id (str): Application ID.
        app_name (str): Application name.
        user_id (str): User ID.
        user_name (str): User name.
        session_id (str): Session ID.
        session_name (str): Session name.
        channel (str): Channel ID.
        channel_name (str): Channel name.
        message_input (str): Input message.
        message_output (str): Output message.
        tag_json (json): JSON representation of tags.
        file_info_json (json): JSON representation of file information.
        data_json (json): JSON representation of data.
        error_or_warning_json (json): JSON representation of errors or warnings.
        step_api_data_json (json): JSON representation of API data.
        info_json (json): JSON representation of additional info.
        evals (json): JSON representation of evaluations.
        ip (str): IP address.
        num_iter (int): Number of iterations.
        external_id (str): External code API identifier.
        successfull (bool): Indicates if the execution was successful.
    """

    def __init__(
        self,
        agentExecId: str,
        agentExecIdRelated: str,
        agentDeployId: str,
        agentDeployName: str,
        agentId: str,
        agentName: str,
        agentExecName: str,
        agentExecStartDT: str,
        agentExecEndDT: str,
        agentExecDurationMs: int,
        agentExecNumTracking: str,
        agentExecIsTest: bool,
        environmentId: str,
        agentExecCliAppId: str,
        agentExecCliAppName: str,
        agentExecCliUserId: str,
        agentExecCliUserName: str,
        agentExecCliSessionId: str,
        agentExecCliSessionName: str,
        agentExecCliChannel: str,
        agentExecCliChannelName: str,
        agentExecMessageInput: str,
        agentExecMessageOutput: str,
        agentExecTagJson: json,
        agentExecFileInfoJson: json,
        agentExecDataJson: json,
        agentExecErrorOrWarningJson: json,
        agentExecStepApiDataJson: json,
        agentExecInfoJson: json,
        agentExecEvals: json,
        agentExecCliIP: str,
        agentExecCliNumIter: int,
        agentExecCliCodeApi: str,
        agentExecSuccessfull: bool,
        **args,
    ):
        """
        Initializes a new instance of ExecutionResponseModel.

        Args:
            All parameters correspond to execution response fields.
            **args: Additional keyword arguments.
        """
        self.enola_id = agentExecId
        self.enola_id_related = agentExecIdRelated
        self.agent_deploy_id = agentDeployId
        self.agent_deploy_name = agentDeployName
        self.agent_id = agentId
        self.agent_name = agentName
        self.name = agentExecName
        self.start_dt = agentExecStartDT
        self.end_dt = agentExecEndDT
        self.duration_ms = agentExecDurationMs
        self.num_tracking = agentExecNumTracking
        self.is_test = agentExecIsTest
        self.environment_id = environmentId
        self.app_id = agentExecCliAppId
        self.app_name = agentExecCliAppName
        self.user_id = agentExecCliUserId
        self.user_name = agentExecCliUserName
        self.session_id = agentExecCliSessionId
        self.session_name = agentExecCliSessionName
        self.channel = agentExecCliChannel
        self.channel_name = agentExecCliChannelName
        self.message_input = agentExecMessageInput
        self.message_output = agentExecMessageOutput
        self.tag_json = agentExecTagJson
        self.file_info_json = agentExecFileInfoJson
        self.data_json = agentExecDataJson
        self.error_or_warning_json = agentExecErrorOrWarningJson
        self.step_api_data_json = agentExecStepApiDataJson
        self.info_json = agentExecInfoJson
        self.evals = agentExecEvals
        self.ip = agentExecCliIP
        self.num_iter = agentExecCliNumIter
        self.external_id = agentExecCliCodeApi
        self.successfull = agentExecSuccessfull

    def __getitem__(self, key: str) -> Any:
        return self.__dict__[key]
    
    def __getattr__(self, key: str) -> Any:
        return self.__dict__[key]
    
    def get(self, key: str, default: Any = None) -> Any:
        return self.__dict__.get(key, default)


# ***********************************************************************************
# *************   E V A L U A T I O N   T Y P E S     ***********************************
# ***********************************************************************************

class EvaluationResultModel:
    """
    Represents the result of an evaluation process.

    Attributes:
        total_evals (int): Total number of evaluations processed.
        total_errors (int): Total number of errors encountered.
        total_success (int): Total number of successful evaluations.
        errors (List[Any]): List of errors.
    """

    def __init__(self, total_evals: int, total_errors: int, total_success: int, errors: List[Any]):
        """
        Initializes a new instance of EvaluationResultModel.

        Args:
            total_evals (int): Total number of evaluations processed.
            total_errors (int): Total number of errors encountered.
            total_success (int): Total number of successful evaluations.
            errors (List[Any]): List of errors.
        """
        self.total_evals = total_evals
        self.total_errors = total_errors
        self.total_success = total_success
        self.errors = errors

    def __getitem__(self, key: str) -> Any:
        return self.__dict__[key]
    
    def __getattr__(self, key: str) -> Any:
        return self.__dict__[key]
    
    def get(self, key: str, default: Any = None) -> Any:
        return self.__dict__.get(key, default)


class EvaluationDetailModel:
    """
    Represents the details of an individual evaluation.

    Attributes:
        eval_id (str): Evaluation identifier.
        value (float): Evaluation value.
        level (int): Evaluation level.
        comment (str): Evaluation comment.
    """

    def __init__(self, eval_id: str, comment: str, value: Optional[float] = None, level: Optional[int] = None):
        """
        Initializes a new instance of EvaluationDetailModel.

        Args:
            eval_id (str): Evaluation identifier.
            comment (str): Evaluation comment.
            value (float, optional): Evaluation value.
            level (int, optional): Evaluation level.
        """
        self.eval_id = eval_id
        self.value = value
        self.level = level
        self.comment = comment

    def __getitem__(self, key: str) -> Any:
        return self.__dict__[key]
    
    def __getattr__(self, key: str) -> Any:
        return self.__dict__[key]
    
    def get(self, key: str, default: Any = None) -> Any:
        return self.__dict__.get(key, default)


class ResultScore:
    """
    Represents the result of a score evaluation.

    Attributes:
        score_value_real (float): Actual score value.
        score_group_real (str): Actual score group.
        score_cluster_real (str): Actual score cluster.
        score_value_dif (float): Difference in score value.
        score_group_dif (str): Difference in score group.
        score_cluster_dif (str): Difference in score cluster.
    """

    def __init__(
        self,
        value_actual: float,
        group_actual: str,
        cluster_actual: str,
        value_dif: float,
        group_dif: str,
        cluster_dif: str,
    ):
        """
        Initializes a new instance of ResultScore.

        Args:
            value_actual (float): Actual score value.
            group_actual (str): Actual score group.
            cluster_actual (str): Actual score cluster.
            value_dif (float): Difference in score value.
            group_dif (str): Difference in score group.
            cluster_dif (str): Difference in score cluster.

        Raises:
            TypeError: If any of the parameters are not of the correct type.
        """
        if not self.__check_types(value_actual):
            raise TypeError("value_actual must be int, float, or str")
        if not self.__check_types(value_dif):
            raise TypeError("value_dif must be int, float, or str")
        if not self.__check_types(group_actual):
            raise TypeError("group_actual must be int, float, or str")
        if not self.__check_types(group_dif):
            raise TypeError("group_dif must be int, float, or str")
        if not self.__check_types(cluster_actual):
            raise TypeError("cluster_actual must be int, float, or str")
        if not self.__check_types(cluster_dif):
            raise TypeError("cluster_dif must be int, float, or str")

        self.score_value_real = value_actual
        self.score_group_real = group_actual
        self.score_cluster_real = cluster_actual
        self.score_value_dif = value_dif
        self.score_group_dif = group_dif
        self.score_cluster_dif = cluster_dif

    def __check_types(self, value: Any) -> bool:
        """
        Checks if the value is of an acceptable type.

        Args:
            value (Any): The value to check.

        Returns:
            bool: True if the value is int, float, or str; False otherwise.
        """
        return isinstance(value, (int, float, str))

    def to_json(self) -> Dict[str, Any]:
        """
        Converts the ResultScore instance to a JSON-serializable dictionary.

        Returns:
            Dict[str, Any]: A dictionary representation of the ResultScore.
        """
        return {
            "scoreValueReal": self.score_value_real,
            "scoreGroupReal": self.score_group_real,
            "scoreClusterReal": self.score_cluster_real,
            "scoreValueDif": self.score_value_dif,
            "scoreGroupDif": self.score_group_dif,
            "scoreClusterDif": self.score_cluster_dif,
            "messageOutputBest": "",
        }

    def __getitem__(self, key: str) -> Any:
        return self.__dict__[key]

    def __getattr__(self, key: str) -> Any:
        return self.__dict__[key]

    def get(self, key: str, default: Any = None) -> Any:
        return self.__dict__.get(key, default)


class ResultLLM:
    """
    Represents the result of a language model evaluation.

    Attributes:
        message_output_best (str): The best output message from the model.
    """

    def __init__(self, message_output_best: str):
        """
        Initializes a new instance of ResultLLM.

        Args:
            message_output_best (str): The best output message from the model.
        """
        self.message_output_best = message_output_best

    def to_json(self) -> Dict[str, Any]:
        """
        Converts the ResultLLM instance to a JSON-serializable dictionary.

        Returns:
            Dict[str, Any]: A dictionary representation of the ResultLLM.
        """
        return {
            "scoreValueReal": 0,
            "scoreGroupReal": "",
            "scoreClusterReal": "",
            "scoreValueDif": 0,
            "scoreGroupDif": "",
            "scoreClusterDif": "",
            "messageOutputBest": self.message_output_best,
        }

    def __getitem__(self, key: str) -> Any:
        return self.__dict__[key]

    def __getattr__(self, key: str) -> Any:
        return self.__dict__[key]

    def get(self, key: str, default: Any = None) -> Any:
        return self.__dict__.get(key, default)
    

class EvaluationModel:
    """
    Represents an evaluation model containing evaluation details and results.

    Attributes:
        enola_id (str): The Enola execution ID associated with the evaluation.
        eval_type (str): The type of evaluation (e.g., 'AUTO', 'USER', 'INTERNAL').
        evals (List[EvaluationDetailModel]): A list of evaluation details.
        enola_sender (EnolaSenderModel): The sender information for the evaluation.
        result_score (Optional[ResultScore]): The result score data, if applicable.
        result_llm (Optional[ResultLLM]): The result from a language model, if applicable.
    """

    def __init__(
        self,
        enola_id: str,
        eval_type: 'EvalType',
        enola_sender: 'EnolaSenderModel',
        result_score: Optional['ResultScore'] = None,
        result_llm: Optional['ResultLLM'] = None,
    ):
        """
        Initializes a new instance of EvaluationModel.

        Args:
            enola_id (str): The Enola execution ID associated with the evaluation.
            eval_type (EvalType): The type of evaluation.
            enola_sender (EnolaSenderModel): The sender information for the evaluation.
            result_score (ResultScore, optional): The result score data.
            result_llm (ResultLLM, optional): The result from a language model.
        """
        self.enola_id = enola_id
        self.eval_type = eval_type.value
        self.evals: List['EvaluationDetailModel'] = []
        self.enola_sender = enola_sender
        self.result_score = result_score
        self.result_llm = result_llm

    def add_eval(self, eval_detail: 'EvaluationDetailModel') -> None:
        """
        Adds an evaluation detail to the evaluation model.

        Args:
            eval_detail (EvaluationDetailModel): The evaluation detail to add.
        """
        self.evals.append(eval_detail)

    def to_json(self) -> Dict[str, Any]:
        """
        Converts the EvaluationModel instance to a JSON-serializable dictionary.

        Returns:
            Dict[str, Any]: A dictionary representation of the EvaluationModel.
        """
        results_json = None
        if self.result_score is not None:
            results_json = self.result_score.to_json()
        elif self.result_llm is not None:
            results_json = self.result_llm.to_json()

        result = {
            "enolaId": self.enola_id,
            "evalType": self.eval_type,
            "sender": {
                "app_id": self.enola_sender.app_id,
                "app_name": self.enola_sender.app_name,
                "user_id": self.enola_sender.user_id,
                "user_name": self.enola_sender.user_name,
                "session_id": self.enola_sender.session_id,
                "session_name": self.enola_sender.session_name,
                "channel_id": self.enola_sender.channel_id,
                "channel_name": self.enola_sender.channel_name,
                "ip": self.enola_sender.ip,
            },
            "results": results_json,
            "evals": {
                item.eval_id: {
                    "value": item.value,
                    "level": item.level,
                    "comment": item.comment,
                }
                for item in self.evals
            },
        }
        return result

    def __getitem__(self, key: str) -> Any:
        return self.__dict__[key]

    def __getattr__(self, key: str) -> Any:
        return self.__dict__.get(key)

    def get(self, key: str, default: Optional[Any] = None) -> Any:
        return self.__dict__.get(key, default)


class EvaluationResponseModel:
    """
    Represents the response model for an evaluation submission.

    Attributes:
        enola_id (Optional[str]): The Enola execution ID.
        agent_deploy_id (Optional[str]): The agent deployment ID.
        enola_eval_id (Optional[str]): The Enola evaluation ID.
        successfull (Optional[bool]): Indicates if the evaluation submission was successful.
        message (str): Response message.
        args (Dict[str, Any]): Additional arguments or data.
    """

    def __init__(
        self,
        enola_id: str = "",
        agent_deploy_id: str = "",
        enola_eval_id: str = "",
        successfull: Optional[bool] = True,
        message: str = "",
        **args,
    ):
        """
        Initializes a new instance of EvaluationResponseModel.

        Args:
            enola_id (str, optional): The Enola execution ID.
            agent_deploy_id (str, optional): The agent deployment ID.
            enola_eval_id (str, optional): The Enola evaluation ID.
            successfull (bool, optional): Indicates if the evaluation submission was successful.
            message (str, optional): Response message.
            **args: Additional keyword arguments.
        """
        self.enola_id = enola_id or args.get("enolaId")
        self.agent_deploy_id = agent_deploy_id or args.get("agentDeployId")
        self.enola_eval_id = enola_eval_id or args.get("enolaEvalId")
        self.successfull = successfull if successfull != "" else args.get("IsSuccessfull")
        self.message = message
        self.args = args

    def to_json(self) -> Dict[str, Any]:
        """
        Converts the EvaluationResponseModel instance to a JSON-serializable dictionary.

        Returns:
            Dict[str, Any]: A dictionary representation of the EvaluationResponseModel.
        """
        return {
            "enolaId": self.enola_id,
            "agentDeployId": self.agent_deploy_id,
            "enolaEvalId": self.enola_eval_id,
            "successfull": self.successfull,
            "message": self.message,
            "args": self.args,
        }

    def __getitem__(self, key: str) -> Any:
        return self.__dict__[key]

    def __getattr__(self, key: str) -> Any:
        return self.__dict__.get(key)

    def get(self, key: str, default: Optional[Any] = None) -> Any:
        return self.__dict__.get(key, default)