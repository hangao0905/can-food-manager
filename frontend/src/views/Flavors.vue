<template>
  <div class="page-container">
    <!-- 上部：查询条件 -->
    <el-card class="filter-card">
      <el-form :inline="true" :model="filterForm">
        <el-form-item label="口味名称">
          <el-input v-model="filterForm.name" placeholder="模糊搜索" clearable />
        </el-form-item>
        <el-form-item label="所属品牌">
          <el-select v-model="filterForm.brand_code" placeholder="全部" clearable style="width: 150px" @change="handleSearch">
            <el-option v-for="b in brands" :key="b.code" :label="b.name" :value="b.code" />
          </el-select>
        </el-form-item>
        <el-form-item label="创建人">
          <el-input v-model="filterForm.creator" placeholder="模糊搜索" clearable />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">查询</el-button>
          <el-button @click="handleReset">重置</el-button>
          <el-button type="success" @click="showDialog('create')">新增口味</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 下部：数据明细 -->
    <el-card class="table-card">
      <el-table :data="pagedData" stripe v-loading="loading">
        <el-table-column prop="code" label="ID" width="80" />
        <el-table-column prop="name" label="口味名称" />
        <el-table-column prop="brand.name" label="所属品牌" width="120" />
        <el-table-column prop="creator" label="创建人" width="100" />
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
const filterForm = ref({ name: '', brand_code: '', creator: '' })
const pagination = ref({ page: 1, pageSize: 20 })

const dialogTitle = computed(() => dialogType.value === 'create' ? '新增口味' : '编辑口味')

const filteredData = computed(() => {
  return flavors.value.filter(f => {
    if (filterForm.value.name && !f.name.includes(filterForm.value.name)) return false
    if (filterForm.value.brand_code && f.brand_code !== filterForm.value.brand_code) return false
    if (filterForm.value.creator && !f.creator?.includes(filterForm.value.creator)) return false
    return true
  })
})

const pagedData = computed(() => {
  const start = (pagination.value.page - 1) * pagination.value.pageSize
  return filteredData.value.slice(start, start + pagination.value.pageSize)
})

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
  try { const { data } = await brandApi.list(); brands.value = data } catch (e) {}
}

const handleSearch = () => { pagination.value.page = 1 }
const handleReset = () => { filterForm.value = { name: '', brand_code: '', creator: '' }; pagination.value.page = 1 }

const showDialog = (type, row = null) => {
  dialogType.value = type
  if (type === 'edit' && row) {
    form.value = { code: row.code, name: row.name, brand_code: row.brand_code, creator: row.creator || '' }
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
    if (error !== 'cancel') ElMessage.error('删除失败')
  }
}

onMounted(() => { loadFlavors(); loadBrands() })
</script>

<style scoped>
.page-container { display: flex; flex-direction: column; gap: 16px; height: 100%; }
.filter-card { }
.table-card { flex: 1; }
.pagination { margin-top: 16px; display: flex; justify-content: flex-end; }
</style>
