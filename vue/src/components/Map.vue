<template>
<div>
  <div id="mapDiv"></div>
  <Qingxu class = "qingxu" ref="myqingxu"/>
    <div class = "scaleButton">
      <Button id="hubei-button" type="primary" @click="mapToHubei" >湖北</Button>
      <Button id="province-button" type="primary" @click="mapToProvince">中国各省</Button>
      <Button id="china-button" type="primary" @click="mapToChina">中国</Button>
    </div>
    <img class="legend" src="http://epistory.deadpoetspoon.xyz/image/legend.jpg" alt="legend" style="width:14%">
    
</div>
</template>

<script>
import * as d3 from "d3"; //导入了d3库
import L from "leaflet"; //leaflet 库
import "leaflet/dist/leaflet.css";
//import 'jquery'
import $ from "jquery";
import Qingxu from  "./Qingxu"
export default {
  name: "Map",
  components:{
    Qingxu,
  },
  data() {
    return {
      MapName: "weiboEpiStory",
      mymap: null,
      myresult:null,
      countries:[],
      map:null,
      isLoadedGeojson:false,
      jsondata:null,
      geocoderrs:null,
      city:null,
      province:null,
      num:null,
      geocoder:null,
      zoomInButton:null,
      zoomOutButton:null,
      zoomOutButton2:null,
      newControl:null,
      hubeiresult:null,
      hubeicountries:[],
      wholecountries:[],
      scale:"province",
      val:null,
      newval:null,
      isQiehuan:false,
      suspect:null,
      heal:null,
      death:null,
      timeScale:"day"
    };
  },
  mounted() {
      this.map = new T.Map("mapDiv", {
      projection: "EPSG:4326"
      });
      document.getElementById("province-button").style.backgroundColor="#E1E100";
  },
  methods: {
  changewmj(){
          if(this.timeScale == "day")
            this.$refs.myqingxu.timeScale = "t";
          if(this.timeScale == "week")
            this.$refs.myqingxu.timeScale = "w";
          if(this.timeScale == "month")
            this.$refs.myqingxu.timeScale = "m";    
    this.$refs.myqingxu.init();
  },
    begin(val,newval) {
      this.val = val;
      this.newval = newval;
      //this.geocoder = new T.Geocoder();
      /*this.map = new T.Map("mapDiv", {
      projection: "EPSG:4326"
      });*/
      this.loadData(val,newval);
    },
    initResult(re){
        this.myresult = re;
        var that = this;
        if(this.isLoadedGeojson == false || this.isQiehuan == true)
        {
          this.isLoadedGeojson=true;
          var url;
          if(this.scale=="province")
          {
            url = new URL("http://epistory.deadpoetspoon.xyz/china.json");
          }
          if(this.scale == "hubei")
          {
            url = new URL("http://epistory.deadpoetspoon.xyz/hubei.json");
          }
          if(this.scale == "china")
          {
            url = new URL("http://epistory.deadpoetspoon.xyz/china(nosub).json");
          }
          d3.json(url).then(function(data){
          var T = require('T');
          that.jsondata  = data;
          that.countries = data.features;
          var countriesOverlay = new T.D3Overlay(that.init, that.redraw);
          that.map.clearOverLays();
          that.map.addOverLay(countriesOverlay); 
          that.isQiehuan = false;     
        });
        }
        else
        {
            var T = require('T');
            this.countries = this.jsondata.features;
            //console.log(that.countries+"???");
            var countriesOverlay = new T.D3Overlay(that.init, that.redraw);
            this.map.clearOverLays();
            this.map.addOverLay(countriesOverlay);
        }
         


    },
    loadData(val,newval) {
      
      //this.map=null;//走之前加了这个
      
      var T = require('T');
      this.countries = [];

      var result;

      /*this.map = new T.Map("mapDiv", {
        projection: "EPSG:4326"
      });*/
      
      if(this.scale == "province")
      {
      this.map.centerAndZoom(new T.LngLat(112.31667, 30.51667), 4);
      
      }
      if(this.scale == "china")
      this.map.centerAndZoom(new T.LngLat(112.27081, 32.53334), 4);      
      if(this.scale == "hubei")
      {
      this.map.centerAndZoom(new T.LngLat(113.24616, 31.07223),7);
      }

      this.map.enableDrag();
      this.map.removeEventListener("click",this.MapClick);
      this.map.addEventListener("click",this.MapClick);
      //this.map.removeEventListener("mousemove",this.MapClick);
      //this.map.addEventListener("mousemove",getmouseprovince);




      var requestOptions = {
        method: "GET",
        redirect: "follow"
      };
        var url;
      if(this.scale == "province")
      {
        if(newval == 1)
        {
            this.timeScale = "day";
            url = new URL("http://pi.deadpoetspoon.xyz:7800/yiqing/?time="+val+"&scalecode=s&datacode=ncshd");
        }
            else if(newval == 2)
            {
              this.timeScale = "week";
                var enddate = new Date(val);
                enddate.setDate(enddate.getDate()+7);
                enddate = enddate.toLocaleDateString().split('/').join('-');
            url = new URL("http://pi.deadpoetspoon.xyz:7800/yiqing/?begintime="+val+"&endtime="+enddate+"&scalecode=s&datacode=ncshd");               
            }
            else if(newval == 3)
            {   
                this.timeScale = "month";
                var enddate = new Date(val);
                enddate.setDate(enddate.getDate()+30);
                enddate = enddate.toLocaleDateString().split('/').join('-');
            url = new URL("http://pi.deadpoetspoon.xyz:7800/yiqing/?begintime="+val+"&endtime="+enddate+"&scalecode=s&datacode=ncshd");    	               
            }
      }
      if(this.scale == "hubei")
      {
            if(newval == 1)
            {
              this.timeScale = "day";
              url = new URL("http://pi.deadpoetspoon.xyz:7800/yiqing/?time="+val+"&scalecode=h&datacode=ncshd");
            }
            else if(newval == 2)
            {
                this.timeScale = "week";
                var enddate = new Date(val);
                enddate.setDate(enddate.getDate()+7);
                enddate = enddate.toLocaleDateString().split('/').join('-');
            url = new URL("http://pi.deadpoetspoon.xyz:7800/yiqing/?begintime="+val+"&endtime="+enddate+"&scalecode=h&datacode=ncshd");               
            }
            else if(newval == 3)
            {
                this.timeScale = "month";
                var enddate = new Date(val);
                enddate.setDate(enddate.getDate()+30);
                enddate = enddate.toLocaleDateString().split('/').join('-');
            url = new URL("http://pi.deadpoetspoon.xyz:7800/yiqing/?begintime="+val+"&endtime="+enddate+"&scalecode=h&datacode=ncshd");    	               
            }        
      }
      if(this.scale == "china")
      {
            if(newval == 1)
            {
              this.timeScale = "day";
              url = new URL("http://pi.deadpoetspoon.xyz:7800/yiqing/?time="+val+"&scalecode=z&datacode=ncshd");
            }
            else if(newval == 2)
            {
                this.timeScale = "week";
                var enddate = new Date(val);
                enddate.setDate(enddate.getDate()+7);
                enddate = enddate.toLocaleDateString().split('/').join('-');
            url = new URL("http://pi.deadpoetspoon.xyz:7800/yiqing/?begintime="+val+"&endtime="+enddate+"&scalecode=z&datacode=ncshd");               
            }
            else if(newval == 3)
            {
                this.timeScale = "month";
                var enddate = new Date(val);
                enddate.setDate(enddate.getDate()+30);
                enddate = enddate.toLocaleDateString().split('/').join('-');
            url = new URL("http://pi.deadpoetspoon.xyz:7800/yiqing/?begintime="+val+"&endtime="+enddate+"&scalecode=z&datacode=ncshd");    	               
            }        
      }

      fetch(
        //"http://pi.deadpoetspoon.xyz:7800/yiqing/?time=2020-02-01&scalecode=s&datacode=ac",
        url,
        requestOptions
      )
        .then(response => response.json())
        .then(re => this.initResult(re))
        .catch(error => console.log("error", error));
    },

    init(sel, transform) {
      var that = this;
      //var T = require("T");
      var upd=sel.selectAll("path.geojson").data(this.countries);

      upd.enter()
        .append("path")
        .attr("class", "geojson")
        .attr("stroke", "black")
        .attr("fill", function(d, i) {
          var ree = d3.rgb(255, 255, 255);
          that.myresult.forEach(rs => {
            if (rs.name == d.properties.name) {
              var color = that.getColor(rs.confirmed);
              ree = d3.rgb(color[0], color[1], color[2]);
            }
          });
          return ree;
        })
        //.attr("fill-opacity", "0.8");
        .attr("fill-opacity", "0.8")
        .on(onmousemove=function(e){
          if(cityname !== undefined)
            {
              if(that.scale=="china")
              cityname='中国';
              upd.attr('fill-opacity',function (d, i){
              if(cityname == d.properties.name){
                    return '1.0';
                      }
                      else{return '0.4';}
                    }).attr('stroke', function (d, i){
                    if(cityname == d.properties.name){
                              return 'white';
                            }
                            else{return 'black';}
                    })
                    }
        
                  });
                  var cityname,provincename;
                  that.map.removeEventListener("mousemove",getmouseprovince);
                  that.map.addEventListener("mousemove",getmouseprovince);
                  function getmouseprovince(e){
                     var geocoder = new T.Geocoder();
                    geocoder.getLocation(e.lnglat,getmouseprovince2);
                  }
                  function getmouseprovince2(result){
                    var addressComponent = result.getAddressComponent();
                    if(that.scale=="hubei")
                    cityname=addressComponent.city;
                    if(that.scale=="province")
                    {
                            var city=addressComponent.city;
                            var administrative = new T.AdministrativeDivision();
                            var config = {
                              needSubInfo: true,
                              needAll: true,
                              needPolygon: true,
                              needPre: true,
                              searchType: 1,
                              searchWord: city
                            };
                            administrative.search(config, getmouseprovince3);
                    }    
                  }

                  function getmouseprovince3(result){
                    if(result.getStatus() == 100) 
                  {
                    
                    var data = result.getData();
                    for(var i = 0; i < data.length; i++){
                      if(data[i].parents.province !== undefined){   
                      cityname = data[i].parents.province.name;
                      }
                      else {
                        cityname = data[i].name;
                  }}}
                      //console.log(provincename);
                  }
                 /* .on("click", function(d,i){  
                      console.log("谭骏翊");
                  } )  */
    },
    redraw(sel, transform) {
      //var T = require("T");
      sel.selectAll("path.geojson").each(function(d, i) {
        d3.select(this).attr("d", transform.pathFromGeojson);
      });
    },

    getColor(value) {
      if (value <= 90000 && value > 80000) return [47, 0, 0];
      else if (value <= 80000 && value > 70000) return [77, 0, 0];
      else if (value <= 70000 && value > 60000) return [96, 0, 0];
      else if (value <= 60000 && value > 50000) return [117, 0, 0];
      else if (value <= 50000 && value > 40000) return [147, 0, 0];
      else if (value <= 40000 && value > 30000) return [174, 0, 0];
      else if (value <= 30000 && value > 20000) return [206, 0, 0];
      else if (value <= 20000 && value > 10000) return [234, 0, 0];
      else if (value <= 10000 && value > 5000) return [255, 0, 0];
      else if (value <= 5000 && value > 2500) return [255, 45, 45];
      else if (value <= 2500 && value > 1000) return [255, 81, 81];
      else if (value <= 1000 && value > 500) return [255, 117, 117];
      else if (value <= 500 && value > 250) return [255, 151, 151];
      else if (value <= 250 && value > 100) return [255, 181, 181];
      else if (value <= 100 && value > 50) return [255, 210, 210];
      else if (value <= 50 && value != 0) return [255, 236, 236];
      else return [255, 255, 255];
    },

    MapClick(e)
    {

      var geocoder=new T.Geocoder();
      //this.geocoderrs=this.geocoder.getLocation(e.lnglat,this.searchResult);
      //var geocoderrs = geocoder.getLocation(e.lnglat,this.searchResult);
      geocoder.getLocation(e.lnglat,this.searchResult);
    },

    searchResult(result)
  {
    var addressComponent = result.getAddressComponent();
    this.city=addressComponent.city;
    var administrative = new T.AdministrativeDivision();
		var config = {
			needSubInfo: true,
			needAll: true,
			needPolygon: true,
			needPre: true,
			searchType: 1,
			searchWord: this.city
		};
    administrative.search(config, this.searchResult2);
  },

  searchResult2(result2)
	{
		if(result2.getStatus() == 100) 
		{
       var name1;var placename;
			var data = result2.getData();
      for(var i = 0; i < data.length; i++){
        if(data[i].parents.province !== undefined){
        
        this.province = data[i].parents.province.name;

        
        if(this.scale == "province")
        {
          name1 = this.province;
          placename = this.province;
        //传时间尺度
          console.log(this.timeScale+"wmj");
          if(this.timeScale == "day")
            this.$refs.myqingxu.timeScale = "t";
          if(this.timeScale == "week")
            this.$refs.myqingxu.timeScale = "w";
          if(this.timeScale == "month")
            this.$refs.myqingxu.timeScale = "m";
        //传空间
          var r=/[^\x00-\xff]/g;
          var tjy
          var sub=function(str,n){
          if(str.replace(r,"mm").length<=2*n){return str;}
          var m=Math.floor(n);
          for(var i=m;i<str.length;i++){
          if(str.substr(0,i).replace(r,"mm").length>=2*n){
          return str.substr(0,i);
        }
        }
        return str;
        }

          if(name1 == "黑龙江省"||name1 == "内蒙古自治区")
          {
            tjy=sub(name1,3);
          }
          else
          {
            tjy=sub(name1,2);
          }
          this.$refs.myqingxu.space = tjy;

          this.$refs.myqingxu.changeSpanText();
          this.$refs.myqingxu.init();
          //this.$refs.myqingxu.document.getElementById("qingxu-button").innerText = "打开"+tjy+"情绪图";
        }
        if(this.scale == "hubei")
        {
          name1 = this.city;
          placename= this.city;
        }
        if(this.scale =="china")
        {
          name1 = "中国";
          placename= "中国";
        }
        this.myresult.forEach(rs => {
                    	//if(rs.name == this.province){   
                        if(rs.name == name1){  	
                          this.num = rs.confirmed;
                          this.suspect = rs.suspected;
                          this.heal = rs.cured;
                          this.death = rs.dead;
                      }
               		 });
    //console.log(province); 
    
    var infowin=new T.InfoWindow("所在地："+placename+"<br>"+"累计确诊人数："+this.num+'<br>'+'疑似病例：'+this.suspect+'<br>'+ '治愈人数：'+this.heal+'<br>'+'死亡人数：'+this.death );
    this.map.openInfoWindow(infowin, new T.LngLat(data[i].lnt,data[i].lat)) ;
        }
        else {
          this.province = data[i].name;
          this.myresult.forEach(rs => {
                    	if(rs.name == name1){   	
                          this.num = rs.confirmed;
                          this.suspect = rs.suspected;
                          this.heal = rs.cured;
                          this.death = rs.dead;
                      }
               		 });
    //console.log(province); 
    var infowin=new T.InfoWindow("所在地："+placename+"<br>"+"累计确诊人数："+this.num+'<br>'+'疑似病例：'+this.suspect+'<br>'+ '治愈人数：'+this.heal+'<br>'+'死亡人数：'+this.death );

    this.map.openInfoWindow(infowin, new T.LngLat(data[i].lnt,data[i].lat)) ;
        }
      }
		}
  },
  mapToHubei(){
    
    this.scale = "hubei";
    //this.begin(this.val,this.newval);
    this.isQiehuan = true;
    this.begin(this.val,this.newval);
        document.getElementById("hubei-button").style.backgroundColor="#E1E100";
        document.getElementById("province-button").style.backgroundColor=null;
        document.getElementById("china-button").style.backgroundColor=null;

        //this.$emit("sendScale",this.scale);
        this.$parent.getScale("hubei");
    
  },

    mapToChina(){
      //this.map = null;
    this.scale = "china";
    this.isQiehuan = true;
    this.loadData(this.val,this.newval);
         document.getElementById("hubei-button").style.backgroundColor=null;
        document.getElementById("province-button").style.backgroundColor=null;
        document.getElementById("china-button").style.backgroundColor="#E1E100";
        this.$parent.getScale("china");
    //this.map.clearOverLays();
  },

    mapToProvince(){
      //this.map = null;
    this.scale = "province";
    this.isQiehuan = true;
    this.loadData(this.val,this.newval);
        document.getElementById("hubei-button").style.backgroundColor=null;
        document.getElementById("province-button").style.backgroundColor="#E1E100";
        document.getElementById("china-button").style.backgroundColor=null;
        this.$parent.getScale("province");
    //this.map.clearOverLays();
  },



  

  

  }
};
</script>

<style lang="" scoped>
#mapDiv {
  width: 219vh;
  height: 97.5vh;
  display: inline-block;
  padding: 0px;
  z-index:0;
}
.scaleButton{
  
  position:absolute;
  top:15px;
  right:630px;
  z-index:4;
}
.qingxu{
  position:absolute;
  top:100px;
  left:330px;
  z-index:4;
}
.legend{
  position:absolute;
  bottom:0px;
  left:330px;
  z-index:4;
  opacity: 0.8;
}

</style>