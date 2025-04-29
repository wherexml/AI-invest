# 股市投资提醒系统

一个基于 AKshare 的 Web 投资提醒软件，针对港股和 A 股市场。

## 功能特点

- 支持 A 股和港股市场
- 实时股票数据更新
- 自定义价格、涨跌幅等提醒设置
- 股票历史数据图表显示
- 自动监控股票价格变化

## 技术栈

- 后端：Flask
- 数据库：PostgreSQL (需要云数据库服务, 如 Vercel Postgres, Neon)
- 前端：Bootstrap 5 + jQuery
- 数据源：AKshare
- 任务调度：Vercel Cron Jobs

## Vercel 部署

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2F<你的GitHub用户名>%2F<你的仓库名>&env=DATABASE_URL,CRON_SECRET&envDescription=需要设置数据库连接URL和Cron安全密钥&project-name=ai-investment-reminder&repository-name=ai-investment-reminder&demo-title=AI%20Investment%20Reminder&demo-description=A%20Flask%20app%20for%20stock%20alerts.&demo-url=YOUR_DEPLOYED_URL_HERE&integration-ids=oac_VercelPostgres)

**点击上方按钮一键部署到您的 Vercel 账户。**

**部署前准备:**

1.  **GitHub 仓库:** 确保您的代码已推送到 GitHub 仓库。
2.  **云数据库:** 您需要一个 PostgreSQL 数据库。推荐使用 Vercel Postgres：
    *   在 Vercel 项目创建过程中或之后，可以通过 Vercel 控制台的 "Storage" 选项卡添加 Vercel Postgres 数据库。Vercel 会自动为您设置 `DATABASE_URL` 环境变量。
    *   如果您使用其他云数据库 (如 Neon, Supabase)，请获取其连接字符串 (通常以 `postgresql://...` 开头)。
3.  **Cron Secret:** 生成一个强随机字符串作为 Cron 作业的安全密钥。这个密钥将用于验证来自 Vercel Cron 的请求。

**部署步骤:**

1.  点击上方的 "Deploy with Vercel" 按钮。
2.  使用您的 GitHub 账户授权 Vercel。
3.  Vercel 会提示您克隆仓库并创建一个新项目。
4.  **配置环境变量:**
    *   **`DATABASE_URL`:** 如果您在 Vercel 中创建了 Postgres 数据库，它通常会自动填充。如果使用外部数据库，请粘贴您的 PostgreSQL 连接字符串。
    *   **`CRON_SECRET`:** 粘贴您生成的强随机字符串。
    *   *(可选)* `SECRET_KEY`: 如果您的 Flask 应用使用了会话，可以设置一个 Flask 的 `SECRET_KEY`。
5.  点击 "Deploy"。
6.  Vercel 将开始构建和部署您的应用。
7.  部署成功后，Vercel 会提供一个 URL 访问您的应用。

**数据库初始化:**
首次部署后，数据库表可能需要手动创建。您可以通过以下方式之一完成：
*   **本地连接:** 使用数据库管理工具 (如 `psql`, DBeaver, TablePlus) 连接到您的云数据库，然后手动执行 SQL `CREATE TABLE` 语句 (您可以从 Flask-SQLAlchemy 模型生成或手动编写)。
*   **Flask Shell (临时):** 如果 Vercel 部署允许临时访问 shell (通常不直接提供)，或者您可以在本地连接到云数据库并运行 Flask shell：
    ```bash
    # 本地设置好 DATABASE_URL 环境变量
    flask shell
    >>> from app import db
    >>> db.create_all()
    >>> exit()
    ```

## 使用指南

### 添加股票

1. 点击"股票列表"菜单
2. 在搜索栏输入股票代码或名称
3. 选择市场类型（A股或港股）
4. 点击"搜索"按钮
5. 在搜索结果中点击"添加"按钮

### 设置提醒

1. 进入股票详情页
2. 在"设置提醒"卡片中选择提醒类型、条件和数值
3. 点击"添加提醒"按钮
4. 提醒将在满足条件时自动触发

### 管理提醒

1. 点击"提醒列表"菜单查看所有提醒
2. 可以启用/禁用、重置或删除提醒

## 数据源说明

本系统使用 AKshare 作为数据源，获取 A 股和港股的实时行情和历史数据。详情请参考 [AKshare 文档](https://akshare.akfamily.xyz)。

## 许可证

MIT 