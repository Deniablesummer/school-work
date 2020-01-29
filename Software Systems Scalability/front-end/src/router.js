import Vue from 'vue'
import Router from 'vue-router'
import Home from './views/Home.vue'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home
    },
    {
      path: '/sign-in',
      name: 'sign-in',
      component: () => import('./views/SignIn.vue')
    },
    {
      path: '/Add-Money',
      name: 'Add-Money',
      component: () => import('./views/AddMoney.vue')
    },
    {
      path: '/Buy-Stock',
      name: 'Buy-Stock',
      component: () => import('./views/BuyStock.vue')
    },
    {
      path: '/Set-Buy-Trigger',
      name: 'Set-Buy-Trigger',
      component: () => import('./views/SetBuyTrigger.vue')
    },
    {
      path: '/Set-Sell-Trigger',
      name: 'Set-Sell-Trigger',
      component: () => import('./views/SetSellTrigger.vue')
    },
    {
      path: '/Sell-Stock',
      name: 'Sell-Stock',
      component: () => import('./views/SellStock.vue')
    },
    {
      path: '/Profile-Summary',
      name: 'Profile-Summary',
      component: () => import('./views/ProfileSummary.vue')
    },
    {
      path: '/Cancel-Set-Buy-Trigger',
      name: 'Cancel-Set-Buy-Trigger',
      component: () => import('./views/CancelSetBuyTrigger.vue')
    }
    ,
    {
      path: '/Cancel-Set-Sell-Trigger',
      name: 'Cancel-Set-Sell-Trigger',
      component: () => import('./views/CancelSetSellTrigger.vue')
    },
    {
      path: '/Dumplog',
      name: 'Dumplog',
      component: () => import('./views/Dumplog.vue')
    }
  ]
})
