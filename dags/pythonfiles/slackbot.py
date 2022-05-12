# JngMkk
from airflow.providers.slack.operators.slack import SlackAPIPostOperator
from dateutil.relativedelta import relativedelta

class Slack:

    def __init__(self, channel):
        self.channel = channel
        self.token = 'xoxb-3504505764613-3508114144178-8JmAL6cFYvU0L27hPGHTFyR6'

    def fail(self, context): 
        alert = SlackAPIPostOperator(
                                task_id='slack_failed',
                                channel=self.channel,
                                token=self.token,
                                text="""result : fail\ntask : {t}\nexec time : {e}\nnext exec time : {n}\nlog : {l}
                                    """.format(
                                        t=context.get('task_instance').task_id,
                                        d=context.get('task_instance').dag_id,
                                        e=(context.get('execution_date') + relativedelta(hours=9)).strftime('%Y-%m-%d %H:%M:%S'),
                                        n=(context.get('next_execution_date') + relativedelta(hours=9)).strftime('%Y-%m-%d %H:%M:%S'),
                                        l=context.get('task_instance').log_url.replace("localhost", "13.115.204.241")
                                    )
                                )
        return alert.execute(context=context)
    def success(self, context):
        alert = SlackAPIPostOperator(
                                task_id='slack_success',
                                channel=self.channel,
                                token=self.token,
                                text="""result : success\ntask : {t}\nexec time : {e}\nlog : {l}
                                """.format(
                                    t=context.get('task_instance').task_id,
                                    d=context.get('task_instance').dag_id,
                                    e=(context.get('execution_date') + relativedelta(hours=9)).strftime('%Y-%m-%d %H:%M:%S'),
                                    l=context.get('task_instance').log_url).replace("localhost", "13.115.204.241")
                                )
        return alert.execute(context=context)
