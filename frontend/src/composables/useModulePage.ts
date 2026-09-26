/**
 * 业务模块页共用能力：列表筛选、登记入口、动作处理与错误文案统一在这里。
 *
 * 各模块页（检测方法、样品接收等）只有配置差异，处理流程完全一致，
 * 因此 reload / runAction / 分支判断只写这一遍，文案统一从配置取。
 */
import { onMounted, ref } from 'vue'

import { request } from '@/api/client'

export interface ModulePageConfig {
  /** 后端模块名，同时作为接口路径，如 'method' */
  module: string
  /** 面向用户的模块名，如 '检测方法' */
  label: string
  /** 单条记录的称呼，如 '检测方法' / '检测任务单' */
  entryName: string
  /** 表格列（= 展示字段），前三列同时作为筛选条件 */
  columns: string[]
  /** 可执行动作，顺序即按钮顺序 */
  actions: string[]
  /** 顶部统计卡片配置（当前为静态占位） */
  stats: { label: string; value: number }[]
}

export function useModulePage(config: ModulePageConfig) {
  const endpoint = `/api/${config.module}`
  type Row = Record<string, string | number | null>

  const rows = ref<Row[]>([])
  const total = ref(0)
  const errorMessage = ref('')
  const filters = ref<Record<string, string>>({})
  const filterFields = config.columns.slice(0, 3)

  function resetFilters() {
    filters.value = {}
    void reload()
  }

  function exportRows() {
    window.open(`${endpoint}/export`, '_blank')
  }

  function openCreate() {
    errorMessage.value = `${config.entryName}登记入口尚未接入审批流`
  }

  async function runAction(action: string, row: Row) {
    errorMessage.value = ''
    try {
      const response = await request(`${endpoint}/${row.id}/actions`, {
        method: 'POST',
        body: JSON.stringify({ action }),
      })
      if (!response.ok) {
        throw new Error(`${config.label}动作未生效，请稍后重试`)
      }
      await reload()
    } catch (error) {
      errorMessage.value = error instanceof Error ? error.message : `${config.label}操作失败`
    }
  }

  async function reload() {
    errorMessage.value = ''
    const query = new URLSearchParams(filters.value as Record<string, string>).toString()
    try {
      const response = await request(`${endpoint}?${query}`)
      if (!response.ok) {
        throw new Error(`${config.label}列表读取失败`)
      }
      const payload = await response.json()
      rows.value = payload.items ?? []
      total.value = payload.total ?? rows.value.length
    } catch (error) {
      errorMessage.value = error instanceof Error ? error.message : `${config.label}列表读取失败`
    }
  }

  onMounted(reload)

  return {
    rows,
    total,
    errorMessage,
    filters,
    filterFields,
    resetFilters,
    exportRows,
    openCreate,
    runAction,
    reload,
  }
}
