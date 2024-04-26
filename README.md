# Safe-Looping


giza transpile linear_regression.onnx --output-path verifiable_lr
giza endpoints deploy --model-id 517 --version-id 2
https://endpoint-rodriguezmatid-517-2-e5a2ea0d-7i3yxzspbq-ew.a.run.app
giza workspaces get
python3 verifiable_inference
giza endpoints get-proof --endpoint-id 156 --proof-id b229901247874c7eb856fab2f48e9f0e
giza endpoints download-proof --endpoint-id 156 --proof-id b229901247874c7eb856fab2f48e9f0e

Model id 517, id version 2, endpoint id 156