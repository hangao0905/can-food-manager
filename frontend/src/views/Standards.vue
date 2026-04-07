<template>
  <div class="page-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>计算标准管理</span>
          <div>
            <el-button type="warning" @click="handleRecalcAll" :loading="recalcLoading">重新计算所有罐头</el-button>
            <el-button type="primary" @click="handleInitDefaults" :loading="initLoading">初始化默认标准</el-button>
          </div>
        </div>
      </template>
      
      <el-table :data="standards" stripe v-loading="loading">
        <el-table-column prop="id" label="ID" width="60" />
        <el-table-column prop="name" label="标准名称" width="180" />
        <el-table-column prop="field" label="字段" width="160">
          <template #default="{ row }">
            <el-tag type="info">{{ row.field }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="运算符" width="100">
          <template #default="{ row }">
            <el-select v-model="row.operator" style="width: 80px" @change="handleUpdate(row)">
              <el-option value=">=" label=">=" />
              <el-option value="<=" label="<=" />
              <el-option value=">" label=">" />
              <el-option value="<" label="<" />
              <el-option value="range" label="range" />
            </el-select>
          </template>
        </el-table-column>
        <el-table-column label="阈值" width="120">
          <template #default="{ row }">
            <el-input-number v-model="row.threshold" :min="0" :precision="4" style="width: 100px" @change="handleUpdate(row)" />
          </template>
        </el-table-column>
        <el-table-column v-if="showMax" label="上限阈值" width="120">
          <template #default="{ row }">
            <el-input-number v-model="row.threshold_max" :min="0" :precision="4" style="width: 100px" @change="handleUpdate(row)" />
          </template>
        </el-table-column>
        <el-table-column prop="unit" label="单位" width="120">
          <template #default="{ row }">
            <el-input v-model="row.unit" style="width: 100px" @change="handleUpdate(row)" />
          </template>
        </el-table-column>
        <el-table-column label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.status === 'active' ? 'success' : 'info'">{{ row.status === 'active' ? '启用' : '停用' }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="120">
          <template #default="{ row }">
            <el-button size="small" :type="row.status === 'active' ? 'danger' : 'success'" @click="toggleStatus(row)">
              {{ row.status === 'active' ? '停用' : '启用' }}
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { standardApi, canFoodApi } from '../api'

const standards = ref([])
const loading = ref(false)
const recalcLoading = ref(false)
const initLoading = ref(false)

const showMax = computed(() => standards.value.some(s => s.operator === 'range'))

const loadStandards = async () => {
  loading.value = true
  try {
    const { data } = await standardApi.list()
    standards.value = data
  } catch (error) {
    ElMessage.error('加载标准失败')
  } finally {
    loading.value = false
  }
}

const handleUpdate = async (row) => {
  try {
    await standardApi.update(row.id, {
      operator: row.operator,
      threshold: row.threshold,
      threshold_max: row.threshold_max,
      unit: row.unit,
    })
    ElMessage.success('更新成功')
  } catch (error) {
    ElMessage.error('更新失败')
  }
}

const toggleStatus = async (row) => {
  const newStatus = row.status === 'active' ? 'inactive' : 'active'
  try {
    await standardApi.update(row.id, { status: newStatus })
    row.status = newStatus
    ElMessage.success(newStatus === 'active' ? '已启用' : '已停用')
  } catch (error) {
    ElMessage.error('操作失败')
  }
}

const handleRecalcAll = async () => {
  try {
    recalcLoading.value = true
    const { data } = await canFoodApi.recalcAll()
    ElMessage.success(data.message || '重新计算完成')
  } catch (error) {
    ElMessage.error('重新计算失败')
  } finally {
    recalcLoading.value = false
  }
}

const handleInitDefaults = async () => {
  try {
    initLoading.value = true
    const { data } = await standardApi.init()
    ElMessage.success(data.message || '初始化完成')
    loadStandards()
  } catch (error) {
    ElMessage.error('初始化失败')
  } finally {
    initLoading.value = false
  }
}

onMounted(() => { loadStandards() })
</script>

<style scoped>
.page-container { height: 100%; }
.card-header { display: flex; justify-content: space-between; align-items: center; }
</style>
