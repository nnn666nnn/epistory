<template>
<div>  
    <div id="main" style="width: 500px;height:350px;"></div> 
    <Button v-show="isShowButton" class="more" type="success" @click="getMoreWeibo">更多热搜</Button> 
    
</div>
</template>

<script >
    import echarts from 'echarts'
    
    export default {
        name: 'Echarts',
        data () {
            return {
                titleText:"单日微博热搜排行榜",
                lengendData:"单日最高热搜排名",
                xAxisName:"排名",
                isShowButton:false,
            }
        },
        methods:{
            getMoreWeibo(){
                window.open("http://epistory.deadpoetspoon.xyz/HotSearchMore.html");
            },
            changeDate(val,newval) {
            //echarts.init(document.getElementById('main')).clear();
            this.isShowButton = false;
            var myChart = echarts.init(document.getElementById('main'));
            document.getElementById("main").removeAttribute("_echarts_instance_");
            //var time = document.getElementById("Date").value;
            // 获取json中元素下标
            //  arr: 传入的数组
            //  obj: 需要获取下标的元素
            function getArrayIndex(arr, obj) {
                var i = arr.length;
                //当i为0时，循环会跳出
                while (i--) {
                    if (arr[i] === obj) {
                        return i
                    }
                }
                return -1
            }


            //构造变量
            var keyword = new Array(); //热搜
            var searchNum = new Array(); //搜索数
            var link = new Array(); //热搜链接
            var rank = new Array(); //最高排名
            var tttime = new Array(); //最高排名
            // 基于准备好的dom，初始化echarts实例

            var myColor = ['#ecbbbc', '#e7a7a9', '#e19395', '#db7f81', '#d66b6e', '#d0575a', '#ca4346', '#bf3539', //颜色数组
                '#ab3033', '#972a2d'
            ]    
            //请求数据
            var requestOptions = {
                method: 'GET',
                redirect: 'follow'
            };
            var url;
            if(newval == 1)
            {
            url = new URL("http://pi.deadpoetspoon.xyz:7800/resou/?datacode=lkrs&time=" + val + "\&num=10");
                this.titleText="本日微博热搜排行榜";
                this.lengendData="本日最高热搜排名";
                this.xAxisName="排名";
            }
            else if(newval == 2)
            {
                var enddate = new Date(val);
                enddate.setDate(enddate.getDate()+7);
                enddate = enddate.toLocaleDateString().split('/').join('-');
                //myColor = ['#dbffdb','#d1ffd1','#c6ffc6','#bcffbc','#b7ffb7','#adffad','#a3ffa3','#99ff99','#8eff8e','#84ff84'];
            url = new URL("http://pi.deadpoetspoon.xyz:7800/resou/?datacode=lkrst&begintime="+val+"&endtime="+enddate+"&num=10");
                this.titleText="本周微博热搜排行榜";
                this.lengendData="本周最高热搜排名";
                this.xAxisName="排名";
            }
            else if(newval == 3)
            {
                var enddate = new Date(val);
                enddate.setDate(enddate.getDate()+30);
                enddate = enddate.toLocaleDateString().split('/').join('-');
            url = new URL("http://pi.deadpoetspoon.xyz:7800/resou/?datacode=lkrst&begintime="+val+"&endtime="+enddate+"&num=10");
                this.titleText="本月微博热搜排行榜";
                this.lengendData="本月最高热搜排名";
                this.xAxisName="排名";
                //myColor = ['#ff7f7f','#ff7fbf','#ff7fff','#bf7fff','#7f7fff','#7fbfff','#7fffff','#7fffbf','#7fff7f','#bfff7f'];	
                
            }
            fetch(url, requestOptions)
                .then(response => response.json())
                .then(result => {
                    result.forEach(rs => {
                        keyword.unshift(rs.keyword);
                        searchNum.unshift(rs.searchNum);
                        link.unshift(rs.link);
                        rank.unshift(rs.rank);
                        if(newval==2||newval==3)
                        tttime.unshift(rs.time);
                    });
                    if(keyword == 0)
                    {
                        return;
                    }
                    else
                    {
                        this.isShowButton = true;
                    }
                    myChart.setOption(option);
                    
                })
                .catch(error => console.log('error', error));




            // 指定图表的配置项和数据
            var option = {
                backgroundColor:'rgba(225, 225, 225, 0.5)', //rgba设置透明度
                grid: {
                    containLabel: true,
                    //right: 120,
                    left: '0%',
                    right: '15%',
                    bottom:'0%'
                },
                title: {
                    text: this.titleText,
                    /*top: 25,
                    left: 300,*/
                    left: 'center',
                    //right: '0%',
                    top:'0%'

                },
                animation:false,
                tooltip: {},
                legend: {
                    data: ['热度', this.lengendData],
                    top: 30,
                    left: 'center',
                },
                yAxis: {
                    data: keyword,
                    
                    axisPointer: {
                        label: {
                            show: true,
                            margin: 30
                        }
                    },
                    axisLabel: {
                        formatter: function (val) {
                            if(newval==2||newval==3)
                            return val + " "+tttime[getArrayIndex(keyword, val)];
                            else
                            return val;
                        }
                    }
                },
                xAxis: [{
                    type: 'value',
                    name: '热度',
                    axisLabel: {
                        interval: 0, //坐标刻度之间的显示间隔，默认就可以了（默认是不重叠）
                        rotate: 25 //调整数值改变倾斜的幅度（范围-90到90）
                    }
                }, {
                    type: 'value',
                    name: this.xAxisName,
                    minInterval: 1,
                    max: function (value) {
                        return Math.ceil(value.max * 1.2)
                    },
                    splitLine: {
                        show: false
                    }
                }],
                series: [{
                        name: '热度',
                        type: 'bar',
                        //barCategoryGap:"50%",
                        //barWidth:"10px",
                        
                        data: searchNum,
                        label: {
                            show: true,
                            position: 'right'
                        },
                        emphasis: {
                            itemStyle: {
                                color: '#6495ED'
                            }
                        },
                        itemStyle: {
                            normal: {
                                color: function (params) {
                                    return myColor[getArrayIndex(keyword, params.name)]
                                },
                                barBorderRadius: [5, 9, 9, 5]
                            }
                        }
                    },
                    {
                        name: this.lengendData,//'单日最高热搜排名'
                        type: 'line',
                        lineStyle: {
                            color: '#FF8C00',
                            width: 1.75
                        },
                        emphasis: {
                            itemStyle: {
                                color: '#6495ED'
                            }
                        },
                        symbol: 'pin',
                        symbolSize: 16,
                        xAxisIndex: 1,
                        data: rank,
                        itemStyle: {
                            normal: {
                                color: function (params) {
                                    return '#FFD700'
                                }
                            }
                        }
                    }
                ]

            };
            // 处理点击事件并且链接到对应的微博
            myChart.on('click', function (params) {
                //所有的鼠标事件包含参数 params，这是一个包含点击图形的数据信息的对象
                window.open(link[getArrayIndex(keyword, params.name)])
            });

        }
        }
    }    
</script>

<style lang="" scoped>
    #main{        
       /* background-color:rgba(225, 225, 225, 0.5);*/
    }
    .more{
        position: absolute;
        right:0px;
        top:0px;
    }
</style>