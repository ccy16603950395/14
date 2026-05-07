# pinn_mvp（PyTorch 轻量真 PINN v1）

本项目用于岩石三轴压缩 COMSOL 数据的内部场反演：

**输入**：表面 DIC 统计特征 + 全局工况 + 内部点坐标（含 `r`,`theta`）  
**输出**：内部 `solid.mises (N/m^2)`

## v1 变化（相对纯 MLP）
- 网络输出扩展为 `u,v,w,mises`。
- 训练总损失：
  - 数据损失（监督 `mises`）
  - von Mises 一致性损失（由位移梯度+线弹性本构计算应力再计算 mises）
  - 静力平衡残差损失（`div(sigma)=0`）
- 通过 `torch.autograd` 对坐标求导，形成 PDE 约束。

## 项目结构
- `config.py`：路径、case 划分、训练参数、PINN 权重
- `data_utils.py`：COMSOL CSV 读取、列名清洗、表面特征提取、归一化
- `model.py`：`LightPINN`（4 输出）
- `train.py`：训练并保存 `best_model.pt`、`train_log.csv`、`loss_curve.png`
- `evaluate.py`：测试集推理，输出指标/预测 CSV/图
- `plot_utils.py`：绘图

## 依赖安装
```bash
pip install -r requirements.txt
```

## 运行
```bash
cd /d E:\数值模拟\pinn_mvp
python train.py
python evaluate.py
```

## 输出
在 `E:\数值模拟\outputs\` 下生成：
- `best_model.pt`
- `train_log.csv`
- `loss_curve.png`
- `test_metrics.csv`
- `predictions/caseXX_prediction.csv`
- `figures/caseXX_scatter.png`
- `figures/caseXX_midplane.png`
