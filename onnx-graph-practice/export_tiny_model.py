"""Export a tiny PyTorch model to ONNX.

The exported model is intentionally small so that its computation graph is easy
to inspect. The model contains Linear and ReLU operations, which usually appear
as Gemm/MatMul/Add and Relu-like nodes in ONNX depending on exporter settings.
"""

from __future__ import annotations

import warnings
from pathlib import Path

import torch
from torch import nn


class TinyModel(nn.Module):
    def __init__(self) -> None:
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(4, 3),
            nn.ReLU(),
            nn.Linear(3, 2),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.net(x)


def main() -> None:
    output_path = Path("tiny_model.onnx")
    torch.manual_seed(0)

    model = TinyModel()
    model.eval()

    dummy_input = torch.randn(1, 4)

    warnings.filterwarnings(
        "ignore",
        category=DeprecationWarning,
        message=".*legacy TorchScript-based ONNX export.*",
    )

    torch.onnx.export(
        model,
        dummy_input,
        output_path,
        input_names=["input"],
        output_names=["output"],
        dynamic_axes={
            "input": {0: "batch_size"},
            "output": {0: "batch_size"},
        },
        opset_version=17,
        external_data=False,
        dynamo=False,
    )

    print(f"Exported ONNX model to {output_path.resolve()}")


if __name__ == "__main__":
    main()
