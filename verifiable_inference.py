from giza_actions.model import GizaModel
from giza_actions.action import action
from giza_actions.task import task
import numpy as np

MODEL_ID = 517  # Update with your model ID
VERSION_ID = 2  # Update with your version ID

@task(name="PredictLRModel")
def prediction(input, model_id, version_id):
    model = GizaModel(id=model_id, version=version_id)

    (result, proof_id) = model.predict(
        input_feed={'input': input}, verifiable=True
    )

    return result, proof_id

@action(name="ExectuteCairoLR", log_prints=True)
def execution():
    # The input data type should match the model's expected input
    input = np.array([[0.1003661394, 0.01903314439, 0.0008148991632, 23429565.78, 1628.669107, 1575.53932, 23094495.2, 1602.100647, 0.1016602355, 0.0206123013]]).astype(np.float32)

    (result, proof_id) = prediction(input, MODEL_ID, VERSION_ID)

    print(f"Predicted value is {result[0].flatten()[0]}")
    print("Proof_id", proof_id)

    return result, proof_id

execution()