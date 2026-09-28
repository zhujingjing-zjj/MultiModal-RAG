# GaosuProject / Myproject

本项目提出一种基于相似案例检索增强的风险隐患检测识别方法，通过提示微调技术动态融合外部知识库与检索 案例上下文，设计有效的图片检索策略，缓解现有多模态大模型因领域知识缺失与特征关联弱化导致的误判问题：以隐患图片为输入，调用不同多模态大模型（如 ChatGPT-4V / DeepSeek / GLM-4V 等）在检索增强框架下生成隐患类别、隐患描述与整改建议，并提供结果清洗、统计与相似度评估的辅助脚本。

> 说明：项目脚本已尽量使用**相对路径**并通过**环境变量/.env**读取 API Key；若你的数据文件中仍残留绝对路径，可按下文说明一键规范化。

## 目录结构（关键）

- `dataset/`
  - `data_check.json`：样本库（键为 `"1".."325"`），字段包含：`图片地址` / `隐患描述` / `隐患类别`
  - `隐患描述文档.txt`：用于生成标准答案/样本库的文本来源
  - 其他：若干模型输出与中间结果 JSON
- `*_output/`：各模型运行后输出（按 `prompt_type`、`result_num` 等分目录）
- `result/`：部分后处理脚本写入的结果目录（若不存在请先创建）

图片文件夹不随仓库提供时，你需要自行准备，例如：

- `dataset/隐患图片/`（示例）或任意目录，然后在运行时传入 `--image_dir`

## 环境准备

建议使用 Python 3.9+（Windows/Linux 均可）。

创建虚拟环境并安装依赖：

```bash
python -m venv .venv
.venv\\Scripts\\activate

pip install -U pip
pip install -r requirements.txt
```


## 配置（API Key）

推荐在项目根目录新建 `.env`（或直接设置系统环境变量）：

```ini
OPENAI_API_KEY=...
DEEPSEEK_API_KEY=...
ZHIPU_API_KEY=...
CLIP_MODEL_PATH=./CLIP
```

各脚本会通过 `python-dotenv` 自动加载 `.env`。

## 数据准备

### 1) 样本库 `data_check.json`

脚本普遍会读取 `data_check.json`（根目录或 `dataset/` 下均存在一份）。推荐把 `图片地址` 规范为**图片文件名**（如 `1-1.jpg`），脚本会在运行时自动与 `--image_dir` 拼接。

如你的 `data_check.json`/`dataset/data_check.json`/`dataset/data_test.json` 中仍有绝对路径，可运行一次（会改写上述数据文件）：

```bash
python .\\scripts\\normalize_repo_paths.py
```

如果你有“图片名:描述”的文本文件，可用 `data_check.py` 生成样本库（默认读取 `./dataset/隐患描述文档.txt`，以及 `--image_dir` 指向的图片目录）。

### 2) 标准答案 `Standard_output.json`

`data2.py` 会从 `dataset/隐患描述文档.txt` 生成 `dataset/Standard_output.json`。

## 运行：调用不同模型生成输出

下面给出常见脚本的运行方式（所有脚本都支持 `-h/--help` 查看参数）。

### ChatGPT-4（图片→文本）

脚本：`chatgpt4.py`  
输出：默认写入 `gpt4_output/`

```bash
python chatgpt4.py --image_dir "<你的图片目录>" --data_check_path ".\\data_check.json" --prompt_type type_1 --result_num 1
```

### DeepSeek（OpenAI SDK 方式调用）

脚本：`Deepseek.py`  
输出：默认写入 `deepseek_output/`

```bash
python Deepseek.py --image_dir "<你的图片目录>" --data_check_path ".\\data_check.json" --prompt_type type_5 --result_num 1
```

### GLM-4V（智谱 API）

脚本：`glm-4v.py`  
输出：默认写入 `glm4_output/`

```bash
python "glm-4v.py" --image_dir "<你的图片目录>" --data_check_path ".\\data_check.json" --prompt_type type_3 --result_num 1
```

## 后处理与评估（可选）

- `data.py`：从某个模型输出目录读取 `.txt`，抽取字段并写入 JSON。
- `data3.py` / `data4.py`：对比标准答案与模型输出，生成结果文本。
- `Class_accuracy.py` / `Class_accuracy_class.py`：读取 JSON 做分类准确率统计。
- `image_similarity.py`：使用本地 CLIP 模型算图像相似度（通过 `CLIP_MODEL_PATH` 指定模型目录）。
- `data_BERT.py`：使用本地 `bert-base-uncased`（仓库内有 `bert-base-uncased/`）对文本做相似度/聚合分析。

## 安全与配置建议

- 不要把 API Key 写在代码里；统一放在环境变量或 `.env`。
- 尽量使用相对路径（建议统一以仓库根目录为基准），把输入/输出目录都暴露为命令行参数。
