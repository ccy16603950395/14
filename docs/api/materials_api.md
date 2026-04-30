# Materials API
## 模块功能
定义 concrete / interface / rock 的参数结构。
## 主要函数或类
- `MaterialProperties`
- `default_materials()`
## 输入参数
- 材料扩散、退化、模量、强度及损伤耦合系数。
## 返回值
- 默认材料字典 `dict[str, MaterialProperties]`。
## 简单示例
```python
mats = default_materials()
print(mats['interface'].degradation_rate)
```
## 后续扩展说明
可替换为数据库读取或实验标定参数。
