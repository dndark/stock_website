<template>
<div>
  <b-navbar toggleable="lg" type="dark" variant="primary">
    <b-navbar-brand disabled>库房系统</b-navbar-brand>

    <!-- <b-navbar-toggle target="nav_collapse" /> -->

    <b-collapse is-nav id="nav_collapse">
      <b-navbar-nav>
        
        <b-nav-item href="/">统计</b-nav-item>
        <b-nav-item href="new">新货输入</b-nav-item>
        <b-nav-item href="in">入库</b-nav-item>
        <!-- <b-nav-item href="#" disabled>出库</b-nav-item> -->
        <b-nav-item href="out">出库</b-nav-item>
        <b-nav-item href="pending">待发货</b-nav-item>
      </b-navbar-nav>

    </b-collapse>
  </b-navbar>
</div>
   
</template>
