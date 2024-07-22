# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.


from datetime import datetime
import os
from airflow.models import DAG
from airflow.operators.dummy import DummyOperator
from airflow.operators.bash import BashOperator

DBT_PROJECT_ID = 70403103942862
DBT_JOB_ID = 70403103955147
DBT_ACCT_ID = 70403103936947


with DAG(
    dag_id="test_dbt_dag",
    default_args={"dbt_cloud_conn_id": "airflow-token", "account_id": DBT_ACCT_ID},
    start_date=datetime(2021, 1, 1),
    schedule_interval=None,
    catchup=False,
) as dag:
    extract = DummyOperator(task_id="extract")
    load = DummyOperator(task_id="load")
    ml_training = DummyOperator(task_id="ml_training")

    # trigger_dbt_cloud_job_run = DbtCloudRunJobOperator(
    #     task_id="trigger_dbt_cloud_job_run",
    #     account_id=DBT_ACCT_ID,
    #     job_id=DBT_JOB_ID,
    #     check_interval=10,
    #     timeout=300,
    # )

    dbt_task = BashOperator(
        task_id="dbt_task",
        bash_command=f"cd /opt/airflow/dbt/ && dbt deps && dbt debug --config-dir && dbt run"
    )

    extract >> load >> dbt_task >> ml_training