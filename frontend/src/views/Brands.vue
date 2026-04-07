<template>
  <div class="page-container">
    <!-- 上部：查询条件 -->
    <el-card class="filter-card">
      <el-form :inline="true" :model="filterForm">
        <el-form-item label="品牌名称">
          <el-input v-model="filterForm.name" placeholder="模糊搜索" clearable />
        </el-form-item>
        <el-form-item label="国家">
          <el-select v-model="filterForm.country" placeholder="全部" clearable style="width: 120px">
            <el-option value="国内" label="国内" />
            <el-option value="国外" label="国外" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">查询</el-button>
          <el-button @click="handleReset">重置</el-button>
          <el-button type="success" @click="showDialog('create')">新增品牌</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 下部：数据明细 -->
    <el-card class="table-card">
      <el-table :data="pagedData" stripe v-loading="loading">
        <el-table-column prop="code" label="ID" width="80" />
        <el-table-column prop="name" label="品牌名称" />
        <el-table-column prop="country" label="国家" width="100">
          <template #default="{ row }">
            <el-tag :type="row.country === '国内' ? 'success' : 'warning'">{{ row.country }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_date" label="创建日期" width="160" />
        <el-table-column label="操作" width="180" fixed="right">
          <template #default="{ row }">
            <el-button size="small" @click="showDialog('edit', row)">编辑</el-button>
            <el-button size="small" type="danger" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
      <div class="pagination">
        <el-pagination
          v-model:current-page="pagination.page"
          v-model:page-size="pagination.pageSize"
          :page-sizes="[10, 20, 50, 100]"
          :total="filteredData.length"
          layout="total, sizes, prev, pager, next"
          background
        />
      </div>
    </el-card>

    <!-- 新增/编辑弹窗 -->
    <el-dialog v-model="dialogVisible" :title="dialogTitle" width="500px">
      <el-form :model="form" label-width="80px">
        <el-form-item label="品牌名称">
          <el-input v-model="form.name" />
        </el-form-item>
        <el-form-item label="国家">
          <el-select v-model="form.country">
            <el-option value="国内" label="国内" />
            <el-option value="国外" label="国外" />
          </el-select>
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
const form = ref({ name: '', country: '国内' })
const filterForm = ref({ name: '', country: '' })
const pagination = ref({ page: 1, pageSize: 20 })

const dialogTitle = computed(() => dialogType.value === 'create' ? '新增品牌' : '编辑品牌')

const filteredData = computed(() => {
  return brands.value.filter(b => {
    if (filterForm.value.name && !b.name.includes(filterForm.value.name)) return false
    if (filterForm.value.country && b.country !== filterForm.value.country) return false
    return true
  })
})

const pagedData = computed(() => {
  const start = (pagination.value.page - 1) * pagination.value.pageSize
  return filteredData.value.slice(start, start + pagination.value.pageSize)
})

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

const handleSearch = () => { pagination.value.page = 1 }
const handleReset = () => { filterForm.value = { name: '', country: '' }; pagination.value.page = 1 }

const showDialog = (type, row = null) => {
  dialogType.value = type
  if (type === 'edit' && row) {
    form.value = { code: row.code, name: row.name, country: row.country || '国内' }
  } else {
    form.value = { name: '', country: '国内' }
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
    if (error !== 'cancel') ElMessage.error('删除失败')
  }
}

onMounted(() => { loadBrands() })
</script>

<style scoped>
.page-container { display: flex; flex-direction: column; gap: 16px; height: 100%; }
.filter-card { }
.table-card { flex: 1; }
.pagination { margin-top: 16px; display: flex; justify-content: flex-end; }
</style>
