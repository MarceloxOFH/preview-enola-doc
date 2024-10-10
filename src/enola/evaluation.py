from typing import Any, List, Optional
import jwt
from enola.base.common.huemul_functions import HuemulFunctions
from enola.base.internal.evaluation.enola_evaluation import create_evaluation
from enola.base.common.auth.auth_model import AuthModel
from enola.enola_types import (
    EnolaSenderModel,
    EvalType,
    EvaluationDetailModel,
    EvaluationModel,
    EvaluationResultModel,
    ResultLLM,
    ResultScore,
    TokenInfo,
)
from enola.base.connect import Connect


class Evaluation:
    """
    The `Evaluation` class provides methods to evaluate executions in the Enola system.

    This class allows you to:

    - Initialize an evaluation session.
    - Add evaluations by value or level.
    - Execute the evaluations and send the data to the Enola server.
    """

    def __init__(
        self,
        token: str,
        eval_type: EvalType = EvalType.AUTO,
        result_score: Optional[ResultScore] = None,
        result_llm: Optional[ResultLLM] = None,
        app_id: Optional[str] = None,
        user_id: Optional[str] = None,
        session_id: Optional[str] = None,
        channel_id: Optional[str] = None,
        ip: Optional[str] = None,
        app_name: str = "",
        user_name: str = "",
        session_name: str = "",
        channel_name: str = "",
    ):
        """
        Initializes a new `Evaluation` instance.

        Args:
            token (str): JWT token, used to identify the agent.
            eval_type (EvalType, optional): Type of evaluation (AUTO, USER, INTERNAL).
            result_score (ResultScore, optional): Actual results of score.
            result_llm (ResultLLM, optional): Actual results of LLM.
            app_id (str, optional): ID of the app calling the evaluation.
            user_id (str, optional): External user ID.
            session_id (str, optional): Session ID of the user or application.
            channel_id (str, optional): Communication channel ID.
            ip (str, optional): IP address of the user or application.
            app_name (str, optional): Name of the app.
            user_name (str, optional): Name of the user.
            session_name (str, optional): Name of the session.
            channel_name (str, optional): Name of the channel.
        """
        self.hf = HuemulFunctions()
        self.eval_type = eval_type
        self.result_score = result_score
        self.result_llm = result_llm

        # Decode JWT token
        self.token_info = TokenInfo(token=token)

        if not self.token_info.is_service_account:
            raise Exception(
                "This token is not a service account. Only service accounts can execute evaluations."
            )

        if (
            self.token_info.is_service_account
            and not self.token_info.service_account_can_evaluate
        ):
            raise Exception("Service Account can't evaluate")

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
            app_name=app_name,
            user_id=user_id,
            user_name=user_name,
            session_id=session_id,
            session_name=session_name,
            channel_id=channel_id,
            channel_name=channel_name,
            batch_id="",
            client_id="",
            external_id="",
            product_id="",
            ip=ip,
        )

        # Current date
        self.date_start = self.hf.get_date_for_api()
        self.executions: List[EvaluationModel] = []

    ########################################################################################
    ###############    E V A L U A T I O N     M E T H O D S     ###########################
    ########################################################################################

    def execution_exists(self, enola_id: str) -> Optional[EvaluationModel]:
        """
        Checks if an execution exists.

        Args:
            enola_id (str): ID of Enola execution.

        Returns:
            Optional[EvaluationModel]: The evaluation model if it exists, None otherwise.
        """
        for item in self.executions:
            if item.enola_id == enola_id:
                return item
        return None

    def add_evaluation(
        self, enola_id: str, eval_id: str, value: float, comment: str
    ) -> None:
        """
        Adds an evaluation by value.

        Args:
            enola_id (str): ID of Enola execution.
            eval_id (str): ID of evaluation.
            value (float): Value of evaluation.
            comment (str): Comment of evaluation.
        """
        eval_detail = EvaluationDetailModel(
            eval_id=eval_id, value=value, comment=comment
        )
        execution = self.execution_exists(enola_id)

        if execution is None:
            execution = EvaluationModel(
                enola_id,
                eval_type=self.eval_type,
                enola_sender=self.enola_sender,
                result_score=self.result_score,
                result_llm=self.result_llm,
            )
            self.executions.append(execution)

        execution.add_eval(eval_detail)

    def add_evaluation_by_level(
        self, enola_id: str, eval_id: str, level: int, comment: str
    ) -> None:
        """
        Adds an evaluation by level.

        Args:
            enola_id (str): ID of Enola execution.
            eval_id (str): ID of evaluation.
            level (int): Level from 1 to 5.
            comment (str): Comment of evaluation.
        """
        eval_detail = EvaluationDetailModel(
            eval_id=eval_id, level=level, comment=comment
        )
        execution = self.execution_exists(enola_id)

        if execution is None:
            execution = EvaluationModel(
                enola_id,
                eval_type=self.eval_type,
                enola_sender=self.enola_sender,
            )
            self.executions.append(execution)

        execution.add_eval(eval_detail)

    def execute(self) -> EvaluationResultModel:
        """
        Executes the evaluations.

        Returns:
            EvaluationResultModel: The result of the evaluations.
        """
        final_result = EvaluationResultModel(
            total_evals=len(self.executions),
            total_errors=0,
            total_success=0,
            errors=[],
        )

        for item in self.executions:
            result = create_evaluation(
                evaluation_model=item, connection=self.connection
            )
            if not result.successfull:
                print(result.errors)
                print(result.message)
                final_result.errors.append(result.message)

        return final_result

    def __getitem__(self, key: str) -> Any:
        return self.__dict__[key]

    def __getattr__(self, key: str) -> Any:
        return self.__dict__[key]

    def get(self, key: str, default: Optional[Any] = None) -> Any:
        return self.__dict__.get(key, default)
