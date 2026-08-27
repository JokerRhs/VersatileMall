# CLI 一键初始化超级管理员文档（V0\.3）

## 1\. 功能概述

为避免手动编写 SQL 初始化商家、超级管理员账号带来的语法错误、哈希不匹配、数据不一致等问题，项目内置 CLI 命令行初始化脚本。

脚本完全复用项目现有核心能力：数据库会话、bcrypt 密码加密、模型定义，支持**幂等执行**，可安全重复运行，是开发、测试、部署环境统一初始化管理员账号的标准方案。

**脚本路径**：`src/cli/create_super_admin.py`

## 2\. 前置依赖与条件

### 2\.1 依赖安装

CLI 基于 typer 实现命令行交互，需安装依赖：

```bash
pip install typer
```

### 2\.2 环境前置条件

- PostgreSQL 数据库服务正常启动，\.env 数据库配置正确

- 已执行完整数据库迁移：`alembic upgrade head`，`merchant`、`merchant_admin` 数据表已存在

- Redis 服务正常启动（不影响初始化脚本执行，仅影响业务登录鉴权）

- 执行命令需配置正确 `PYTHONPATH=src`，保证项目模块正常导入

## 3\. 脚本核心特性

- **幂等设计**：重复执行不会重复创建数据，已存在的商家、管理员会自动跳过

- **安全加密**：自动调用项目统一密码加密工具，兼容 bcrypt 72 字节长度限制，自动截断超长密码

- **事务保障**：数据库操作开启事务，异常自动回滚，避免脏数据

- **统一规范**：完全复用业务模型、数据库会话，与线上接口数据一致性一致

- **自定义参数**：支持自定义商家信息、管理员账号、密码、昵称

## 4\. 命令使用说明

### 4\.1 基础默认执行（快速初始化）

使用默认参数创建默认商家 \+ 超级管理员账号：

```bash
export PYTHONPATH=src
python src/cli/create_super_admin.py
```

**默认参数**：

- 商家编码：M001

- 商家名称：默认主商家

- 管理员账号：superadmin

- 管理员密码：123456

- 管理员昵称：超级管理员

### 4\.2 自定义参数执行

支持自定义全部参数，适配多环境、多商家初始化场景：

```bash
export PYTHONPATH=src
python src/cli/create_super_admin.py \
--merchant-code M002 \
--merchant-name "测试合作商家" \
--admin-username shop_admin \
--admin-password "Abc@123456" \
--admin-nickname "商家运营管理员"
```

### 4\.3 查看帮助文档

```bash
export PYTHONPATH=src
python src/cli/create_super_admin.py --help
```

## 5\. 可配置参数详解

|参数名|作用|默认值|备注|
|---|---|---|---|
|merchant\-code|商家唯一编码|M001|全局唯一，不可重复|
|merchant\-name|商家名称|默认主商家|自定义企业/店铺名称|
|admin\-username|管理员登录账号|superadmin|账号唯一，3\-32位字符|
|admin\-password|管理员登录密码|123456|自动兼容bcrypt72字节限制，建议6\-64位|
|admin\-nickname|管理员昵称|超级管理员|可选自定义|

## 6\. 执行成功示例输出

```text
✅ 创建商家成功 id=1 code=M001
✅ 超级管理员创建完成！
   商家ID: 1
   账号: superadmin
   密码: 123456
```

## 7\. 异常处理机制

- **数据已存在**：检测到商家/管理员已存在，静默跳过创建，无报错

- **数据库异常**：自动事务回滚，保证数据一致性，打印错误信息

- **密码超长异常**：内置72字节自动截断，彻底规避bcrypt长度报错

## 10\. 常见踩坑与解决方案

- **报错：unexpected extra argument\(s\) \(create\)**
原因：当前脚本为 Typer 单命令模式，无需携带 `create` 子命令
解决方案：执行命令去掉 `create`，直接运行脚本即可

- **报错：int object has no attribute 'id'**
原因：使用 `模型.__table__.select()` 查询仅返回主键数字，非 ORM 实例
解决方案：统一使用 `select(模型)` 标准 ORM 查询，获取完整模型对象取值

- **数据库字段非空约束报错**
原因：新增 `is_super` 布尔字段且设置非空，存量数据为 NULL
解决方案：修改 alembic 迁移脚本，先加可空字段、批量赋值默认值，再设置非空约束

- **模块导入失败 ModuleNotFoundError**
原因：未配置 `PYTHONPATH=src`，项目模块无法识别
解决方案：执行脚本前必须配置环境变量，保证项目根目录模块可导入

- **状态字段类型不匹配报错**
原因：数据库字段为布尔类型，传入字符串状态值（normal/disabled）
解决方案：商户状态、管理员状态字段统一使用字符串类型，搭配枚举管理状态

## 11\. 对接业务接口

初始化完成后，可直接使用创建的管理员账号密码，调用登录接口获取 JWT 令牌：

接口地址：`POST /api/v1/admin/auth/login`

登录成功后可正常访问所有需租户鉴权、管理员鉴权的业务接口。

> （注：部分内容可能由 AI 生成）
