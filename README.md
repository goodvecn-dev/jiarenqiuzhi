# Job Auto Apply Agent (Playwright + A2A-ready)

一个可扩展的自动化求职系统：

- 根据候选人工作经历自动提取技能并匹配岗位。
- 基于 Playwright 实现跨平台浏览器自动化（Boss 直聘、智联招聘）。
- 统一关键问答引擎，自动回答常见投递问题。
- 预留 A2A（Agent-to-Agent）接口，便于与其他 Agent 系统协作。

> ⚠️ 默认示例使用“干跑模式（dry-run）”，不会真实投递；你需要自行填写账号、简历、关键词与风控策略。

## 快速开始

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m playwright install chromium
python -m job_bot.cli run --config config.example.yaml --dry-run
```

## 目录结构

- `src/job_bot/models.py`: 核心数据模型。
- `src/job_bot/matcher.py`: 工作经历与岗位匹配逻辑。
- `src/job_bot/qa.py`: 关键问答引擎（平台问题自动回答）。
- `src/job_bot/platforms/`: 平台适配器。
  - `boss.py`: Boss 直聘适配器示例。
  - `zhilian.py`: 智联招聘适配器示例。
- `src/job_bot/engine.py`: 统一调度引擎。
- `src/job_bot/a2a.py`: A2A 协议消息封装（JSON over stdin/stdout）。

## 配置

见 `config.example.yaml`：

- 候选人信息、工作经历、技能。
- 平台账号配置。
- 匹配阈值。
- 自动问答规则。

## 合规与风险控制

请务必遵守各平台服务条款与当地法律法规。建议：

- 限速、随机等待，避免高频请求。
- 保留人工确认开关。
- 仅对明确授权岗位执行投递。

