<template>
  <div class="page-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>口味管理</span>
          <el-button type="primary" @click="showDialog('create')">新增口味</el-button>
        </div>
      </template>
      
      <el-table :data="flavors" stripe v-loading="loading">
        <el-table-column prop="code" label="ID" width="80" />
        <el-table-column prop="name" label="口味名称" />
        <el-table-column prop="brand.name" label="所属品牌" />
        <el-table-column prop="creator" label="创建人" width="100" />
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
        <el-form-item label="口味名称">
          <el-input v-model="form.name" />
        </el-form-item>
        <el-form-item label="所属品牌">
          <el-select v-model="form.brand_code" placeholder="请选择品牌">
            <el-option v-for="b in brands" :key="b.code" :label="b.name" :value="b.code" />
          </el-select>
        </el-form-item>
        <el-form-item label="创建人">
          <el-input v-model="form.creator" />
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
import { flavorApi, brandApi } from '../api'

const flavors = ref([])
const brands = ref([])
const loading = ref(false)
const dialogVisible = ref(false)
const dialogType = ref('create')
const form = ref({ name: '', brand_code: '', creator: '' })

const dialogTitle = computed(() => dialogType.value === 'create' ? '新增口味' : '编辑口味')

const loadFlavors = async () => {
  loading.value = true
  try {
    const { data } = await flavorApi.list()
    flavors.value = data
  } catch (error) {
    ElMessage.error('加载口味失败')
  } finally {
    loading.value = false
  }
}

const loadBrands = async () => {
  try {
    const { data } = await brandApi.list()
    brands.value = data
  } catch (error) {
    console.error('加载品牌失败', error)
  }
}

const showDialog = (type, row = null) => {
  dialogType.value = type
  if (type === 'edit' && row) {
    form.value = { name: row.name, brand_code: row.brand_code, creator: row.creator || '' }
  } else {
    form.value = { name: '', brand_code: '', creator: '' }
  }
  dialogVisible.value = true
}

const handleSubmit = async () => {
  try {
    if (dialogType.value === 'create') {
      await flavorApi.create(form.value)
      ElMessage.success('创建成功')
    } else {
      await flavorApi.update(form.value.code, form.value)
      ElMessage.success('更新成功')
    }
    dialogVisible.value = false
    loadFlavors()
  } catch (error) {
    ElMessage.error(error.response?.data?.detail || '操作失败')
  }
}

const handleDelete = async (row) => {
  try {
    await ElMessageBox.confirm('确定删除该口味?', '提示', { type: 'warning' })
    await flavorApi.delete(row.code)
    ElMessage.success('删除成功')
    loadFlavors()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

onMounted(() => {
  loadFlavors()
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
