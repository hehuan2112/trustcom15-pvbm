// Copyright 2017 Xi'an Jiaotong University
/**
 @fileoverview 用于绘制Course Video Predict的 CV Visited Estimated Distribution 统计预测
 * 本脚本的调用包括两个步骤
 * chart.init(divid); 用于将指定的div的id传给配置参数
 * chart.draw(data); 用于根据指定的数据绘图
 * 另外，此脚本依赖于`/api/course_cvpredict` API，需要在外部使用API获得数据
 * @author hehuan@mail.xjtu.edu.cn
 */
var chart_course_cvpredict_cvvhist = {
    myChart: null,
    option: {
        title : {
            text: '课件视频总访问量分布'
        },
        grid: {
            height: '70%',
            y: '15%'
        },
        tooltip : {
            formatter: function(obj){
                //var val = obj.value;
                //return num2csn[val[0]] + ' - chapter ' + val[1] + ': ' +
                //    val[2] + '次';
                return obj.value;
            }
        },
        legend: {
            data:['累积分布']
        },
        toolbox: {
            show : true,
            feature : {
                dataView : {show: true, readOnly: false},
                magicType : {show: true, type: ['line', 'bar']},
                restore : {show: true},
                saveAsImage : {show: true}
            }
        },
        calculable : true,
        xAxis : {
            name: '节',
            data: [],
            type: 'category'
        },
        yAxis : {
            name: '章',
            data: [],
            type: 'category'
        },
        visualMap: {
            min: 0,
            max: 100,
            inRange: {
                color: ['#00c0ef', '#dd4b39']
            },
            calculable: true,
            orient: 'horizontal',
            left: 'center',
            bottom: '5%'
        },
        series : [{
            name: '累积分布',
            type: 'heatmap',
            data: [],
            label: {
                normal: {
                    show: true
                }
            },
            itemStyle: {
                emphasis: {
                    shadowBlur: 10,
                    shadowColor: 'rgba(0, 0, 0, 0.5)'
                }
            } 
        }]
    },
    /**
     * Init the chart with a div id
     * @param {string} divid The id of a div tag for chart
     * @return {void} returns nothing
     */
    init: function(divid){
        this.myChart = echarts.init(document.getElementById(divid), 'shine');
    },

    /**
     * Draw or update the chart
     * @param {object} data The required data to draw graph
     * @returns {void} returns nothing
     */
    draw: function(data){
        this.option.xAxis.data = data.xdata;
        this.option.yAxis.data = data.ydata;
        this.option.visualMap.max = data.max;
        this.option.series[0].data = data.vals;
        this.myChart.setOption(this.option);
    }
};


