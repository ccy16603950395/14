# Visualization API
## 模块功能
输出浓度、退化、损伤、弹性模量云图和平均指标曲线。
## 主要函数或类
- `plot_concentration`
- `plot_degradation`
- `plot_damage`
- `plot_elastic_modulus`
- `plot_average_curves`
## 输入参数
- 场数据 `ndarray` 与输出路径 `Path`。
## 返回值
- 保存 PNG 图像文件到 `outputs/`。
## 简单示例
```python
plot_concentration(C, Path('outputs/concentration_final.png'))
```
## 后续扩展说明
可增加动画、对比图和批处理绘图接口。
