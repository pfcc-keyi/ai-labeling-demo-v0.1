# AI Labeling Platform - 免费部署指南

这个指南将帮助你将AI标注平台免费部署到云端，让其他人可以公开访问。

## 部署架构

- **后端**: Render.com (免费层)
- **前端**: Vercel (免费层)
- **数据库**: SQLite (内置在后端服务中)
- **日志访问**: 通过API端点下载

## 第一步：部署后端到Render.com

### 1.1 准备代码仓库

首先，你需要将代码推送到GitHub仓库：

```bash
cd /Users/keyi/Desktop/AI-Labeling
git init
git add .
git commit -m "Initial commit - AI Labeling Platform"
# 创建GitHub仓库并推送
git remote add origin YOUR_GITHUB_REPO_URL
git push -u origin main
```

### 1.2 在Render.com创建账户并部署

1. 访问 [Render.com](https://render.com) 并注册账户
2. 点击 "New +" → "Web Service"
3. 连接你的GitHub仓库
4. 选择 `AI-Labeling` 仓库
5. 配置部署设置：

**基础设置:**
- **Name**: `ai-labeling-backend`
- **Region**: 选择距离用户最近的地区
- **Branch**: `main`
- **Root Directory**: `backend`
- **Runtime**: `Python 3`

**构建和部署命令:**
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

**环境变量:**
添加以下环境变量：
- `OPENAI_API_KEY`: 你的OpenAI API密钥
- `JWT_SECRET_KEY`: 任意强密码（自动生成）
- `JWT_ALGORITHM`: `HS256`
- `ACCESS_TOKEN_EXPIRE_MINUTES`: `30`

6. 点击 "Create Web Service"

### 1.3 获取后端URL

部署完成后，你会得到一个类似这样的URL：
`https://ai-labeling-backend.onrender.com`

记录这个URL，前端部署时需要用到。

## 第二步：部署前端到Vercel

### 2.1 在Vercel创建账户并部署

1. 访问 [Vercel.com](https://vercel.com) 并注册账户
2. 点击 "New Project"
3. 导入你的GitHub仓库 `AI-Labeling`
4. 配置项目设置：

**框架预设:** Vite

**根目录:** `frontend`

**构建命令:** `npm run build`

**输出目录:** `dist`

**安装命令:** `npm install`

### 2.2 配置环境变量

在Vercel项目设置中添加环境变量：
- **Name**: `VITE_API_BASE_URL`
- **Value**: 你的Render后端URL（如：`https://ai-labeling-backend.onrender.com`）

### 2.3 部署

点击 "Deploy" 开始部署。

部署完成后，你会得到一个类似这样的URL：
`https://your-app-name.vercel.app`

## 第三步：更新CORS设置

部署完成后，需要更新后端的CORS设置以允许你的Vercel域名：

1. 编辑 `backend/app/main.py` 文件
2. 在CORS配置中添加你的Vercel URL：

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000", 
        "http://localhost:5173",
        "https://your-app-name.vercel.app",  # 添加你的Vercel URL
        "https://*.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

3. 提交并推送更改，Render会自动重新部署

## 第四步：访问日志数据

你可以通过以下方式访问数据库日志：

### 4.1 下载完整数据库文件

使用admin账户登录后，访问：
```
https://ai-labeling-backend.onrender.com/download-logs
```

这会下载完整的SQLite数据库文件。

### 4.2 查看日志摘要

访问：
```
https://ai-labeling-backend.onrender.com/logs-summary
```

这会返回JSON格式的统计数据：
- 总请求数
- 总反馈数
- 各账户的使用统计

### 4.3 使用SQLite工具查看数据

下载的数据库文件可以用以下工具打开：
- [DB Browser for SQLite](https://sqlitebrowser.org/) (免费)
- [DBeaver](https://dbeaver.io/) (免费)
- 命令行: `sqlite3 ai_labeling_logs.db`

## 第五步：账户信息

部署完成后，用户可以使用以下账户登录：

| 用户名 | 密码 | 角色 |
|--------|------|------|
| admin  | admin123 | 管理员（可下载日志） |
| user1  | user123  | 普通用户 |
| user2  | user456  | 普通用户 |
| user3  | user789  | 普通用户 |
| demo   | demo123  | 演示用户 |

## 费用说明

### Render.com 免费层限制：
- 750小时/月的运行时间
- 512MB RAM
- 自动休眠（无活动15分钟后）
- 100GB带宽/月

### Vercel 免费层限制：
- 100GB带宽/月
- 无限制的个人项目
- 自动HTTPS
- 全球CDN

## 监控和维护

1. **服务健康检查**: 访问 `https://your-backend.onrender.com/` 查看API状态
2. **前端状态**: 定期访问你的Vercel URL确保服务正常
3. **日志监控**: 定期下载数据库文件备份数据
4. **更新部署**: 推送代码到GitHub会自动触发重新部署

## 故障排除

### 常见问题：

1. **后端服务休眠**: Render免费层会在15分钟无活动后休眠，首次访问可能需要30秒启动
2. **CORS错误**: 确保后端CORS设置包含了你的前端域名
3. **API密钥错误**: 检查Render环境变量中的OpenAI API Key是否正确设置
4. **数据库丢失**: Render免费层重新部署时可能丢失数据，定期备份很重要

### 联系支持：

如果遇到部署问题，可以：
1. 检查Render和Vercel的部署日志
2. 确认环境变量设置正确
3. 验证API密钥有效性

## 下一步

部署完成后，你可以：
1. 分享你的Vercel URL给其他用户
2. 定期备份数据库
3. 监控使用情况
4. 根据需要升级到付费计划

你的AI标注平台现在可以公开访问了！🎉