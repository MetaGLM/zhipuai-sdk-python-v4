## Release Notes

### 2024-08-12

**New Features:**
- Modified video prompt to be optional, added file deletion functionality
- Added Assistant business logic
- Fixed embedding 3 dimensions

### 2024-07-25

**Bug Fixes:**
- Fixed cogvideo related issues

### 2024-07-12

**New Features:**
- Added advanced search tool Web search business logic
- Specified Python versions support (3.8, 3.9, 3.10, 3.11, 3.12)
- Integrated cogvideo business functionality

### 2024-05-20

**Improvements:**
- Fixed some `python3.12` dependency issues
- Added pagination processing code, rewrote instantiation rules for some response classes
- Added type conversion validation
- Added batch task related APIs
- Added file stream response wrapper

### 2024-04-29

**Improvements:**
- Fixed some `python3.7` code compatibility issues
- Added interface failure retry mechanism, controlled by `retry` parameter with default of 3 retries
- Adjusted interface timeout strategy, controlled by `Timeout` for interface `connect` and `read` timeout, default `timeout=300.0, connect=8.0`
- Added support for super-humanoid large model parameters in conversation module, `model="charglm-3"`, `meta` parameter support

### 2024-04-23

**Improvements:**
- Fixed some compatibility issues with `pydantic<3,>=1.9.0`
- Message processing business request and response parameters can be extended through configuration
- Compatible with some parameters `top_p:1`, `temperature:0` (do_sample rewritten to false, parameters top_p temperature do not take effect)
- Image understanding part, image_url parameter base64 content containing `data:image/jpeg;base64` compatibility
- Removed JWT authentication logic

---

## Migration Guide

For users upgrading from older versions, please note the following breaking changes:

### From v3.x to v4.x

- API key configuration has been simplified
- Some method signatures have changed for better type safety
- Error handling has been improved with more specific exception types

## Support

For questions about specific versions or upgrade assistance, please visit our [documentation](https://open.bigmodel.cn/) or contact our support team.

---

## 版本更新

### 2024-08-12

**新功能：**
- ✅ 视频提示词设为可选，新增文件删除功能
- ✅ 智能助手业务逻辑
- 🔧 修复 embedding 3 维度问题

### 2024-07-25

**问题修复：**
- 🔧 修复 cogvideo 相关问题

### 2024-07-12

**新功能：**
- ✅ 高级搜索工具 Web search 业务逻辑
- ✅ 指定 Python 版本支持 (3.8, 3.9, 3.10, 3.11, 3.12)
- ✅ 集成 cogvideo 业务功能

### 2024-05-20

**改进优化：**
- 🔧 修复部分 `python3.12` 依赖问题
- ✅ 新增分页处理代码，重写部分响应类实例化规则
- ✅ 新增类型转换校验
- ✅ 批处理任务相关 API
- ✅ 文件流响应包装器

### 2024-04-29

**改进优化：**
- 🔧 修复部分 `python3.7` 代码兼容性问题
- ✅ 接口失败重试机制，通过 `retry` 参数控制重试次数，默认 3 次
- ⏱️ 调整接口超时策略，通过 `Timeout` 控制接口 `connect` 和 `read` 超时时间，默认 `timeout=300.0, connect=8.0`
- ✅ 对话模块新增超拟人大模型参数支持，`model="charglm-3"`，`meta` 参数支持

### 2024-04-23

**改进优化：**
- 🔧 修复部分 `pydantic<3,>=1.9.0` 兼容性问题
- ✅ 报文处理的业务请求参数和响应参数可通过配置扩充
- ✅ 兼容部分参数 `top_p:1`，`temperature:0`（do_sample 重写为 false，参数 top_p temperature 不生效）
- ✅ 图像理解部分，image_url 参数 base64 内容包含 `data:image/jpeg;base64` 兼容性
- 🔄 删除 JWT 认证逻辑

---

## 迁移指南

对于从旧版本升级的用户，请注意以下重大变更：

### 从 v3.x 到 v4.x

- API 密钥配置已简化
- 部分方法签名已更改以提供更好的类型安全性
- 错误处理已改进，提供更具体的异常类型

## 技术支持

如有特定版本问题或升级协助需求，请访问我们的[文档](https://open.bigmodel.cn/)或联系我们的支持团队。