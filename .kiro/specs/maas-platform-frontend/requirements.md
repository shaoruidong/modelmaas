# Requirements Document

## Introduction

本项目为企业级大模型MaaS（Model as a Service）平台前端，参考阿里云百炼平台、华为云ModelArts等产品设计风格，具备科技感UI，支持模型管理、微调训练、数据管理、API管理、应用开发等核心功能模块。前端使用 Vue 3 + TypeScript 构建，采用暗色科技风格设计，登录阶段使用本地固定账号（admin/admin），后续可接入后端数据库。

## Glossary

- **MaaS Platform**: Model as a Service 平台，提供大模型的托管、调用、微调等服务
- **Model Marketplace (模型广场)**: 展示可用大模型列表的页面，支持筛选和搜索
- **Fine-tuning (模型微调)**: 基于预训练模型，使用自定义数据集进行二次训练的过程
- **API Key**: 用于鉴权的访问密钥，供外部应用调用模型接口
- **Inference (推理)**: 使用已部署模型对输入数据进行预测的过程
- **Dataset (数据集)**: 用于模型训练或评估的结构化数据集合
- **Training Job (训练任务)**: 一次完整的模型微调或训练执行过程
- **Deployment (模型部署)**: 将训练好的模型发布为可调用服务的操作
- **Dashboard (控制台)**: 平台主页，展示核心指标和快捷入口
- **System**: 指本MaaS平台前端应用
- **User**: 已登录的平台使用者
- **Admin**: 具有管理员权限的用户角色

---

## Requirements

### Requirement 1: 用户登录与认证

**User Story:** As a user, I want to log in to the MaaS platform with my credentials, so that I can securely access platform features.

#### Acceptance Criteria

1. WHEN a user visits the platform root URL, THE System SHALL redirect the user to the login page if no valid session exists
2. WHEN a user enters username "admin" and password "admin" and submits the login form, THE System SHALL authenticate the user and redirect to the Dashboard
3. WHEN a user enters incorrect credentials and submits the login form, THE System SHALL display an error message and keep the user on the login page
4. WHEN a user attempts to access any protected route without authentication, THE System SHALL redirect the user to the login page
5. WHEN a logged-in user clicks the logout button, THE System SHALL clear the session and redirect the user to the login page

---

### Requirement 2: 控制台主页（Dashboard）

**User Story:** As a user, I want to see a dashboard with key metrics and quick-access tools after login, so that I can get an overview of my platform usage and navigate quickly.

#### Acceptance Criteria

1. WHEN a user successfully logs in, THE System SHALL display the Dashboard page with a navigation sidebar and top header
2. WHEN the Dashboard loads, THE System SHALL display core metric cards including: total models count, active training jobs count, API call count, and dataset count
3. WHEN the Dashboard loads, THE System SHALL display a "一站式工具链" section with three entry cards: 选模型、改模型、用模型
4. WHEN the Dashboard loads, THE System SHALL display a recent activity or announcement section
5. WHILE the user is on any page, THE System SHALL display a persistent left sidebar with all main navigation categories

---

### Requirement 3: 模型广场（Model Marketplace）

**User Story:** As a user, I want to browse and search available models in the model marketplace, so that I can find the right model for my use case.

#### Acceptance Criteria

1. WHEN a user navigates to the Model Marketplace, THE System SHALL display a list of available models with name, description, category, and capability tags
2. WHEN a user enters a keyword in the search input, THE System SHALL filter and display only models whose name or description matches the keyword
3. WHEN a user selects a category filter, THE System SHALL display only models belonging to that category
4. WHEN a user clicks on a model card, THE System SHALL navigate to the model detail page showing full specifications
5. WHEN the model list is loading, THE System SHALL display skeleton loading placeholders in place of model cards

---

### Requirement 4: 模型微调（Fine-tuning）

**User Story:** As a user, I want to create and manage model fine-tuning jobs, so that I can customize pre-trained models with my own data.

#### Acceptance Criteria

1. WHEN a user navigates to the Fine-tuning page, THE System SHALL display a list of existing training jobs with status, creation time, and base model name
2. WHEN a user clicks "新建微调任务", THE System SHALL display a multi-step form wizard for configuring a new fine-tuning job
3. WHEN a user completes the fine-tuning configuration form and submits, THE System SHALL validate all required fields and add the new job to the training job list with "待运行" status
4. IF a required field in the fine-tuning form is empty when the user submits, THEN THE System SHALL highlight the invalid fields and display inline validation error messages
5. WHEN a user clicks the detail button on a training job, THE System SHALL display a job detail panel with configuration parameters and simulated progress information

---

### Requirement 5: 数据管理（Data Management）

**User Story:** As a user, I want to manage datasets for model training, so that I can organize and prepare training data efficiently.

#### Acceptance Criteria

1. WHEN a user navigates to the Data Management page, THE System SHALL display a list of datasets with name, size, type, and creation date
2. WHEN a user clicks "新建数据集", THE System SHALL display a form for creating a new dataset with name, description, and type fields
3. WHEN a user submits a valid dataset creation form, THE System SHALL add the new dataset to the list immediately
4. IF a required field in the dataset form is empty when submitted, THEN THE System SHALL display validation error messages without closing the form
5. WHEN a user clicks the delete button on a dataset, THE System SHALL display a confirmation dialog before removing the dataset from the list

---

### Requirement 6: API Key 管理

**User Story:** As a user, I want to create and manage API keys, so that I can integrate the platform's model services into my applications.

#### Acceptance Criteria

1. WHEN a user navigates to the API Key management page, THE System SHALL display a list of existing API keys with name, masked key value, creation date, and status
2. WHEN a user clicks "新建 API Key", THE System SHALL display a form to input a key name and generate a new API key
3. WHEN a new API key is created, THE System SHALL display the full key value once in a modal with a copy button, and mask it in the list thereafter
4. WHEN a user clicks the delete button on an API key, THE System SHALL display a confirmation dialog before removing the key
5. WHEN a user clicks the copy button next to a masked API key, THE System SHALL copy the masked representation to clipboard and show a success toast notification

---

### Requirement 7: 模型部署与推理（Model Deployment & Inference）

**User Story:** As a user, I want to deploy models and test inference online, so that I can validate model performance and integrate it into applications.

#### Acceptance Criteria

1. WHEN a user navigates to the Model Deployment page, THE System SHALL display a list of deployed model instances with name, status, and endpoint URL
2. WHEN a user clicks "在线体验" on a model, THE System SHALL display an interactive chat/inference panel where the user can send prompts and receive simulated responses
3. WHEN a user submits a prompt in the inference panel, THE System SHALL display a loading indicator and then render the simulated response
4. WHEN a user navigates to the Batch Inference page, THE System SHALL display a form for submitting batch inference jobs with dataset selection and model selection

---

### Requirement 8: 导航与布局（Navigation & Layout）

**User Story:** As a user, I want a consistent and intuitive navigation layout, so that I can move between platform features efficiently.

#### Acceptance Criteria

1. WHEN a user is on any authenticated page, THE System SHALL display a left sidebar with grouped navigation items: 模型广场、模型训练、数据管理、安全工具、工具应用、统计看板
2. WHEN a user clicks a navigation item, THE System SHALL highlight the active item and navigate to the corresponding page
3. WHEN a user hovers over a collapsed sidebar item, THE System SHALL display a tooltip with the item label
4. WHEN the viewport width is below 1024px, THE System SHALL collapse the sidebar to icon-only mode automatically
5. WHILE a user is on any page, THE System SHALL display a top header with platform logo, breadcrumb navigation, and user profile menu

---

### Requirement 9: 统计看板（Analytics Dashboard）

**User Story:** As a user, I want to view API usage statistics and resource consumption charts, so that I can monitor platform usage and costs.

#### Acceptance Criteria

1. WHEN a user navigates to the Analytics page, THE System SHALL display API call trend charts grouped by time range (day/week/month)
2. WHEN a user selects a different time range, THE System SHALL update the charts to reflect the selected period
3. WHEN the Analytics page loads, THE System SHALL display summary cards for total API calls, total tokens consumed, and active model count
4. WHEN the Analytics page loads, THE System SHALL display a model usage breakdown chart showing relative usage per model

---

### Requirement 10: 科技感UI设计规范

**User Story:** As a user, I want a visually modern and tech-oriented interface, so that the platform feels professional and inspiring.

#### Acceptance Criteria

1. THE System SHALL use a dark-themed color palette with primary colors of deep navy (#0a0e1a), accent blue (#1677ff), and gradient highlights
2. THE System SHALL apply smooth CSS transitions (duration 200–300ms) on all interactive elements including buttons, cards, and sidebar items
3. THE System SHALL display animated gradient backgrounds or particle effects on the login page to convey a tech aesthetic
4. WHEN a user hovers over a card or button, THE System SHALL apply a subtle glow or elevation shadow effect
5. THE System SHALL use a consistent icon set (e.g., a single icon library) throughout all pages
