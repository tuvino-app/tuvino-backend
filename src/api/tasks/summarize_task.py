from fastapi import BackgroundTasks
import logging
import time

class SummarizeTask:
    def __init__(self, background_tasks: BackgroundTasks):
        logging.info('SummarizeTask ready')
        self.background_tasks = background_tasks

    def _run_actual_task(self, wine_id: int, ratings: list):
        logging.info(f'Starting to summarize wine with id {wine_id}')

        time.sleep(10)  # Simulación de la tarea larga

        logging.info(f'New wine summary for id {wine_id} ready')

    def schedule_summary(self, wine_id: int, ratings: list):
        self.background_tasks.add_task(
            self._run_actual_task,
            wine_id,
            ratings
        )