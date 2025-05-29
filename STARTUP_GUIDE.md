# 🚀 AI Labeling Platform - 启动指南

## 项目概览

这是一个完整的AI文本分类平台，支持：
- 🔐 用户认证 (5个预定义账户)
- 🤖 AI模型选择 (GPT-4 / GPT-3.5-turbo)
- 📝 金融服务职位描述分类
- 🔒 并发控制 (单用户锁定机制)
- 📊 用户反馈收集
- 📈 完整的操作日志

## 🏃‍♂️ 快速启动

### 第一步：启动后端API

1. **打开终端1 - 启动后端**
   ```bash
   cd /Users/keyi/Desktop/AI-Labeling/backend
   
   # 激活虚拟环境
   source /Users/keyi/Library/Caches/pypoetry/virtualenvs/ai-labeling-ueEwKQCn-py3.12/bin/activate
   
   # 启动后端服务器
   python -m uvicorn app.main:app --reload --port 8000
   ```

2. **验证后端启动成功**
   - 看到以下信息表示成功：
   ```
   INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
   INFO:     Started server process [xxxx]
   INFO:     Application startup complete.
   ```

### 第二步：启动前端应用

1. **打开终端2 - 启动前端**
   ```bash
   cd /Users/keyi/Desktop/AI-Labeling/frontend
   
   # 启动前端开发服务器
   npm run dev
   ```

2. **验证前端启动成功**
   - 看到以下信息表示成功：
   ```
   VITE v4.5.14  ready in 137 ms
   ➜  Local:   http://localhost:3000/
   ➜  Network: use --host to expose
   ```

### 第三步：访问应用

1. **打开浏览器访问：** http://localhost:3000
2. **API文档访问：** http://127.0.0.1:8000/docs

## 🔑 测试账户

系统预配置了5个测试账户：

| 用户名 | 密码 | 说明 |
|--------|------|------|
| admin | admin123 | 管理员账户 |
| user1 | user123 | 普通用户1 |
| user2 | user456 | 普通用户2 |
| user3 | user789 | 普通用户3 |
| demo | demo123 | 演示账户 |

## 🧪 手动测试流程

### 1. 用户登录测试
- [ ] 使用正确账户登录成功
- [ ] 使用错误密码登录失败
- [ ] 登录后显示用户名

### 2. 模型选择测试
- [ ] 可以选择 GPT-4 模型
- [ ] 可以选择 GPT-3.5-turbo 模型
- [ ] 模型选择状态正确显示

### 3. 文本分类测试
使用以下测试文本：

```
MORGAN STANLEY
Executive Director – Finance Technology
Business Platforms Setup in Asia Markets
- Extensive experiences in setting up banking and broker dealer platforms in Asia markets
- Leading activities like market intelligence gathering, license acquisition, vendor platform selection,
business processes design, front to back integration and system implementation.
- Solid understanding in regulatory landscape in emerging markets
```

**测试步骤：**
- [ ] 输入测试文本
- [ ] 选择模型 (GPT-4 或 GPT-3.5-turbo)
- [ ] 点击 "Label Text" 按钮
- [ ] 等待处理完成 (显示loading状态)
- [ ] 查看分类结果

### 4. 并发控制测试
- [ ] 在一个浏览器窗口开始处理
- [ ] 在另一个浏览器窗口/账户尝试处理
- [ ] 第二个请求应显示 "系统忙碌" 消息

### 5. 反馈功能测试
处理完成后：
- [ ] 点击 "✓ Support" 支持结果
- [ ] 或点击 "✗ Don't Support" 不支持结果
- [ ] 如果不支持，选择正确的标签
- [ ] 提交反馈成功

### 6. 系统状态测试
- [ ] 查看系统状态显示 (忙碌/空闲)
- [ ] 处理时显示当前用户信息
- [ ] 处理时间统计正确

## 🔧 API直接测试

如果前端有问题，可以直接测试API：

### 1. 测试根端点
```bash
curl http://127.0.0.1:8000/
# 期望输出: {"message":"AI Labeling API is running","status":"healthy"}
```

### 2. 测试登录
```bash
curl -X POST http://127.0.0.1:8000/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'
```

### 3. 测试标签列表
```bash
curl http://127.0.0.1:8000/labels
```

### 4. 测试系统状态
```bash
curl http://127.0.0.1:8000/status
```

### 5. 测试文本分类 (需要JWT token)
```bash
# 先获取token
TOKEN=$(curl -s -X POST http://127.0.0.1:8000/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}' | \
  python3 -c "import sys, json; print(json.load(sys.stdin)['access_token'])")

# 使用token进行分类
curl -X POST http://127.0.0.1:8000/label \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "text": "Managing investment portfolios for high-net-worth clients",
    "model_name": "gpt-4"
  }'
```

## 🐛 故障排除

### 后端问题
- **端口8000被占用**：使用 `lsof -i :8000` 查看，或更改端口
- **依赖缺失**：重新运行 `pip install -r backend/requirements.txt`
- **虚拟环境**：确保激活了正确的虚拟环境

### 前端问题
- **端口3000被占用**：使用 `lsof -i :3000` 查看，或在vite.config.ts中更改端口
- **依赖缺失**：重新运行 `npm install`
- **无法连接后端**：检查后端是否在8000端口运行

### OpenAI API问题
- **API密钥无效**：检查 `backend/.env` 文件中的 `OPENAI_API_KEY`
- **配额超限**：检查OpenAI账户余额和使用限制

## 📝 日志查看

### 后端日志
- 在启动后端的终端窗口中查看实时日志
- 数据库日志存储在 `backend/logs.db`

### 前端日志
- 在浏览器开发者工具的Console中查看
- 网络请求在Network标签中查看

## 🎯 测试检查清单

- [ ] 后端API启动成功
- [ ] 前端应用启动成功
- [ ] 用户可以成功登录
- [ ] 模型选择功能正常
- [ ] 文本分类功能正常
- [ ] 并发控制机制生效
- [ ] 用户反馈功能正常
- [ ] 系统状态显示正确
- [ ] 日志记录完整

## 🚀 部署准备

完成本地测试后，可以参考以下部署选项：
- **后端**: Render.com (免费tier)
- **前端**: Vercel (免费tier)
- **数据库**: SQLite (已配置) 