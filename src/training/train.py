from hpo import HyperParmeterOptimize
from config.trainer_case import KoBert

case_1 = HyperParmeterOptimize()

# Fine-Tuning for Classification
from sentence_transformers.losses import CosineSimilarityLoss
#train_loss = CosineSimilarityLoss(model=model)

with torch.no_grad():
    logits = model(inputs).logits

predicted_class_ids = torch.arange(0, logits.shape[-1])[torch.sigmoid(logits).squeeze(dim=0) > 0.5]
labels = torch.sum(
    torch.nn.functional.one_hot(predicted_class_ids[None, :].clone(), num_classes=num_labels), dim=1
).to(torch.float)

loss = model(inputs, labels=labels).loss