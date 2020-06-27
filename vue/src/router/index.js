import Vue from 'vue'
import Router from 'vue-router'
import HelloWorld from '@/components/HelloWorld'
import Map from '@/components/Map'
import Echarts from '@/components/Echarts'
import Cipin from '@/components/Cipin'
import Yiqing from '@/components/Yiqing'
Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'HelloWorld',
      component: HelloWorld
    },
    {
      path:'/Map',
      name:'Map',
      component:Map
    },
    {
      path:'/Echarts',
      name:'Echarts',
      component:Echarts
    },   
    {
      path:'/Cipin',
      name:'Cipin',
      component:Cipin
    },
    {
      path:'Yiqing',
      name:'Yiqing',
      component:Yiqing
    }
  ]
})
