# NOTICE — 版权与来源说明

本仓库是 [ykqiu/Image-Processing](https://github.com/ykqiu/image-processing) 的 **fork（二次开发）**，
GitHub 页面会显示 "forked from ykqiu/Image-Processing"。

## 原始内容（版权归原作者 ykqiu）

- `image_processing/`、`image_processing_top/`、`sdram_controller/`、`vga_controller/`、`ISP_testbench/`
- `docs/` 下的文档插图
- `README.md` 的原始英文说明（「项目来源 / Provenance」与「Simulation & Verification」章节除外）

上游仓库**未声明开源许可证**（无 LICENSE 文件），按默认规则保留所有权利。
本仓库不对上述原始内容主张任何权利，也不对其再许可；商用或再分发原始 RTL 前请先联系原作者取得授权。

## 本二次开发新增 / 修改的内容

- `sim/` —— 周期精确仿真验证体系（原创代码）
- `docs/HANDOFF.md` —— 验证交接文档
- `README.md` 的「项目来源 / Provenance」与「Simulation & Verification」章节
- 对上游 RTL 的 bug 修复（修复部分版权归本仓库作者；被修改文件的原始代码仍归 ykqiu）：
  - `RGB2YUV.v`：RGB565 → RGB888 标准高位复制
  - `canny.v`：`canny_in` 端口方向、缺失的 `2'b01` phase 分支
  - `matrix_generator.v`：VGA 低有效同步信号的沿检测
  - `sram_ctrl.v`：写数据与 WRITE 命令对齐

## 独立开源的验证套件

`sim/` 中的验证代码另以 **MIT** 许可证发布于独立仓库：

**https://github.com/lowfreq-quant/isp-verification**

该仓库只包含验证代码（不含 RTL），可通过 `RTL_ROOT` 环境变量配合上游 RTL 或本仓库运行。
