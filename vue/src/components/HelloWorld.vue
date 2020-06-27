<template>
  <div class="hello" style="height:97.5px" >
    <!--Button type="success" >Success</Button-->
    <img src="../image/welcome.png" alt="welcome" class="welcome" style="width:100%;height:97.5vh" v-if="isShowWelcome" @click="hideImage">
    <div>
      <Tag id="mytag" color="cyan" size = "large">时间滑动条</Tag>
      <Slider v-model="value1" class="time" :step="mystep" show-tip="always" :min=1 :max=160 :tip-format="showformat" @on-change="up" :marks="mymarks" ></Slider>
      <!--Icon type="md-arrow-dropright-circle" @click="autoPlay" size="30"  /-->
      <div class = "mybutton">
        <Button type="default" @click="autoPlay" id="autoPlay">播放</Button>
        <Button type="default" @click="stopPlay">停止播放</Button>
        <Button type="info" @click="toDay" id="dayButton" style="margin-left:30px">日</Button>
        <Button type="info" @click="toWeek" id="weekButton">周</Button>
        <Button type="info" @click="toMonth" id="monthButton">月</Button>
      </div>
      <!--Modal id="myDialog" v-show="this.isShowDialog"
        v-model="modal1"
        v-bind:title="myDialogTitle">
        <p id="myDialogContent"></p> 
        <img src="../image/1.jpg" alt="heihei" id="myimage" style="width:100%">       
      </Modal-->
    
      <!--Map id="mymap" ref=""></Map-->
      <!--Echarts id="myecharts">what2</Echarts-->
      <div class = "buju">
          <Cipin class="cipin" ref="mycipin"/>
          <Map ref="mymap" class="map" /> 
          <Echarts ref="myecharts" class="echarts"/>
          <Yiqing class = "yiqing" ref="myyiqing"/>
          
      </div> 
      
    </div>
  </div>
</template>

<script>
//import Echart from ' ./map'
import Map from "./Map";
import Echarts from "./Echarts"
import Cipin from "./Cipin"
import Yiqing from "./Yiqing"

export default {
  name: 'HelloWorld',
  components:{
    Map,
    Echarts,
    Cipin,
    Yiqing,
  },
  data () {
    return {
      msg: 'Welcome to Your Vue.js App',
      isShowWelcome:"true",
      value1: 1,
      mystep:1,
      isShowDate:false,
      isAutoPlay:false,
      myDate:"2019-12-27",
      timeScale:"day",
      mymarks: {
          1:{
            style:{
                color: '#000000',                
            },
            label: this.$createElement('strong', '第一阶段'),
            
          },
          24: {
            style:{
                color: '#000000',                
            },
            label: this.$createElement('strong', '第二阶段'),
            
          },
          56: {
            style:{
                color: '#000000',                
            },
            label: this.$createElement('strong', '第三阶段'),
            
          },
          82: {
            style:{
                color: '#000000',                
            },
            label: this.$createElement('strong', '第四阶段'),
            
          },
          124: {
            style:{
                color: '#000000',                
            },
            label: this.$createElement('strong', '第五阶段'),
            
          },
      },

    }
  },

      
  mounted(){
            this.showDate();
            if(this.timeScale == "day")
            {
              this.changeEcharts(this.myDate,1);//日尺度
              this.changeCipin(this.myDate,1);
              this.changeEpiNumMap(this.myDate,1);
              this.changeYiqing1(this.myDate);
              document.getElementById("dayButton").style.backgroundColor="orange";
            }
  },
  methods:{
      getScale(data){
          console.log(data+"咩咩咩咩");
          this.$refs.myyiqing.scale=data;
          this.$refs.myyiqing.changedate(this.myDate);
          this.$refs.myyiqing.changeDates(this.myDate,this.timeScale);
          this.$refs.myyiqing.update();
      },
      toDay(){
        document.getElementById("mytag").innerText =  this.myDate;
        this.$refs.mymap.timeScale="day";
        //this.$refs.mymap.changeQingxu();
        this.$refs.mymap.changewmj();
        this.mystep=1;
        this.timeScale = "day";
        document.getElementById("dayButton").style.backgroundColor="orange";
        document.getElementById("weekButton").style.backgroundColor=null;
        document.getElementById("monthButton").style.backgroundColor=null;
        
        this.$refs.myyiqing.timeScale="day";
        if(this.isAutoPlay == true)
        {
          //clearInterval(this. timer); 
          this.autoPlay();
        }
        
      },
      toWeek(){
        var enddate = new Date(this.myDate);
        enddate.setDate(enddate.getDate()+7);
        enddate = enddate.toLocaleDateString().split('/').join('-');
        document.getElementById("mytag").innerText =  this.myDate+"——"+enddate;
        this.$refs.mymap.timeScale="week";
        //this.$refs.mymap.changeQingxu();
        this.$refs.mymap.changewmj();
        this.mystep=7;
        this.timeScale = "week";
        document.getElementById("dayButton").style.backgroundColor=null;
        document.getElementById("weekButton").style.backgroundColor="orange";
        document.getElementById("monthButton").style.backgroundColor=null;
        
        
        this.$refs.myyiqing.showZhuzhuang = false;
        this.$refs.myyiqing.update1();
        this.$refs.myyiqing.timeScale="week";
      },
      toMonth(){
        var enddate = new Date(this.myDate);
        enddate.setDate(enddate.getDate()+30);
        enddate = enddate.toLocaleDateString().split('/').join('-');
        document.getElementById("mytag").innerText =  this.myDate+"——"+enddate;
        this.$refs.mymap.timeScale="month";
        //this.$refs.mymap.changeQingxu();
        this.$refs.mymap.changewmj();
        this.mystep=30;
        this.timeScale = "month";
        document.getElementById("dayButton").style.backgroundColor=null;
        document.getElementById("weekButton").style.backgroundColor=null;
        document.getElementById("monthButton").style.backgroundColor="orange";
        
         
         this.$refs.myyiqing.showZhuzhuang = false;
         this.$refs.myyiqing.update1();
         this.$refs.myyiqing.timeScale="month";
      },
      dayAuto(){    //
        //this.value1++;  
        this.value1=this.value1+this.mystep;     
        //document.getElementById("Realtime").innerText = "日期是: " + this.myDate;
      },
      weekAuto(){
        //this.value1+=7; 
        this.value1=this.value1+this.mystep;
      },
      monthAuto(){
        //this.value1+=30; 
        this.value1=this.value1+this.mystep;
      },
      autoPlay(){
        document.getElementById("autoPlay").style.backgroundColor="lightgreen";
        if(this.isAutoPlay == true)
         return ;
        this.$Message.info('自动播放中！');
        if(this.timeScale == "day")
        this.timer = setInterval(this.dayAuto, 4000); //循环执行函数dayAuto，value1++
        else if(this.timeScale == "week")
        this.timer = setInterval(this.weekAuto, 4000); //循环执行函数weekAuto
        else if(this.timeScale == "month")
        this.timer = setInterval(this.monthAuto, 4000); //循环执行函数weekAuto
        /*if(this.value1==160)
        clearInterval(this. timer);*/
        this.isShowDate = true;
        this.isAutoPlay = true;
        
        //showDate();
      },
      showDate(){
        if(this.timeScale == "day")
        {
          
          document.getElementById("mytag").innerText =  this.myDate;
        }
        if(this.timeScale == "week")
          {

          var enddate = new Date(this.myDate);
          enddate.setDate(enddate.getDate()+7);
          enddate = enddate.toLocaleDateString().split('/').join('-');
          document.getElementById("mytag").innerText =  this.myDate+"——"+enddate;
          }
        if(this.timeScale == "month")
          {

          var enddate = new Date(this.myDate);
          enddate.setDate(enddate.getDate()+30);
          enddate = enddate.toLocaleDateString().split('/').join('-');
          document.getElementById("mytag").innerText =  this.myDate+"——"+enddate;
          }
      },
      stopPlay(){
        document.getElementById("autoPlay").style.backgroundColor=null;
        clearInterval(this. timer);
        this.$Message.info('停了哦！');
        this.isAutoPlay = false;
      },
      //监听到value1变化改变对应图表
      changeEcharts(val,newval){
        this.$refs.myecharts.changeDate(val,newval);
      },

      showformat(){
        if(this.value1>0)
        {
          if(this.timeScale == "day")
          return "第"+this.value1+"天";
          else if(this.timeScale == "week")
          return "第"+Math.floor(this.value1/7+1)+"周";
          else if(this.timeScale == "month")
          return "第"+Math.floor(this.value1/30+1)+"个月"; //取整数
        }
          else
          return null;
      },

      changeValtoDate(){
            var x = this.value1;
            var date = new Date("2019-12-27");
      
            if(x<=5&&x>=1){
              date.setDate(x+26); 
            }
            else if(x<=36){
              date.setFullYear(2020);
              date.setMonth(0);
              date.setDate(x-5);
            }
            else if(x<=65){
              date.setFullYear(2020);
              date.setMonth(1);
              date.setDate(x-36);
            }
            else if(x<=96){
              date.setFullYear(2020);
              date.setMonth(2);
              date.setDate(x-65);
            }
            else if(x<=126){
              date.setFullYear(2020);
              date.setMonth(3);
              date.setDate(x-96);
            }
            else if(x<=157){
              date.setFullYear(2020);
              date.setMonth(4);
              date.setDate(x-126);
            }
            else if(x<=160){
              date.setFullYear(2020);
              date.setMonth(5);
              date.setDate(x-157); 
            }
            //console.log(date+"wmj");
            date = date.toLocaleDateString().split('/').join('-');
            this.myDate = date;
            //this.changeEcharts(date);      
      },
      //鼠标抬起才显示图
      up(){
            this.changeValtoDate();
            //this.changeEcharts(this.myDate);
      },
      changeCipin(val,newval)
      {
        this.$refs.mycipin.getCipin(val,newval);
      },
      changeEpiNumMap(val,newval)
      {
        /*if(this.timeScale == "day")
          this.$refs.mymap.timeScale="t";
        if(this.timeScale == "week")
          this.$refs.mymap.timeScale="w";
        if(this.timeScale == "month")
          this.$refs.mymap.timeScale="m";*/
        this.$refs.mymap.begin(val,newval);
      },
      changeYiqing1(val){  //饼图
        this.$refs.myyiqing.changedate(val);
      },
      changeYiqing2(val1,val2){
        this.$refs.myyiqing.changeDates(val1,val2);
      },
      hideImage(){
        this.isShowWelcome = false;
      }

  },

    watch:{
      //监测滑块变化
      　//value1(curVal,oldVal){this.value1
        value1:{
          handler:function(curVal,oldVal){
            //先显示对话框
            if(curVal == 1 ){
                    clearInterval(this. timer);
                    //this.isAutoPlay = false;
                    this.$Modal.info({
                    title: '第一阶段：迅即应对突发疫情',
                    content: '<p>&nbsp; &nbsp; &nbsp; &nbsp;湖北省武汉市监测发现不明原因肺炎病例，中国第一时间报告疫情，迅速采取行动，开展病因学和流行病学调查，阻断疫情蔓延。及时主动向世界卫生组织以及美国等国家通报疫情信息，向世界公布新型冠状病毒基因组序列。武汉地区出现局部社区传播和聚集性病例，其他地区开始出现武汉关联确诊病例，中国全面展开疫情防控。</p>  <img src="http://epistory.deadpoetspoon.xyz/image/1.jpg" alt="heihei" id="myimage" style="width:100%">',
                    onOk: () => {
                      if(this.isAutoPlay ==true)
                      {
                              if(this.timeScale == "day")
                                this.timer = setInterval(this.dayAuto, 4000); //循环执行函数dayAuto，value1++
                                else if(this.timeScale == "week")
                                this.timer = setInterval(this.weekAuto, 4000); //循环执行函数weekAuto
                                else if(this.timeScale == "month")
                                this.timer = setInterval(this.monthAuto, 4000); //循环执行函数weekAuto
                                this.isAutoPlay = true;
                      }
                    },
                    width:"500px"
                });
            }
            if(curVal == 24||(this.timeScale=="week"&&curVal>=24&&curVal<31)||(this.timeScale=="month"&&curVal>=24&&curVal<54)){
                    clearInterval(this. timer);
                    //this.isAutoPlay = false;
                    this.$Modal.info({
                    title: '第二阶段：初步遏制疫情蔓延势头',
                    content: '<p>&nbsp; &nbsp; &nbsp; &nbsp;全国新增确诊病例快速增加，防控形势异常严峻。中国采取阻断病毒传播的关键一招，坚决果断关闭离汉离鄂通道，武汉保卫战、湖北保卫战全面打响。中共中央成立应对疫情工作领导小组，并向湖北等疫情严重地区派出中央指导组。国务院先后建立联防联控机制、复工复产推进工作机制。全国集中资源和力量驰援湖北省和武汉市。各地启动重大突发公共卫生事件应急响应。最全面最严格最彻底的全国疫情防控正式展开，疫情蔓延势头初步遏制。</p>  <img src="http://epistory.deadpoetspoon.xyz/image/2.jpg" alt="heihei" id="myimage" style="width:100%">',
                    onOk: () => {
                      if(this.isAutoPlay ==true)
                      {
                              if(this.timeScale == "day")
                                this.timer = setInterval(this.dayAuto, 4000); //循环执行函数dayAuto，value1++
                                else if(this.timeScale == "week")
                                this.timer = setInterval(this.weekAuto, 4000); //循环执行函数weekAuto
                                else if(this.timeScale == "month")
                                this.timer = setInterval(this.monthAuto, 4000); //循环执行函数weekAuto
                                this.isAutoPlay = true;
                      }
                    },
                    width:"500px"
                });
            }
            if(curVal == 56||(this.timeScale=="week"&&curVal>=56&&curVal<63)||(this.timeScale=="month"&&curVal>=56&&curVal<86)){
                    clearInterval(this. timer);
                    //this.isAutoPlay = false;
                    this.$Modal.info({
                    title: '第三阶段：本土新增病例数逐步下降至个位数',
                    content: '<p>&nbsp; &nbsp; &nbsp; &nbsp;湖北省和武汉市疫情快速上升势头均得到遏制，全国除湖北省以外疫情形势总体平稳，3月中旬每日新增病例控制在个位数以内，疫情防控取得阶段性重要成效。根据疫情防控形势发展，中共中央作出统筹疫情防控和经济社会发展、有序复工复产重大决策。</p>  <img src="http://epistory.deadpoetspoon.xyz/image/3.jpg" alt="heihei" id="myimage" style="width:100%" >   ',
                    onOk: () => {
                      if(this.isAutoPlay ==true)
                      {
                              if(this.timeScale == "day")
                                this.timer = setInterval(this.dayAuto, 4000); //循环执行函数dayAuto，value1++
                                else if(this.timeScale == "week")
                                this.timer = setInterval(this.weekAuto, 4000); //循环执行函数weekAuto
                                else if(this.timeScale == "month")
                                this.timer = setInterval(this.monthAuto, 4000); //循环执行函数weekAuto
                                this.isAutoPlay = true;
                      }
                    },
                    width:"500px"
                });
            }
            if(curVal == 82||(this.timeScale=="week"&&curVal>=82&&curVal<89)||(this.timeScale=="month"&&curVal>=82&&curVal<112)){
                    clearInterval(this. timer);
                    //this.isAutoPlay = false;
                    this.$Modal.info({
                    title: '第四阶段：取得武汉保卫战、湖北保卫战决定性成果',
                    content: '<p>&nbsp; &nbsp; &nbsp; &nbsp;以武汉市为主战场的全国本土疫情传播基本阻断，离汉离鄂通道管控措施解除，武汉市在院新冠肺炎患者清零，武汉保卫战、湖北保卫战取得决定性成果，全国疫情防控阻击战取得重大战略成果。境内疫情零星散发，境外疫情快速扩散蔓延，境外输入病例造成关联病例传播。中共中央把握疫情形势发展变化，确定了“外防输入、内防反弹”的防控策略，巩固深化国内疫情防控成效，及时处置聚集性疫情，分类推动复工复产，关心关爱境外中国公民。</p>  <img src="http://epistory.deadpoetspoon.xyz/image/4.jpg" alt="heihei" id="myimage" style="width:100%" >   ',
                    onOk: () => {
                      if(this.isAutoPlay ==true)
                      {
                              if(this.timeScale == "day")
                                this.timer = setInterval(this.dayAuto, 4000); //循环执行函数dayAuto，value1++
                                else if(this.timeScale == "week")
                                this.timer = setInterval(this.weekAuto, 4000); //循环执行函数weekAuto
                                else if(this.timeScale == "month")
                                this.timer = setInterval(this.monthAuto, 4000); //循环执行函数weekAuto
                                this.isAutoPlay = true;
                      }
                    }, 
                    width:"500px"
                });              
            }
            if(curVal == 124||(this.timeScale=="week"&&curVal>=124&&curVal<131)||(this.timeScale=="month"&&curVal>=124&&curVal<154)){
                    clearInterval(this. timer);
                    //this.isAutoPlay = false;
                    this.$Modal.info({
                    title: '第五阶段：全国疫情防控进入常态化',
                    content: '<p>&nbsp; &nbsp; &nbsp; &nbsp;境内疫情总体呈零星散发状态，局部地区出现散发病例引起的聚集性疫情，境外输入病例基本得到控制，疫情积极向好态势持续巩固，全国疫情防控进入常态化。加大力度推进复工复产复学，常态化防控措施经受“五一”假期考验。经中共中央批准，国务院联防联控机制派出联络组，继续加强湖北省疫情防控。</p>  <img src="http://epistory.deadpoetspoon.xyz/image/5.jpg" alt="heihei" id="myimage" style="width:100%" >   ',
                    onOk: () => {
                      if(this.isAutoPlay ==true)
                      {
                              if(this.timeScale == "day")
                                this.timer = setInterval(this.dayAuto, 4000); //循环执行函数dayAuto，value1++
                                else if(this.timeScale == "week")
                                this.timer = setInterval(this.weekAuto, 4000); //循环执行函数weekAuto
                                else if(this.timeScale == "month")
                                this.timer = setInterval(this.monthAuto, 4000); //循环执行函数weekAuto
                                this.isAutoPlay = true;
                      }
                    },
                    width:"500px"
                });
            }


            if(this.timeScale=="day"&&curVal == 160){
            clearInterval(this. timer);
            this.isAutoPlay =false;
            document.getElementById("autoPlay").style.backgroundColor=null;
            this.$Message.info({content:'已经到最后一天啦！',duration: 5});
            }
            else if(this.timeScale=="week"&&curVal>153&&curVal<=160){
            clearInterval(this. timer);
            this.isAutoPlay =false;
            this.$Message.info({content:'已经到最后一周啦！',duration: 5}); 
            document.getElementById("autoPlay").style.backgroundColor=null; 
            }
            else if(this.timeScale=="month"&&curVal>130&&curVal<=160){
            clearInterval(this. timer);
            this.isAutoPlay =false;
            this.$Message.info({content:'已经到最后一月啦！',duration: 5});  
            document.getElementById("autoPlay").style.backgroundColor=null;           
            }
            this.changeValtoDate();
            this.isShowDate = true;
            this.showDate();
            //if(this.isAutoPlay == true)
            if(this.timeScale == "day")
            {
              this.changeEcharts(this.myDate,1);//日尺度
              this.changeCipin(this.myDate,1);
              this.changeEpiNumMap(this.myDate,1);
              this.changeYiqing1(this.myDate);
            }
            else if(this.timeScale == "week")
            {
              this.changeEcharts(this.myDate,2);//周尺度
              this.changeCipin(Math.floor(this.value1/7+1),2);
              this.changeEpiNumMap(this.myDate,2);
              this.changeYiqing2(this.myDate,"week");
              this.changeYiqing1(this.myDate);

            }
            else if(this.timeScale == "month")
            {
              this.changeEcharts(this.myDate,3);   //月尺度   
              this.changeCipin(Math.floor(this.value1/30+1),3);
              this.changeEpiNumMap(this.myDate,3); 
              this.changeYiqing2(this.myDate,"month");
              this.changeYiqing1(this.myDate);
            }   
          },

　　　　}
    },

    beforeDestroy() {
      //clearInterval(this.timer);
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
/*h1{
  background-color: #f1f1f1;
  padding: 20px;
  margin-top: -60px;
  text-align: center;
}*/
/*p {
  font-size: 30px;
  color: blue;
}*/
.class{
  overflow:hidden;
}
.time{
  position: absolute;
  top:40px;
  left:200px;
  width: 70%;
  z-index: 2;
  margin: auto;
}
.mybutton{
  position: absolute;
  top:15px;
  left:300px;
  /*margin-left: 100px;
  display: inline-block;*/
  z-index: 2;
}
/* 背景为黄色 */

/*p{
  display:inline-block;
}*/
.cipin{
  position: absolute;
  z-index: 3;
  left: -105px;
  top:390px;
}
.map{
  position: absolute;
  z-index: 1;
  top:0px;
  left: -5vh;
  /*margin: 30px;*/
  /*margin-top: 30px;*/
}
.echarts{
  position: absolute;
  z-index: 3;
  right: 0px;
  top:360px;
}
.yiqing{
position: absolute;
z-index: 2;
left:-150px;
top:100px;
}
#mytag{
  position: absolute;
  left:20px;
  top:40px;
  /*margin-right: 50px;*/
  z-index:2;
}
#myDialogContent{
  font-size: 15px;
}
.welcome{
  position: absolute;
  top:0px;
  left:0px;
  z-index: 4;
  
}
</style>
