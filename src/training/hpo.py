"""
Hyper-Parameter Optimization (HPO)
"""

import evaluate
import transformers
from optuna import trial
from transformers import Trainer
from transformers.trainer_utils import BestRun
from typing import List

f1_metric = evaluate.load("f1")
f1_metric_results = f1_metric.compute(predictions=[0, 1], references=[0, 1])

class HyperParmeterOptimize:
    def __init__(self, trainer: Trainer):
        self.trainer = trainer
        
    def optuna_hp_space(self, trial: trial.Trial):
        return {
            "num_neurons"   : trial.suggest_int("num_neurons",
                                                low=16,
                                                high=256),
            "num_layers"    : trial.suggest_int("num_layers",
                                                low=1,
                                                high=3),
            "learning_rate" : trial.suggest_float("learning_rate",
                                                  low=1e-6,
                                                  high=1e-4,
                                                  log=True),  # 학습률은 작은 값의 차이에서도 영향을 받으므로, log scale에서 샘플링
            "optimizer"     : trial.suggest_categorical("optimizer",
                                                        choices=["AdamW",
                                                                 "AdaFactor"
                                                                ]),
            "per_device_train_batch_size": trial.suggest_categorical("per_device_train_batch_size",
                                                                     [16, 32, 64, 128]),
        }

    def get_best_trials(self) -> BestRun | List[BestRun]:
        return self.trainer.hyperparameter_search(
            # direction=["minimize", "maximize"],
            direction="maximize",
            backend="optuna",
            hp_space=self.optuna_hp_space,
            n_trials=20,
            compute_objective=f1_metric_results,  # 기본값은 [`~trainer_utils.default_compute_objective`] 함수로 설정
        )
