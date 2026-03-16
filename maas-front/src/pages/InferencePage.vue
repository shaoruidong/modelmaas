<script setup lang="ts">
import { ref, nextTick } from 'vue'
import { useModelStore } from '@/stores/models'

const modelStore = useModelStore()

const selectedModelId = ref(modelStore.models[0]?.id ?? '')
const selectedModel = ref(modelStore.models[0])
const inputText = ref('')
const loading = ref(false)
const messagesRef = ref<HTMLElement | null>(null)

interface Message {
  role: 'user' | 'assistant'
  content: string
  time: string
}

const messages = ref<Message[]>([
  {
    role: 'assistant',
    content:
      '你好！我是 MaaS 平台的 AI 助手。请选择一个模型开始对话，我可以帮助你回答问题、生成内容、分析数据等。',
    time: new Date().toLocaleTimeString('zh-CN', { hour12: false }),
  },
])

const mockResponses = [
  '这是一个很好的问题！根据我的理解，{input}涉及到多个维度的考量。首先从技术层面来看，我们需要考虑系统的可扩展性和性能；其次从业务层面，需要平衡用户体验和成本效益。建议您可以从以下几个步骤入手：\n\n1. 明确核心需求和约束条件\n2. 评估现有技术方案的优劣\n3. 制定渐进式的实施计划\n\n如需进一步探讨，欢迎继续提问。',
  '感谢您的提问！关于"{input}"，这是一个在AI领域非常重要的话题。大语言模型通过海量数据训练，能够理解和生成自然语言。在实际应用中，模型的效果很大程度上取决于提示词的质量和上下文的完整性。',
  '您好！我理解您想了解关于"{input}"的内容。这个问题可以从多个角度来分析：\n\n**技术角度**：现代AI系统采用Transformer架构，通过注意力机制处理序列数据。\n\n**应用角度**：在企业场景中，可以用于自动化文档处理、智能客服、代码辅助等多种场景。\n\n希望这个回答对您有帮助！',
]

function selectModel(id: string) {
  selectedModelId.value = id
  selectedModel.value = modelStore.models.find((m) => m.id === id) ?? modelStore.models[0]
  messages.value = [
    {
      role: 'assistant',
      content: `已切换到 ${selectedModel.value?.name}。有什么我可以帮助您的？`,
      time: new Date().toLocaleTimeString('zh-CN', { hour12: false }),
    },
  ]
}

async function sendMessage() {
  const text = inputText.value.trim()
  if (!text || loading.value) return

  messages.value.push({
    role: 'user',
    content: text,
    time: new Date().toLocaleTimeString('zh-CN', { hour12: false }),
  })
  inputText.value = ''
  loading.value = true

  await nextTick()
  scrollToBottom()

  await new Promise((r) => setTimeout(r, 1200 + Math.random() * 800))

  const template = mockResponses[Math.floor(Math.random() * mockResponses.length)]
  const response = template.replace('{input}', text.slice(0, 20))

  messages.value.push({
    role: 'assistant',
    content: response,
    time: new Date().toLocaleTimeString('zh-CN', { hour12: false }),
  })
  loading.value = false

  await nextTick()
  scrollToBottom()
}

function scrollToBottom() {
  if (messagesRef.value) {
    messagesRef.value.scrollTop = messagesRef.value.scrollHeight
  }
}

function handleKeydown(e: KeyboardEvent) {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault()
    sendMessage()
  }
}
</script>

<template>
  <div class="inference-layout">
    <!-- Left: model list -->
    <aside class="model-panel">
      <div class="panel-title">选择模型</div>
      <div class="model-list">
        <div
          v-for="m in modelStore.models"
          :key="m.id"
          class="model-item"
          :class="{ active: selectedModelId === m.id }"
          @click="selectModel(m.id)"
        >
          <div class="model-item-name">{{ m.name }}</div>
          <div class="model-item-sub">{{ m.provider }} · {{ m.parameterSize }}</div>
        </div>
      </div>
    </aside>

    <!-- Right: chat panel -->
    <div class="chat-panel">
      <!-- Chat header -->
      <div class="chat-header">
        <div class="chat-model-info">
          <div class="chat-model-name">{{ selectedModel?.name }}</div>
          <div class="chat-model-sub">
            {{ selectedModel?.provider }} · {{ selectedModel?.parameterSize }}
          </div>
        </div>
        <div class="chat-tags">
          <el-tag
            v-for="tag in selectedModel?.tags.slice(0, 3)"
            :key="tag"
            size="small"
            effect="plain"
          >
            {{ tag }}
          </el-tag>
        </div>
      </div>

      <!-- Messages -->
      <div ref="messagesRef" class="messages-area">
        <div v-for="(msg, i) in messages" :key="i" class="message-row" :class="msg.role">
          <div class="message-avatar">
            <span v-if="msg.role === 'assistant'">AI</span>
            <span v-else>我</span>
          </div>
          <div class="message-bubble">
            <div class="message-content" style="white-space: pre-wrap">{{ msg.content }}</div>
            <div class="message-time">{{ msg.time }}</div>
          </div>
        </div>

        <!-- Loading indicator -->
        <div v-if="loading" class="message-row assistant">
          <div class="message-avatar">AI</div>
          <div class="message-bubble">
            <div class="typing-indicator"><span></span><span></span><span></span></div>
          </div>
        </div>
      </div>

      <!-- Input area -->
      <div class="input-area">
        <el-input
          v-model="inputText"
          type="textarea"
          :rows="3"
          placeholder="输入消息，按 Enter 发送，Shift+Enter 换行..."
          resize="none"
          @keydown="handleKeydown"
        />
        <div class="input-actions">
          <span class="input-hint">Enter 发送 · Shift+Enter 换行</span>
          <el-button
            type="primary"
            :loading="loading"
            :disabled="!inputText.trim()"
            @click="sendMessage"
          >
            <el-icon v-if="!loading"><Promotion /></el-icon>
            发送
          </el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.inference-layout {
  display: flex;
  height: calc(100vh - var(--header-height));
  overflow: hidden;
}

/* Model panel */
.model-panel {
  width: 220px;
  flex-shrink: 0;
  background: var(--color-bg-sidebar);
  border-right: 1px solid var(--color-border);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.panel-title {
  padding: 16px;
  font-size: 13px;
  font-weight: 600;
  color: var(--color-text-muted);
  border-bottom: 1px solid var(--color-border);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.model-list {
  flex: 1;
  overflow-y: auto;
  padding: 8px;
}

.model-item {
  padding: 10px 12px;
  border-radius: var(--radius-sm);
  cursor: pointer;
  transition: all var(--transition-fast);
  margin-bottom: 2px;
}

.model-item:hover {
  background: var(--color-accent-light);
}

.model-item.active {
  background: var(--color-accent-light);
  border-left: 2px solid var(--color-accent);
}

.model-item-name {
  font-size: 13px;
  font-weight: 500;
  color: var(--color-text-primary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.model-item-sub {
  font-size: 11px;
  color: var(--color-text-muted);
  margin-top: 2px;
}

/* Chat panel */
.chat-panel {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  background: var(--color-bg-primary);
}

.chat-header {
  padding: 16px 24px;
  border-bottom: 1px solid var(--color-border);
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: var(--color-bg-header);
  flex-shrink: 0;
}

.chat-model-name {
  font-size: 15px;
  font-weight: 600;
  color: var(--color-text-primary);
}

.chat-model-sub {
  font-size: 12px;
  color: var(--color-text-muted);
  margin-top: 2px;
}

.chat-tags {
  display: flex;
  gap: 6px;
}

/* Messages */
.messages-area {
  flex: 1;
  overflow-y: auto;
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.message-row {
  display: flex;
  gap: 12px;
  align-items: flex-start;
}

.message-row.user {
  flex-direction: row-reverse;
}

.message-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 600;
  flex-shrink: 0;
}

.message-row.assistant .message-avatar {
  background: var(--gradient-primary);
  color: #fff;
}

.message-row.user .message-avatar {
  background: var(--color-bg-card);
  color: var(--color-text-secondary);
  border: 1px solid var(--color-border);
}

.message-bubble {
  max-width: 70%;
}

.message-content {
  padding: 12px 16px;
  border-radius: var(--radius-md);
  font-size: 14px;
  line-height: 1.7;
}

.message-row.assistant .message-content {
  background: var(--color-bg-card);
  border: 1px solid var(--color-border);
  color: var(--color-text-primary);
  border-top-left-radius: 4px;
}

.message-row.user .message-content {
  background: var(--color-accent);
  color: #fff;
  border-top-right-radius: 4px;
}

.message-time {
  font-size: 11px;
  color: var(--color-text-muted);
  margin-top: 4px;
  padding: 0 4px;
}

.message-row.user .message-time {
  text-align: right;
}

/* Typing indicator */
.typing-indicator {
  display: flex;
  gap: 4px;
  padding: 12px 16px;
  background: var(--color-bg-card);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  border-top-left-radius: 4px;
  width: fit-content;
}

.typing-indicator span {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--color-accent);
  animation: bounce 1.2s ease-in-out infinite;
}

.typing-indicator span:nth-child(2) {
  animation-delay: 0.2s;
}
.typing-indicator span:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes bounce {
  0%,
  60%,
  100% {
    transform: translateY(0);
    opacity: 0.4;
  }
  30% {
    transform: translateY(-6px);
    opacity: 1;
  }
}

/* Input area */
.input-area {
  padding: 16px 24px;
  border-top: 1px solid var(--color-border);
  background: var(--color-bg-header);
  flex-shrink: 0;
}

.input-area :deep(.el-textarea__inner) {
  background: var(--color-bg-input) !important;
  border-color: var(--color-border) !important;
  color: var(--color-text-primary) !important;
  resize: none !important;
}

.input-area :deep(.el-textarea__inner:focus) {
  border-color: var(--color-accent) !important;
}

.input-actions {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 10px;
}

.input-hint {
  font-size: 12px;
  color: var(--color-text-muted);
}
</style>
