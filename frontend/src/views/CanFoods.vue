<template>
  <div class="page-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>罐头管理</span>
          <el-button type="primary" @click="showDialog('create')">新增罐头</el-button>
        </div>
      </template>
      
      <el-table :data="canFoods" stripe v-loading="loading">
        <el-table-column prop="code" label="ID" width="100" />
        <el-table-column prop="brand.name" label="品牌" width="120" />
        <el-table-column prop="flavor.name" label="口味" width="100" />
        <el-table-column prop="description" label="简介" show-overflow-tooltip min-width="200" />
        <el-table-column prop="protein_pass" label="粗蛋白" width="80">
          <template #default="{ row }">{{ row.protein_pass || '-' }}</template>
        </el-table-column>
        <el-table-column prop="fat_pass" label="粗脂肪" width="80">
          <template #default="{ row }">{{ row.fat_pass || '-' }}</template>
        </el-table-column>
        <el-table-column prop="fiber_pass" label="粗纤维" width="80">
          <template #default="{ row }">{{ row.fiber_pass || '-' }}</template>
        </el-table-column>
        <el-table-column prop="creator" label="创建人" width="100" />
        <el-table-column label="操作" width="180" fixed="right">
          <template #default="{ row }">
            <el-button size="small" @click="showDialog('edit', row)">编辑</el-button>
            <el-button size="small" type="danger" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog v-model="dialogVisible" :title="dialogTitle" width="600px">
      <el-form :model="form" label-width="90px">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="品牌">
              <el-select v-model="form.brand_code" placeholder="请选择品牌" @change="onBrandChange">
                <el-option v-for="b in brands" :key="b.code" :label="b.name" :value="b.code" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="口味">
              <el-select v-model="form.flavor_code" placeholder="请先选品牌">
                <el-option v-for="f in filteredFlavors" :key="f.code" :label="f.name" :value="f.code" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="简介">
          <el-input v-model="form.description" type="textarea" rows="3" />
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
import { canFoodApi, brandApi, flavorApi } from '../api'

const canFoods = ref([])
const brands = ref([])
const flavors = ref([])
const loading = ref(false)
const dialogVisible = ref(false)
const dialogType = ref('create')
const form = ref({ brand_code: '', flavor_code: '', description: '', creator: '' })

const dialogTitle = computed(() => dialogType.value === 'create' ? '新增罐头' : '编辑罐头')

const filteredFlavors = computed(() => {
  if (!form.value.brand_code) return []
  return flavors.value.filter(f => f.brand_code === form.value.brand_code)
})

const onBrandChange = () => {
  form.value.flavor_code = ''
}

const loadCanFoods = async () => {
  loading.value = true
  try {
    const { data } = await canFoodApi.list()
    canFoods.value = data
  } catch (error) {
    ElMessage.error('加载罐头失败')
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

const loadFlavors = async () => {
  try {
    const { data } = await flavorApi.list()
    flavors.value = data
  } catch (error) {
    console.error('加载口味失败', error)
  }
}

const showDialog = (type, row = null) => {
  dialogType.value = type
  if (type === 'edit' && row) {
    form.value = { code: row.code, brand_code: row.brand_code, flavor_code: row.flavor_code, description: row.description || '', creator: row.creator || '' }
  } else {
    form.value = { brand_code: '', flavor_code: '', description: '', creator: '' }
  }
  dialogVisible.value = true
}

const handleSubmit = async () => {
  try {
    if (dialogType.value === 'create') {
      await canFoodApi.create(form.value)
      ElMessage.success('创建成功')
    } else {
      await canFoodApi.update(form.value.code, form.value)
      ElMessage.success('更新成功')
    }
    dialogVisible.value = false
    loadCanFoods()
  } catch (error) {
    ElMessage.error(error.response?.data?.detail || '操作失败')
  }
}

const handleDelete = async (row) => {
  try {
    await ElMessageBox.confirm('确定删除该罐头?', '提示', { type: 'warning' })
    await canFoodApi.delete(row.code)
    ElMessage.success('删除成功')
    loadCanFoods()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

onMounted(() => {
  loadCanFoods()
  loadBrands()
  loadFlavors()
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
