<template>
<div>
    <div id="container" style="width: 400px;height:320px;">
	</div>
	<Button v-show="isShowButton" class="moreCiyun" type="success" @click="getMoreCiyun">更多词云</Button> 
	
</div>
</template>

<script>
import echarts from 'echarts'
import "echarts-wordcloud/dist/echarts-wordcloud.js"
import "echarts-wordcloud/dist/echarts-wordcloud.min.js"

    export default {
        name: 'Cipin',
        data() {
            return {
				date:"2020-12-27",
				scale:1,
				isShowButton:false
            }
        },
        mounted(){
        //this.getCipin(this.date,this.scale);
        },
        methods: {

		getMoreCiyun(){
			window.open("http://epistory.deadpoetspoon.xyz/WordFrequency.html");
		},

        getCipin(val,newval){
			this.isShowButton = false;
		document.getElementById("container").removeAttribute("_echarts_instance_");
		var dom = document.getElementById("container");
		var myChart = echarts.init(dom);
		var app = {};
		var cipindata = new Array()
		var option = null;
		 option = {
			backgroundColor:'rgba(225, 225, 225, 0.8)', //rgba设置透明度
			//backgroundColor: '',
			title: {
				text: '热搜关键词',
				//left: 'center',
				left: '200px',
				//right:'0%',
				top: 10,
				textStyle: {
					color: '#000000'
				}
			},

			//animation:false,
			tooltip: {
				trigger: 'item',
				formatter: "{b} : {c}(权重) "
			},

			visualMap: {
				show: false,
				min: 600,
				max: 800,
				inRange: {
					//colorLightness: [0, 1]
				}
			},
			series: [
			{
			type: 'wordCloud',
				gridSize: 2,
				//animation:false,
				sizeRange: [10, 40],
				rotationRange: [-60, 60],
				shape: 'circle',
				textStyle: {
					normal: {
						color: function () {
							return 'rgb(' + [
									Math.round(Math.random() * 255),
									Math.round(Math.random() * 255),
									Math.round(Math.random() * 255)
								].join(',') + ')';
						}
					},
					emphasis: {
						shadowBlur: 10,
						shadowColor: ' #6495ED'
					},
				},
            left: "110px",
            top: "30px",
            //right: "0px",
            //bottom: null,
            //width: "200%",
            //height: "200%",
				data: cipindata,
				
			}
			]
		};
            //请求数据
        var requestOptions = {
            method: 'GET',
            redirect: 'follow'
		};
		var url;
		    if(newval == 1)
            url = new URL("http://pi.deadpoetspoon.xyz:7800/rscipin/?num=50&time="+val);
            else if(newval == 2)
            {
				console.log("进入了周词频");
            url = new URL("http://pi.deadpoetspoon.xyz:7800/rscipin/?week="+val+"&num=50");               
            }
            else if(newval == 3)
            {
            url = new URL("http://pi.deadpoetspoon.xyz:7800/rscipin/?week="+val+"&num=50");   	               
            }

		//fetch("http://pi.deadpoetspoon.xyz:7800/rscipin/?time=2020-3-15", requestOptions)
		//fetch("http://pi.deadpoetspoon.xyz:7800/rscipin/?num=50&time="+val, requestOptions)
		fetch(url,requestOptions)
            .then(response => response.json())
            .then(result => {
                result.forEach(rs => {
                    cipindata.push({name:rs.word,value:rs.weight})
				});
				    if(cipindata == 0)
                    {
                    	return;
					}
					else
					{
						this.isShowButton=true;
					}

                if (option && typeof option === "object") {
					myChart.setOption(option, true);
				}
            })
            .catch(error => console.log('error', error)); 
            }
        },
    }
</script>

<style lang="" scoped>
 #container{
  width: 30%;
  height: 50vh;
  display: inline-block;
  /*background-color: #ccc;
  opacity: 0.6;*/
  /*background-color:rgba(225, 225, 225, 0.8);*/
 }
   .moreCiyun{
	  position: absolute;
	  right:0px;
	  top:10px;
  }
</style>