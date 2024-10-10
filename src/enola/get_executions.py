from typing import Any, List, Optional
from enola.base.common.auth.auth_model import AuthModel
from enola.base.common.huemul_functions import HuemulFunctions
from enola.base.connect import Connect
from enola.base.internal.executions.enola_execution import get_execution
from enola.enola_types import (
    Environtment,
    ExecutionEvalFilter,
    ExecutionModel,
    ExecutionQueryModel,
    TokenInfo,
)


class GetExecutions:
    """
    The `GetExecutions` class provides methods to retrieve executions from the Enola system.

    This class allows you to:

    - Initialize a retrieval session.
    - Query executions based on various filters.
    - Fetch subsequent pages of results.
    """

    def __init__(self, token: str, raise_error_if_fail: bool = True):
        """
        Initializes a new `GetExecutions` instance.

        Args:
            token (str): JWT token used to identify the agent.
            raise_error_if_fail (bool, optional): Whether to raise an error if the retrieval fails.
        """
        self.raise_error_if_fail = raise_error_if_fail
        self.num_rows_acum = 0
        self.num_rows = 0
        self.continue_execution = False
        self.hf = HuemulFunctions()
        # Connection data

        # Get token info
        self.token_info = TokenInfo(token=token)

        if (
            self.token_info.is_service_account
            and not self.token_info.service_account_can_get_executions
        ):
            raise Exception("Service Account Token is not allowed to get executions")

        self.connection = Connect(
            AuthModel(
                jwt_token=token,
                url_service=self.token_info.service_account_url_backend,
                org_id=self.token_info.org_id,
            )
        )

    def get_next_page(self) -> ExecutionModel:
        """
        Retrieves the next page of results.

        Returns:
            ExecutionModel: The execution model containing the results.
        """
        if not self.continue_execution:
            raise Exception("No more data to show.")

        self.execution_query_model.page_number += 1
        enola_result = self.__run_query()

        # Show results
        return enola_result

    def get_page_number(self) -> int:
        """
        Gets the current page number.

        Returns:
            int: The current page number.
        """
        return self.execution_query_model.page_number

    def query(
        self,
        date_from: str,
        date_to: str,
        chamber_id_list: Optional[List[str]] = None,
        agent_id_list: Optional[List[str]] = None,
        agent_deploy_id_list: Optional[List[str]] = None,
        user_id_list: Optional[List[str]] = None,
        session_id_list: Optional[List[str]] = None,
        channel_id_list: Optional[List[str]] = None,
        data_filter_list: Optional[List[Any]] = None,
        eval_id_user: Optional[ExecutionEvalFilter] = None,
        eval_id_internal: Optional[ExecutionEvalFilter] = None,
        eval_id_auto: Optional[ExecutionEvalFilter] = None,
        environment_id: Optional[Environtment] = None,
        is_test_plan: Optional[bool] = None,
        finished: Optional[bool] = None,
        limit: int = 100,
        include_tags: bool = False,
        include_data: bool = False,
        include_errors: bool = False,
        include_evals: bool = False,
    ) -> ExecutionModel:
        """
        Queries executions based on various filters.

        Args:
            date_from (str): Start date.
            date_to (str): End date.
            chamber_id_list (List[str], optional): List of chamber IDs.
            agent_id_list (List[str], optional): List of agent IDs.
            agent_deploy_id_list (List[str], optional): List of agent deploy IDs.
            user_id_list (List[str], optional): List of user IDs.
            session_id_list (List[str], optional): List of session IDs.
            channel_id_list (List[str], optional): List of channel IDs.
            data_filter_list (List[Any], optional): List of data filters.
            eval_id_user (ExecutionEvalFilter, optional): User evaluation filter.
            eval_id_internal (ExecutionEvalFilter, optional): Internal evaluation filter.
            eval_id_auto (ExecutionEvalFilter, optional): Auto evaluation filter.
            environment_id (Environtment, optional): Environment ID.
            is_test_plan (bool, optional): Whether it's a test plan.
            finished (bool, optional): Whether execution is finished.
            limit (int, optional): Limit of results per page.
            include_tags (bool, optional): Whether to include tags.
            include_data (bool, optional): Whether to include data.
            include_errors (bool, optional): Whether to include errors.
            include_evals (bool, optional): Whether to include evaluations.

        Returns:
            ExecutionModel: The execution model containing the results.
        """
        chamber_id_list = chamber_id_list or []
        agent_id_list = agent_id_list or []
        agent_deploy_id_list = agent_deploy_id_list or []

        if (
            self.token_info.agent_deploy_id
            and self.token_info.agent_deploy_id != "0"
        ):
            if len(agent_deploy_id_list) > 1:
                raise Exception(
                    "Service Account Token is not allowed to access more than one agent_deploy_id",
                    self.token_info.agent_deploy_id,
                )
            if len(agent_deploy_id_list) == 1:
                if self.token_info.agent_deploy_id != agent_deploy_id_list[0]:
                    raise Exception(
                        "Service Account Token is not allowed to access this agent_deploy_id",
                        self.token_info.agent_deploy_id,
                    )
            else:
                agent_deploy_id_list = [self.token_info.agent_deploy_id]

        if not chamber_id_list and not agent_id_list and not agent_deploy_id_list:
            raise Exception(
                "chamber_id or agent_id or agent_deploy_id must be filled."
            )

        self.num_rows_acum = 0
        self.num_rows = 0
        self.continue_execution = True

        self.execution_query_model = ExecutionQueryModel(
            date_from=date_from,
            date_to=date_to,
            chamber_id_list=chamber_id_list,
            agent_id_list=agent_id_list,
            agent_deploy_id_list=agent_deploy_id_list,
            user_id_list=user_id_list,
            session_id_list=session_id_list,
            channel_id_list=channel_id_list,
            data_filter_list=data_filter_list,
            eval_id_user=eval_id_user,
            eval_id_internal=eval_id_internal,
            eval_id_auto=eval_id_auto,
            environment_id=environment_id,
            is_test_plan=is_test_plan,
            finished=finished,
            limit=limit,
            page_number=0,
            include_tags=include_tags,
            include_data=include_data,
            include_errors=include_errors,
            include_evals=include_evals,
        )

    def __run_query(self) -> ExecutionModel:
        """
        Runs the query using the current execution query model.

        Returns:
            ExecutionModel: The execution model containing the results.
        """
        enola_result = get_execution(
            execution_query_model=self.execution_query_model,
            connection=self.connection,
            raise_error_if_fail=self.raise_error_if_fail,
        )

        self.num_rows = len(enola_result.data)

        self.continue_execution = False
        if (
            self.num_rows == self.execution_query_model.limit
            and self.num_rows != 0
        ):
            self.continue_execution = True

        self.num_rows_acum += self.num_rows

        return enola_result

    def __getitem__(self, key: str) -> Any:
        return self.__dict__[key]

    def __getattr__(self, key: str) -> Any:
        return self.__dict__[key]

    def get(self, key: str, default: Optional[Any] = None) -> Any:
        return self.__dict__.get(key, default)
