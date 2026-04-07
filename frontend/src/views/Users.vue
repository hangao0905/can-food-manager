<template>
  <div class="page-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>用户管理</span>
          <el-button type="primary" @click="showCreate">新增用户</el-button>
        </div>
      </template>
      
      <el-table :data="users" stripe v-loading="loading">
        <el-table-column prop="id" label="ID" width="60" />
        <el-table-column prop="username" label="用户名" />
        <el-table-column prop="role" label="角色" width="100">
          <template #default="{ row }">
            <el-tag :type="row.role === 'admin' ? 'danger' : 'success'">{{ row.role === 'admin' ? '管理员' : '普通用户' }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.status === 'active' ? 'success' : 'info'">{{ row.status === 'active' ? '启用' : '停用' }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_date" label="创建日期" width="160" />
        <el-table-column label="操作" width="200">
          <template #default="{ row }">
            <el-button size="small" @click="showEdit(row)">编辑</el-button>
            <el-button size="small" :type="row.status === 'active' ? 'warning' : 'success'" @click="toggleStatus(row)">
              {{ row.status === 'active' ? '停用' : '启用' }}
            </el-button>
            <el-button size="small" type="danger" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog v-model="dialogVisible" :title="dialogTitle" width="400px">
      <el-form :model="form" label-width="80px">
        <el-form-item label="用户名">
          <el-input v-model="form.username" :disabled="!!form.id" />
        </el-form-item>
        <el-form-item label="密码">
          <el-input v-model="form.password" type="password" show-password :placeholder="form.id ? '留空则不修改' : ''" />
        </el-form-item>
        <el-form-item label="角色">
          <el-select v-model="form.role">
            <el-option value="admin" label="管理员" />
            <el-option value="user" label="普通用户" />
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
import { userApi } from '../api'

const users = ref([])
const loading = ref(false)
const dialogVisible = ref(false)
const dialogType = ref('create')
const form = ref({ id: null, username: '', password: '', role: 'user' })

const dialogTitle = computed(() => dialogType.value === 'create' ? '新增用户' : '编辑用户')

const loadUsers = async () => {
  loading.value = true
  try {
    const { data } = await userApi.list()
    users.value = data
  } catch (error) {
    ElMessage.error('加载用户失败')
  } finally {
    loading.value = false
  }
}

const showCreate = () => {
  dialogType.value = 'create'
  form.value = { id: null, username: '', password: '', role: 'user' }
  dialogVisible.value = true
}

const showEdit = (row) => {
  dialogType.value = 'edit'
  form.value = { id: row.id, username: row.username, password: '', role: row.role }
  dialogVisible.value = true
}

const handleSubmit = async () => {
  if (!form.value.username || (!form.value.password && dialogType.value === 'create')) {
    ElMessage.warning('请填写用户名和密码')
    return
  }
  try {
    if (dialogType.value === 'create') {
      await userApi.create(form.value.username, form.value.password, form.value.role)
      ElMessage.success('创建成功')
    } else {
      const updateData = { role: form.value.role }
      if (form.value.password) updateData.password = form.value.password
      await userApi.update(form.value.id, updateData)
      ElMessage.success('更新成功')
    }
    dialogVisible.value = false
    loadUsers()
  } catch (error) {
    if (!error.config?._handled) ElMessage.error(error.response?.data?.detail || '操作失败')
  }
}

const toggleStatus = async (row) => {
  const newStatus = row.status === 'active' ? 'inactive' : 'active'
  try {
    await userApi.update(row.id, { status: newStatus })
    ElMessage.success(newStatus === 'active' ? '已启用' : '已停用')
    loadUsers()
  } catch (error) {
    ElMessage.error('操作失败')
  }
}

const handleDelete = async (row) => {
  try {
    await ElMessageBox.confirm('确定删除该用户?', '提示', { type: 'warning' })
    await userApi.delete(row.id)
    ElMessage.success('删除成功')
    loadUsers()
  } catch (error) {
    if (error !== 'cancel') ElMessage.error('删除失败')
  }
}

onMounted(() => { loadUsers() })
</script>

<style scoped>
.page-container { height: 100%; }
.card-header { display: flex; justify-content: space-between; align-items: center; }
</style>
