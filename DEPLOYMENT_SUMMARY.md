# 🚀 AI标注平台 - 免费部署摘要

## 快速部署步骤

### 1️⃣ 准备工作
```bash
./deploy.sh  # 运行部署准备脚本
```

### 2️⃣ 后端部署 (Render.com)
1. 推送代码到GitHub
2. 在Render.com创建Web Service
3. 配置设置：
   - **Root Directory**: `backend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. 添加环境变量：
   - `OPENAI_API_KEY`: 你的API密钥
   - `JWT_SECRET_KEY`: 随机密码
   - `JWT_ALGORITHM`: `HS256`

### 3️⃣ 前端部署 (Vercel.com)
1. 在Vercel导入GitHub仓库
2. 配置设置：
   - **Framework**: Vite
   - **Root Directory**: `frontend`
3. 添加环境变量：
   - `VITE_API_BASE_URL`: 你的Render后端URL

### 4️⃣ 更新CORS
在`backend/app/main.py`中添加你的Vercel域名到CORS配置

## 🔑 登录账户

| 用户名 | 密码 | 权限 |
|--------|------|------|
| admin  | admin123 | 管理员（可下载日志） |
| user1  | user123  | 普通用户 |
| user2  | user456  | 普通用户 |
| user3  | user789  | 普通用户 |
| demo   | demo123  | 演示用户 |

## 📊 访问日志数据

### 下载完整数据库
```
GET https://your-backend.onrender.com/download-logs
```
需要admin账户登录

### 查看统计摘要
```
GET https://your-backend.onrender.com/logs-summary
```
返回JSON格式的使用统计

## 💰 费用
- **完全免费** 使用Render和Vercel的免费层
- Render: 750小时/月，自动休眠
- Vercel: 100GB带宽/月，全球CDN

## 🔧 主要功能
- ✅ 用户认证和授权
- ✅ GPT-4和GPT-3.5模型选择
- ✅ 23个金融服务分类标签
- ✅ 并发控制（防止API超限）
- ✅ 用户反馈系统
- ✅ 完整的操作日志
- ✅ 管理员数据下载

## 📄 详细文档
- 完整部署指南: `DEPLOYMENT_GUIDE.md`
- 本地开发指南: `STARTUP_GUIDE.md`

部署完成后，你的AI标注平台将可以公开访问！🎉