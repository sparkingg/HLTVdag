from datetime import datetime
from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.operators.python import PythonOperator
import json
from airflow.models import XCom
import pendulum
from functions import parsing_html_code,parsing_results


with DAG(
        dag_id='hltv_results_parsing',
        start_date=datetime(2021, 5, 29),
        schedule_interval='@hourly',
        ) as dag:

    create_table = PostgresOperator(
        task_id='create_table',
        sql='create_table.sql',
        postgres_conn_id='postgres_default',
    )
    parsing_hltv = PythonOperator(
        task_id='parsing_resuls',
        python_callable=parsing_results,
        dag=dag,
        
    )
    
    results = XCom.get_many(execution_date=pendulum.now(),task_ids='parsing_hltv')   
    #json file: {"/matches/2348797/alternate-attax-vs-nemiga-esea-premier-season-37-europe": [113, 56, 22, 34, 0, 0, 0, 1, 1], 
                    #"/matches/2349094/dire-wolves-vs-rooster-epic-league-oceania-2021": [83, 154, 25, 11, 0, 0, 1, 2, 2]...}
    tasks = []

    for key,value in results:
        rank1 = value[0]
        rank2 = value[1]
        count_matches1 = value[2]
        count_matches2 = value[3]
        wr1 = value[4]
        wr2 = value[5]
        streak1 = value[6]
        streak2 = value[7]
        won = value[8]     
        insert_rate = PostgresOperator(
            task_id='insert_results_{ value }',
            postgres_conn_id='postgres_default',
            sql='insert.sql'
        )
        params={
            'rank1': base,
            'rank2': currency,
            'count_matches1':count_matches1,
            'count_matches2': count_matches2,
            'wr1':wr1,
            'wr2':wr2,
            'streak1': streak1,
            'streak2': streak2,
            'won': won,
            
        }
        insert_rate
        tasks.append(insert_rate)
    print(tasks)
    create_table>>parsing_hltv>>tasks
    

