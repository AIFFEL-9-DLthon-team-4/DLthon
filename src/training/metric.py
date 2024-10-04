import evaluate

f1_metric = evaluate.load("f1")
f1_metric_results = f1_metric.compute(predictions=[0, 1], references=[0, 1])
