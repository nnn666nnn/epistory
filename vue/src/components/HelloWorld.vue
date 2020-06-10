<template>
  <div class="hello">
   <!--
      <h1>{{ msg }}</h1>
    <h2>Essential Links</h2>
    <ul>
      <li>
        <a
          href="https://vuejs.org"
          target="_blank"
        >
          Core Docs
        </a>
      </li>
      <li>
        <a
          href="https://forum.vuejs.org"
          target="_blank"
        >
          Forum
        </a>
      </li>
      <li>
        <a
          href="https://chat.vuejs.org"
          target="_blank"
        >
          Community Chat
        </a>
      </li>
      <li>
        <a
          href="https://twitter.com/vuejs"
          target="_blank"
        >
          Twitter
        </a>
      </li>
      <br>
      <li>
        <a
          href="http://vuejs-templates.github.io/webpack/"
          target="_blank"
        >
          Docs for This Template
        </a>
      </li>
    </ul>
    <h2>Ecosystem</h2>
    <ul>
      <li>
        <a
          href="http://router.vuejs.org/"
          target="_blank"
        >
          vue-router
        </a>
      </li>
      <li>
        <a
          href="http://vuex.vuejs.org/"
          target="_blank"
        >
          vuex
        </a>
      </li>
      <li>
        <a
          href="http://vue-loader.vuejs.org/"
          target="_blank"
        >
          vue-loader
        </a>
      </li>
      <li>
        <a
          href="https://github.com/vuejs/awesome-vue"
          target="_blank"
        >
          awesome-vue
        </a>
      </li>
    </ul>
    -->
    <p>Why we do this</p>
    <Button type="success" >Success</Button>
    <div>
      <tag>时间滑动条</tag>
      <Slider v-model="value1" class="time" :step="mystep" show-tip="always" show-input></Slider>
      <Icon type="md-arrow-dropright-circle" @click="autoPlay" size="30"  />
      <Button type="primary" @click="stopPlay">停止播放</Button>
    </div>
    
    <Button type="primary" @click="toDay">日</Button>
    <Button type="primary" @click="toWeek">周</Button>
    <Button type="primary" @click="toMonth">月</Button>
    <p id="Realtime" v-show="isShowDate">Group9+value1</p>
    <!--a href="http://epistory.deadpoetspoon.xyz/HotSearchRange.html" 
    target="_blank">显示图表
    </a-->
    <iframe src="http://epistory.deadpoetspoon.xyz/HotSearchRange.html" frameborder="0" width="1200" height="300"></iframe>
  </div>
</template>

<script>
export default {
  name: 'HelloWorld',
  data () {
    return {
      msg: 'Welcome to Your Vue.js App',
      value1: 0,
      mystep:1,
      isShowDate:false
    }
  },
  methods:{
      toDay(){
        this.mystep=1;
      },
      toWeek(){
        this.mystep=7;
      },
      toMonth(){
        this.mystep=30;
      },
      dayAuto(){    //
        this.value1++; 
        document.getElementById("Realtime").innerText = "日期是: " + this.value1;
      },
      autoPlay(){
        this.$Message.info('自动播放中！');
        this.timer = setInterval(this.dayAuto, 1000); //循环执行函数dayAuto，value1++
        this.isShowDate = true;
        
        showDate();
      },
      showDate(){
        
        document.getElementById("Realtime").innerHtml = "日期是: " + this.value1;
      },
      stopPlay(){
        //document.getElementById("Realtime").innerHtml = "日期是: " + this.value1;
        clearInterval(this. timer);
        this.$Message.info('停了哦！');
      },

  },
  mounted() {

    },
    beforeDestroy() {
      //clearInterval(this.timer);
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1, h2 {
  font-weight: normal;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
p {
  font-size: 100px;
  color: blue;
}
.time{
  width: 50%;
  display: inline-block;
}
/*.hello{
  background:url("../assets/image/background.jpg");
  width:100%;			
  height:100%;			
  position:fixed;
  background-size:100% 100%;
}*/

</style>
