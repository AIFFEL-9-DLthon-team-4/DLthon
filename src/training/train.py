from hpo import HyperParmeterOptimize
from config.trainer_case import trainer_02

case_1 = HyperParmeterOptimize(trainer_02)

print("Best Trials: ", case_1.get_best_trials())