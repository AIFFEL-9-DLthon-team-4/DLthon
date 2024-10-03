import copy
import evaluate
from typing import Any, Dict, List, NamedTuple, Optional, Tuple, Union

def default_compute_objective(metrics: Dict[str, float]) -> float:
    """
    In `transformers/src/transformers/trainer_utils.py` - line 265 (24.Oct.3)
    
    The default objective to maximize/minimize when doing an hyperparameter search. It is the evaluation loss if no
    metrics are provided to the [`Trainer`], the sum of all metrics otherwise.

    Args:
        metrics (`Dict[str, float]`): The metrics returned by the evaluate method.

    Return:
        `float`: The objective to minimize or maximize
    """
    metrics = copy.deepcopy(metrics)
    loss = metrics.pop("eval_loss", None)
    _ = metrics.pop("epoch", None)
    # Remove speed metrics
    speed_metrics = [
        m
        for m in metrics.keys()
        if m.endswith("_runtime") or m.endswith("_per_second") or m.endswith("_compilation_time")
    ]
    for sm in speed_metrics:
        _ = metrics.pop(sm, None)
    return loss if len(metrics) == 0 else sum(metrics.values())


def compute_f1_objective(metrics: Dict[str, float]) -> float:
    f1_metric = evaluate.load("f1")
    results = f1_metric.compute(predictions=[0, 1], references=[0, 1])
    return results