<template>
  <div class="app-container">
    <header class="app-header">
      <div class="header-content">
        <h1 class="app-title">缂丝扇面定制</h1>
        <nav class="app-nav">
          <router-link to="/" class="nav-link" active-class="active">客户下单</router-link>
          <router-link to="/admin" class="nav-link" active-class="active">管理员后台</router-link>
        </nav>
      </div>
    </header>
    <main class="app-main">
      <router-view />
    </main>
    <footer class="app-footer">
      <p>© 2026 缂丝工艺传承 · 匠心独运</p>
    </footer>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>
