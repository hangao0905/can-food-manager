<template>
  <div class="page-container">
    <!-- 上卡片：查询条件 -->
    <el-card class="search-card">
      <template #header>
        <div class="card-header">
          <span>查询条件</span>
          <el-button type="primary" @click="handleSearch">查询</el-button>
          <el-button @click="handleReset">重置</el-button>
        </div>
      </template>
      
      <el-form :model="searchForm" inline>
        <el-form-item label="所属品牌">
          <el-select v-model="searchForm.brand_code" placeholder="请选择品牌" clearable>
            <el-option v-for="b in brands" :key="b.code" :label="b.name" :value="b.code" />
          </el-select>
        </el-form-item>
        <el-form-item label="口味名称">
          <el-input v-model="searchForm.name" placeholder="请输入口味名称" clearable />
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 下卡片：查询结果 -->
    <el-card class="result-card">
      <template #header>
        <div class="card-header">
          <span>查询结果 (共 {{ total }} 条)</span>
          <el-button type="primary" @click="showDialog('create')">新增口味</el-button>
        </div>
      </template>
      
      <el-table :data="flavors" stripe v-loading="loading">
        <el-table-column prop="code" label="Code" width="80" />
        <el-table-column prop="name" label="口味名称" />
        <el-table-column prop="brand.name" label="所属品牌" />
        <el-table-column prop="created_date" label="创建时间" width="120" />
        <el-table-column label="操作" width="180">
          <template #default="{ row }">
            <el-button size="small" @click="showDialog('edit', row)">编辑</el-button>
            <el-button size="small" type="danger" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页组件 -->
      <div class="pagination-container">
        <el-pagination
          v-model:current-page="pagination.page"
          v-model:page-size="pagination.pageSize"
          :page-sizes="[10, 20, 50, 100]"
          :total="total"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handlePageChange"
        />
      </div>
    </el-card>

    <!-- 新增/编辑对话框 -->
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
        <el-form-item label="创建时间">
          <el-input v-model="form.created_date" />
        </el-form-item>
        <el-form-item label="照片">
          <el-input v-model="form.photo" />
        </el-form-item>
        <el-form-item label="创建者">
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
const total = ref(0)

// 分页参数
const pagination = ref({
  page: 1,
  pageSize: 20
})

// 查询表单
const searchForm = ref({
  name: '',
  brand_code: null
})

// 新增/编辑表单
const form = ref({ name: '', brand_code: '', created_date: '', photo: '', creator: '' })

const dialogTitle = computed(() => dialogType.value === 'create' ? '新增口味' : '编辑口味')

// 加载口味列表
const loadFlavors = async () => {
  loading.value = true
  try {
    const params = {
      skip: (pagination.value.page - 1) * pagination.value.pageSize,
      limit: pagination.value.pageSize
    }
    if (searchForm.value.name) {
      params.name = searchForm.value.name
    }
    if (searchForm.value.brand_code) {
      params.brand_code = searchForm.value.brand_code
    }
    const { data } = await flavorApi.list(params)
    flavors.value = data.data
    total.value = data.total
  } catch (error) {
    ElMessage.error('加载口味失败')
  } finally {
    loading.value = false
  }
}

// 加载品牌列表
const loadBrands = async () => {
  try {
    const { data } = await brandApi.list()
    brands.value = data
  } catch (error) {
    console.error('加载品牌失败', error)
  }
}

// 查询
const handleSearch = () => {
  pagination.value.page = 1
  loadFlavors()
}

// 重置
const handleReset = () => {
  searchForm.value = {
    name: '',
    brand_code: null
  }
  pagination.value.page = 1
  pagination.value.pageSize = 20
  loadFlavors()
}

// 分页大小改变
const handleSizeChange = () => {
  pagination.value.page = 1
  loadFlavors()
}

// 页码改变
const handlePageChange = () => {
  loadFlavors()
}

// 显示对话框
const showDialog = (type, row = null) => {
  dialogType.value = type
  if (type === 'edit' && row) {
    form.value = { ...row }
  } else {
    form.value = { name: '', brand_code: '', created_date: '', photo: '', creator: '' }
  }
  dialogVisible.value = true
}

// 提交表单
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

// 删除
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
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.search-card {
  flex-shrink: 0;
}

.result-card {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.pagination-container {
  margin-top: 16px;
  display: flex;
  justify-content: flex-end;
}
</style>
