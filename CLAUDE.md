# 3D 手势粒子系统 (Gesture Particle System)

## 项目概述
通过摄像头实时识别手势来控制 3D 粒子分布和动画。纯前端单文件实现，浏览器直开即用。

## 技术栈
- **Three.js** (CDN: bootcdn, 版本 0.160) — 3D 渲染
- **MediaPipe Hands** (本地 node_modules, 版本 0.4.1675469240) — 手部 21 关键点检测
- 单文件 `index.html`，无需构建工具

## 访问方式
```
cd /c/Users/admin/my-project
python3 -m http.server 8080
# 访问: http://localhost:8080/index.html
```
⚠️ 必须通过 localhost 访问（摄像头需要安全上下文）

## 环境依赖
- **Node.js** 需安装（项目依赖 `@mediapipe/hands` 和 `@mediapipe/camera_utils`）
- 首次使用或 `node_modules` 缺失时运行：`npm install`
- 所有 MediaPipe 文件（JS/WASM/TFLite）从本地 node_modules 加载，不依赖 CDN

## 运行模式
| 模式 | 操作 | 说明 |
|------|------|------|
| 🖱 鼠标模式 | 默认 | 移动=位置, 左键=扩散, 右键=收缩, 滚轮=深度 |
| 📷 手势模式 | 点右下角按钮或按 `2` | 摄像头手势识别 |
| ⌨ 快捷键 | 方向键, A, F, 1, 2 | 键盘操控 |

## 手势 → 粒子映射
| 手势 | 粒子效果 |
|------|---------|
| 张开手掌 (≥3指) | 粒子球膨胀扩散 |
| 握拳 (≤1指) | 粒子收缩聚集 |
| 食指指向 | 粒子沿方向流动 |
| 捏合 (拇+食) | 粒子形成环状涡旋 |
| 手掌旋转 | 粒子云旋转 |
| 手掌移动 | 粒子云跟随 |
| 双手 | 双中心分布 |

## 已知问题
- **摄像头镜像**：X 轴已翻转处理 (`0.5 - lm[WRIST].x`)
- **MediaPipe 全本地化**：JS 脚本、WASM、模型文件均从 `node_modules/` 加载，不再依赖 unpkg CDN
- **手指检测**：用 `指尖到手腕距离 vs 指节到手腕距离` 判断伸展，阈值 1.05
- **模型复杂度**：modelComplexity=1（设 2 可能导致页面卡顿）
- **Three.js** 仍从 bootcdn CDN 加载（国内可访问），fallback 到 unpkg

## 关键参数（调优参考）
- 手指伸展阈值：1.05 (`tipToWrist > pipToWrist * 1.05`)
- 张开判定：`totalFingers >= 3 && openness > 0.3`
- 握拳判定：`totalFingers <= 1 && openness < 0.2`
- 捏合判定：`pinchDist < 0.08`
- 平滑因子：`alpha = 1 - exp(-dt * 12)`
- 粒子数：3000
- 粒子跟随速度：`1 - exp(-dt * 10)`
