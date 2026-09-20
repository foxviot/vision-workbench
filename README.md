# Vision Workbench

> 本地图片边缘与区域分析工具

![Stage](https://img.shields.io/badge/stage-runnable_demo-10b981?style=flat-square)
![License](https://img.shields.io/badge/license-MIT-0ea5e9?style=flat-square)

![Annotated demo](examples/output/annotated.png)

## What runs today

OpenCV Canny、轮廓提取、区域框选；导出输入、边缘图、标注图及 JSON。默认生成三个几何形状作为可复现样例。不是 YOLO 语义检测器，尚无追踪与 ONNX 功能。

## Quick start

```bash
git clone https://github.com/foxviot/vision-workbench.git
cd vision-workbench
python -m pip install -r requirements.txt
python analyze.py
```

## Custom input

```text
python analyze.py --input your-image.jpg --output output
```

## Results and limits

样例输出来自实际运行。速度随硬件与依赖版本变化；示例结果不代表生产环境性能。默认运行不需要 API Key、GPU 或云服务。

## Attribution

[OpenCV Canny tutorial](https://docs.opencv.org/4.x/da/d22/tutorial_py_canny.html)；复用 opencv-python 的算法实现，应用编排代码为本仓库新增。OpenCV 4.5+ 使用 Apache-2.0；NumPy 使用 BSD-3-Clause。

本仓库新增代码采用 [MIT](LICENSE)，依赖库和数据保持各自许可证。本项目不代表上游官方项目。
