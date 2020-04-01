import time
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.dummy_operator import DummyOperator

# Default task arguments
# https://airflow.apache.org/docs/stable/_api/airflow/operators/index.html#package-contents
default_args = {
    "owner": "airflow",
    "depends_on_past": False,  #
    "start_date": datetime(2020, 4, 1),
    "email": ["airflow@airflow.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(seconds=5),
}


# ** to unpack keyword arguments
def fetch_example_data(my_param, **context):
    print("Params", my_param)
    return "Liftoff! We have a liftoff"


def parallel_task(random_base, **context):
    message_from_task = context["task_instance"].xcom_pull(
        task_ids="fetch_example_data"
    )
    print("message_from_task ---> ", message_from_task)
    time.sleep(random_base)


def notify_users(**context):
    try_number = context["task_instance"].try_number
    if try_number != 3:
        raise Exception("Houston, we have a problem.")


with DAG("example", default_args=default_args, schedule_interval="@hourly") as dag:
    # Using BashOperator
    list_dir = BashOperator(
        task_id="list_dir", depends_on_past=False, bash_command="ls -la",
    )

    # PythonOperator with parameter and returned value
    fetch_data = PythonOperator(
        task_id="fetch_example_data",
        provide_context=True,
        python_callable=fetch_example_data,
        op_kwargs={"my_param": "Parameter I passed in"},
    )

    # DummyOperator
    update_data_or_checkpoint = DummyOperator(task_id="update_data_or_checkpoint")

    # Dynamic tasks, sleeping from 0.0 to 4 seconds respectively.
    # Using xcom_pull to get returned value from tasks.
    for i in range(4):
        task = PythonOperator(
            task_id="parallel_task_" + str(i),
            python_callable=parallel_task,
            provide_context=True,
            op_kwargs={"random_base": (float(i) / 10) * 10},
        )

        fetch_data >> task >> update_data_or_checkpoint

    # Task with failure
    notify = PythonOperator(
        task_id="notify_users",
        python_callable=notify_users,
        provide_context=True,
        retries=3,
        retry_delay=timedelta(seconds=10),
    )

    update_data_or_checkpoint >> notify

    list_dir >> fetch_data
