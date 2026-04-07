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
        <el-table-column label="缩略图" width="80" align="center">
          <template #default="{ row }">
            <el-image
              v-if="row.photo"
              :src="row.photo"
              fit="cover"
              style="width: 48px; height: 48px; cursor: pointer; border-radius: 6px;"
              :preview-src-list="[row.photo]"
              :initial-index="0"
            />
            <span v-else style="color: #c0c4cc; font-size: 12px;">无图</span>
          </template>
        </el-table-column>
        <el-table-column prop="code" label="ID" width="70" />
        <el-table-column prop="name" label="口味名称" min-width="120" />
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
    <el-dialog v-model="dialogVisible" :title="dialogTitle" width="560px">
      <el-form :model="form" label-width="90px">
        <el-form-item label="口味名称">
          <el-input v-model="form.name" placeholder="如 鸡肉口味" />
        </el-form-item>
        <el-form-item label="所属品牌">
          <el-select v-model="form.brand_code" placeholder="请选择品牌" style="width: 100%">
            <el-option v-for="b in brands" :key="b.code" :label="b.name" :value="b.code" />
          </el-select>
        </el-form-item>
        <el-form-item label="口味图片">
          <div class="photo-upload">
            <el-image
              v-if="form.photo"
              :src="form.photo"
              fit="cover"
              style="width: 96px; height: 96px; cursor: pointer; border-radius: 8px; border: 1px solid #dcdfe6;"
              :preview-src-list="[form.photo]"
              :initial-index="0"
            />
            <div v-else class="photo-placeholder" @click="triggerPhotoUpload">
              <span>+</span>
              <span style="font-size: 12px;">上传图片</span>
            </div>
            <div v-if="form.photo" style="margin-left: 12px;">
              <el-button size="small" type="danger" @click="form.photo = ''">移除图片</el-button>
            </div>
          </div>
          <input ref="photoInput" type="file" accept="image/*" style="display:none" @change="handlePhotoUpload" />
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
const photoInput = ref(null)
const form = ref({ name: '', brand_code: '', photo: '' })
const filterForm = ref({ name: '', brand_code: '' })
const pagination = ref({ page: 1, pageSize: 20 })

const dialogTitle = computed(() => dialogType.value === 'create' ? '新增口味' : '编辑口味')

const filteredData = computed(() => {
  return flavors.value.filter(f => {
    if (filterForm.value.name && !f.name.includes(filterForm.value.name)) return false
    if (filterForm.value.brand_code && f.brand_code !== filterForm.value.brand_code) return false
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
const handleReset = () => { filterForm.value = { name: '', brand_code: '' }; pagination.value.page = 1 }

const triggerPhotoUpload = () => { photoInput.value.click() }

const handlePhotoUpload = (e) => {
  const file = e.target.files[0]
  if (!file) return
  if (file.size > 5 * 1024 * 1024) { ElMessage.warning('图片大小不能超过5MB'); return }
  const reader = new FileReader()
  reader.onload = (ev) => { form.value.photo = ev.target.result }
  reader.readAsDataURL(file)
}

const showDialog = (type, row = null) => {
  dialogType.value = type
  if (type === 'edit' && row) {
    form.value = { code: row.code, name: row.name, brand_code: row.brand_code, photo: row.photo || '' }
  } else {
    form.value = { name: '', brand_code: '', photo: '' }
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
    if (!error.config?._handled) ElMessage.error(error.response?.data?.detail || '操作失败')
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
.table-card { flex: 1; }
.pagination { margin-top: 16px; display: flex; justify-content: flex-end; }
.photo-upload { display: flex; align-items: center; gap: 0; }
.photo-placeholder {
  width: 96px; height: 96px; border: 1px dashed #dcdfe6; border-radius: 8px;
  display: flex; flex-direction: column; align-items: center; justify-content: center;
  cursor: pointer; color: #909399; gap: 4px;
}
</style>
