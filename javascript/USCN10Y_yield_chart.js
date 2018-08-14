var ctx = document.getElementById("yield_chart").getContext('2d');
var today=new Date()
var from=new Date()
from.setDate(new Date().getDate()-400)
var chartData=[]
function formatDate(date) {
   var d = new Date(date),
       month = '' + (d.getMonth() + 1),
       day = '' + d.getDate(),
       year = d.getFullYear();

   if (month.length < 2) month = '0' + month;
   if (day.length < 2) day = '0' + day;

   return [year, month, day].join('-');
}

var cfg={
	type:'line',
	data:{
		labels:[],
		datasets:[{
			label:'CN-US 10Y yield delta(bp)',
			fill:false,
//			lineTension:0,
			data:[],
			borderColor:"rgb(0, 0, 255)",
			backgroundColor:"rgb(0, 0, 255)",
			pointRadius:0,
			yAxisID:"delta"
		},{
			label:'CN10Y yield',
			fill:false,
//			lineTension:0,
			data:[],
			borderColor:"rgb(255, 0,0)",
			backgroundColor:"rgb(255, 0,0)",
			pointRadius:0,
			yAxisID:"yield"
		},{
			label:'US10Y yield',
			fill:false,
//			lineTension:0,
			data:[],
			borderColor:"rgb(0, 255, 0)",
			backgroundColor:"rgb(0, 255, 0)",
			pointRadius:0,
			yAxisID:"yield"			
		}]
	},
	options:{
		maintainAspectRatio:false,
                animation:{
                    duration:0
                },
		scales:{
			xAxes:[{
				type:'time',
				time:{
                                    displayFormats:{
                                        day:"MMM D, YYYY"
                                    }
				},				
				gridLines:{
					display:false					
				},
				distribution:"series",
				ticks:{
					source:"labels",
					autoSkip:true,
					maxTicksLimit:40,
/*   					callback:function(dateLabel,index){
						return index % 5==0? dateLabel:""
					}  */
				}
			}],
			yAxes:[{
				gridLines:{
					
				},
				ticks:{								
					callback:function(value,index,values){
						return value+ " bp"
					}
				},
				position:'left',
				id:'delta'
			},{
				gridLines:{
					
				},
				ticks:{									
					callback:function(value,index,values){
						return value+ "%"
					}
				},
				position:'right',
				id:'yield'				
			}]
		},
		hover:{
			mode:'index',
			intersect:false
		},
		tooltips:{
			intersect:false,
			mode:'index',
			callbacks:{
				title:function(tooltipItems,data){
					var date=data.labels[tooltipItems[0].index]
					options={month:'short',day:'numeric',year:'numeric'}
					return date.toLocaleDateString("en-US",options)
				},
				label:function(tooltipItem,data){
					if (tooltipItem.datasetIndex==0) {
						return data.datasets[0].label+":"+Math.round(tooltipItem.yLabel)
					}
					return data.datasets[tooltipItem.datasetIndex].label+":"+tooltipItem.yLabel
				}
					
				
			}
		}
	}
}
var yield_chart= new Chart(ctx,cfg)
var datelist=[],delta=[],CN10Y=[],US10Y=[]
var left_verge_date=new Date()
var chartDate_length_monitor=0
left_verge_date.setDate(today.getDate()-100)
var message_queue=[]
var slider=$("#slider").dateRangeSlider({
	bounds:{
		min:new Date("2010-07-01"),
		max:today
	},
	defaultValues:{
		min:left_verge_date,
		max:today
	},
	formatter:function(date){
		options={month:'short',day:'numeric',year:'numeric'}
		return date.toLocaleDateString("en-US",options)
	},
	valueLabels:"change",
})
var msg=$.getJSON("/USvsCN/data.json?from="+formatDate(from)+"&to="+formatDate(today),function(result){
		$.each(result.data,function(index,field){			
			datelist.push(new Date(field.date))
			delta.push((field.CN10Y-field.US10Y)*100)
			CN10Y.push(field.CN10Y)
			US10Y.push(field.US10Y)
		})
		yield_chart.config.data.labels=datelist
 		yield_chart.config.data.datasets[0].data=delta
		yield_chart.config.data.datasets[1].data=CN10Y
		yield_chart.config.data.datasets[2].data=US10Y
		yield_chart.config.options.scales.xAxes[0].time.min=left_verge_date
 		yield_chart.update()
	})
outer_msgqueue=[]
message_queue.push(msg)
outer_msgqueue.push(msg)
var i=0
$("#slider").on("valuesChanging",function(e,data){
		if (data.values.min<from) {
			var datelist_append=[],delta_append=[],CN10Y_append=[],US10Y_append=[]
			var to_date=from
			to_date.setDate(from.getDate()-1)
			from=data.values.min
			from.setDate(data.values.min.getDate()-400)
                        var j=i
                        i++                                                                            
                        console.log(i,from,to_date)    
                        var outer_msg=$.getJSON("/USvsCN/data.json?from="+formatDate(from)+"&to="+formatDate(to_date),function(result){
				$.each(result.data,function(index,field){
					datelist_append.push(new Date(field.date))
					delta_append.push((field.CN10Y-field.US10Y)*100)
					CN10Y_append.push(field.CN10Y)
					US10Y_append.push(field.US10Y)
                                })
                                var message=outer_msgqueue[j].done(function(){
                                    message_queue[j].done(function(){                                
                                        console.log(j)                                
				        datelist=datelist_append.concat(datelist)
    				        delta=delta_append.concat(delta)
				        CN10Y=CN10Y_append.concat(CN10Y)
				        US10Y=US10Y_append.concat(US10Y)
				        yield_chart.config.data.labels=datelist
				        yield_chart.config.data.datasets[0].data=delta
				        yield_chart.config.data.datasets[1].data=CN10Y
				        yield_chart.config.data.datasets[2].data=US10Y

				        yield_chart.config.options.scales.xAxes[0].time.min=data.values.min
				        yield_chart.config.options.scales.xAxes[0].time.max=data.values.max
                                        yield_chart.update()
                                    })
                                })
                                message_queue[j+1]=message
			})
                        outer_msgqueue.push(outer_msg)
		}
		else{			
			yield_chart.config.options.scales.xAxes[0].time.min=data.values.min
			yield_chart.config.options.scales.xAxes[0].time.max=data.values.max
			yield_chart.update()			
		}
		
})

