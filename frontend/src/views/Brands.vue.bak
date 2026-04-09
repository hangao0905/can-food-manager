<template>
  <div class="page-container">
    <!-- 上部：查询条件 -->
    <el-card class="filter-card">
      <el-form :inline="true" :model="filterForm">
        <el-form-item label="品牌名称">
          <el-input v-model="filterForm.name" placeholder="模糊搜索" clearable />
        </el-form-item>
        <el-form-item label="通俗名">
          <el-input v-model="filterForm.alias" placeholder="模糊搜索" clearable />
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
        <el-table-column label="Logo" width="70" align="center">
          <template #default="{ row }">
            <el-image
              v-if="row.logo"
              :src="row.logo"
              fit="contain"
              style="width: 40px; height: 40px; cursor: pointer; border-radius: 4px;"
              :preview-src-list="[row.logo]"
              :initial-index="0"
            />
            <span v-else style="color: #c0c4cc; font-size: 12px;">无</span>
          </template>
        </el-table-column>
        <el-table-column prop="code" label="ID" width="70" />
        <el-table-column prop="name" label="品牌名称" min-width="120" />
        <el-table-column prop="alias" label="通俗名" min-width="120">
          <template #default="{ row }">{{ row.alias || '-' }}</template>
        </el-table-column>
        <el-table-column prop="description" label="简介" show-overflow-tooltip min-width="160">
          <template #default="{ row }">{{ row.description || '-' }}</template>
        </el-table-column>
        <el-table-column prop="country" label="国家" width="90" align="center">
          <template #default="{ row }">
            <el-tag :type="row.country === '国内' ? 'success' : 'warning'" size="small">
              {{ row.country || '-' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_date" label="创建时间" width="120" />
        <el-table-column label="操作" width="150" fixed="right">
          <template #default="{ row }">
            <el-button size="small" @click="showDialog('edit', row)">编辑</el-button>
            <el-button size="small" type="danger" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
      
      <el-pagination
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        :page-sizes="[10, 20, 50, 100]"
        :total="filteredData.length"
        layout="total, sizes, prev, pager, next, jumper"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        style="margin-top: 20px;"
      />
    </el-card>

    <!-- 新增/编辑对话框 -->
    <el-dialog v-model="dialogVisible" :title="dialogTitle" width="500px">
      <el-form :model="form" label-width="80px" :rules="rules" ref="formRef">
        <el-form-item label="品牌名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入品牌名称" />
        </el-form-item>
        <el-form-item label="通俗名">
          <el-input v-model="form.alias" placeholder="请输入通俗名（可选）" />
        </el-form-item>
        <el-form-item label="Logo URL">
          <el-input v-model="form.logo" placeholder="请输入Logo图片URL（可选）" />
        </el-form-item>
        <el-form-item label="品牌简介">
          <el-input
            v-model="form.description"
            type="textarea"
            :rows="3"
            placeholder="请输入品牌简介（可选）"
          />
        </el-form-item>
        <el-form-item label="国家">
          <el-select v-model="form.country" placeholder="请选择" style="width: 100%">
            <el-option value="国内" label="国内" />
            <el-option value="国外" label="国外" />
          </el-select>
        </el-form-item>
        <el-form-item label="创建时间">
          <el-input v-model="form.created_date" placeholder="格式：YYYY-MM-DD HH:MM:SS（可选）" />
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
import axios from 'axios'

const loading = ref(false)
const dialogVisible = ref(false)
const dialogType = ref('create')
const brands = ref([])
const currentPage = ref(1)
const pageSize = ref(10)
const formRef = ref()

// 查询表单
const filterForm = ref({
  name: '',
  alias: '',
  country: ''
})

// 编辑表单
const form = ref({
  name: '',
  alias: '',
  logo: '',
  description: '',
  country: '',
  created_date: ''
})

// 表单验证规则
const rules = {
  name: [{ required: true, message: '请输入品牌名称', trigger: 'blur' }]
}

const dialogTitle = computed(() => {
  return dialogType.value === 'create' ? '新增品牌' : '编辑品牌'
})

// 加载品牌数据
const loadBrands = async () => {
  loading.value = true
  try {
    const { data } = await axios.get('/api/brands/')
    brands.value = data
  } catch (error) {
    ElMessage.error('加载品牌失败')
  } finally {
    loading.value = false
  }
}

// 过滤数据
const filteredData = computed(() => {
  return brands.value.filter(brand => {
    const nameMatch = !filterForm.value.name || 
      (brand.name && brand.name.toLowerCase().includes(filterForm.value.name.toLowerCase()))
    const aliasMatch = !filterForm.value.alias || 
      (brand.alias && brand.alias.toLowerCase().includes(filterForm.value.alias.toLowerCase()))
    const countryMatch = !filterForm.value.country || brand.country === filterForm.value.country
    return nameMatch && aliasMatch && countryMatch
  })
})

// 分页数据
const pagedData = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value
  const end = start + pageSize.value
  return filteredData.value.slice(start, end)
})

// 查询
const handleSearch = () => {
  currentPage.value = 1
}

// 重置查询
const handleReset = () => {
  filterForm.value = { name: '', alias: '', country: '' }
  currentPage.value = 1
}

// 显示对话框
const showDialog = (type, row = null) => {
  dialogType.value = type
  if (type === 'edit' && row) {
    form.value = { ...row }
  } else {
    form.value = {
      name: '',
      alias: '',
      logo: '',
      description: '',
      country: '',
      created_date: ''
    }
  }
  dialogVisible.value = true
}

// 保存品牌
const handleSubmit = async () => {
  if (!formRef.value) return
  
  try {
    await formRef.value.validate()
    
    if (dialogType.value === 'create') {
      await axios.post('/api/brands/', form.value)
      ElMessage.success('创建成功')
    } else {
      await axios.put(`/api/brands/${form.value.code}`, form.value)
      ElMessage.success('更新成功')
    }
    dialogVisible.value = false
    loadBrands()
  } catch (error) {
    if (error.name !== 'ValidationError') {
      ElMessage.error(error.response?.data?.detail || '操作失败')
    }
  }
}

// 删除品牌
const handleDelete = async (row) => {
  try {
    await ElMessageBox.confirm('确定删除该品牌?', '提示', {
      type: 'warning'
    })
    await axios.delete(`/api/brands/${row.code}`)
    ElMessage.success('删除成功')
    loadBrands()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

// 分页大小改变
const handleSizeChange = (val) => {
  pageSize.value = val
  currentPage.value = 1
}

// 当前页改变
const handleCurrentChange = (val) => {
  currentPage.value = val
}

onMounted(() => {
  loadBrands()
})
</script>

<style scoped>
.filter-card {
  margin-bottom: 20px;
}
.table-card {
  margin-top: 20px;
}
</style>
