<template>
  <div class="page-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>品牌管理</span>
          <el-button type="primary" @click="showDialog('create')">新增品牌</el-button>
        </div>
      </template>
      
      <el-table :data="brands" stripe v-loading="loading">
        <el-table-column prop="code" label="ID" width="80" />
        <el-table-column prop="name" label="品牌名称" />
        <el-table-column prop="created_date" label="创建日期" width="160" />
        <el-table-column label="操作" width="180">
          <template #default="{ row }">
            <el-button size="small" @click="showDialog('edit', row)">编辑</el-button>
            <el-button size="small" type="danger" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog v-model="dialogVisible" :title="dialogTitle" width="500px">
      <el-form :model="form" label-width="80px">
        <el-form-item label="品牌名称">
          <el-input v-model="form.name" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { brandApi } from '../api'

const brands = ref([])
const loading = ref(false)
const dialogVisible = ref(false)
const dialogType = ref('create')
const form = ref({ name: '' })

const dialogTitle = computed(() => dialogType.value === 'create' ? '新增品牌' : '编辑品牌')

const loadBrands = async () => {
  loading.value = true
  try {
    const { data } = await brandApi.list()
    brands.value = data
  } catch (error) {
    ElMessage.error('加载品牌失败')
  } finally {
    loading.value = false
  }
}

const showDialog = (type, row = null) => {
  dialogType.value = type
  if (type === 'edit' && row) {
    form.value = { code: row.code, name: row.name }
  } else {
    form.value = { name: '' }
  }
  dialogVisible.value = true
}

const handleSubmit = async () => {
  try {
    if (dialogType.value === 'create') {
      await brandApi.create(form.value)
      ElMessage.success('创建成功')
    } else {
      await brandApi.update(form.value.code, form.value)
      ElMessage.success('更新成功')
    }
    dialogVisible.value = false
    loadBrands()
  } catch (error) {
    ElMessage.error(error.response?.data?.detail || '操作失败')
  }
}

const handleDelete = async (row) => {
  try {
    await ElMessageBox.confirm('确定删除该品牌?', '提示', { type: 'warning' })
    await brandApi.delete(row.code)
    ElMessage.success('删除成功')
    loadBrands()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

onMounted(() => {
  loadBrands()
})
</script>

<style scoped>
.page-container {
  height: 100%;
}
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
