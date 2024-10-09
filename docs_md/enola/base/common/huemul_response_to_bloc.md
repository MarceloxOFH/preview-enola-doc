Module enola.base.common.huemul_response_to_bloc
================================================

Classes
-------

`HuemulResponseToBloc(connect_object: enola.base.connect.Connect, **args)`
:   

    ### Ancestors (in MRO)

    * enola.base.common.huemul_response_provider.HuemulResponseProvider

    ### Descendants

    * enola.base.common.auth.auth_service_provider.AuthServiceProvider
    * enola.base.internal.evaluation.enola_evaluation_provider.EnolaEvaluationProvider
    * enola.base.internal.executions.enola_execution_provider.EnolaExecutionProvider
    * enola.base.internal.tracking.enola_tracking_provider.EnolaTrackingProvider
    * enola.base.internal.tracking_batch.enola_tracking_batch_provider.EnolaTrackingBatchProvider

    ### Methods

    `analyze_errors(self, attempt)`
    :

    `from_response_provider(self, huemul_response_provider: enola.base.common.huemul_response_provider.HuemulResponseProvider)`
    :

    `get(self, key, default=None)`
    :