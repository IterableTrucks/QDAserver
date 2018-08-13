var ctx = document.getElementById("vym_yield_chart").getContext('2d');
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
var Duration=["UST1M","UST3M","UST6M","UST1Y","UST2Y","UST3Y","UST5Y","UST7Y",
					"UST10Y","UST20Y","UST30Y"]
var cfg={
	type:'line',
	data:{
		datasets:[{
			label:'VYM Div Yield',
			fill:false,
			lineTension:0,
			data:[],
			borderColor:"rgb(75, 192, 192)"

		}]
	},
	options:{
		maintainAspectRatio:false,
		scales:{
			xAxes:[{
				type:'time',
				time:{
					unit:'day'
				},				
				gridLines:{
					display:false					
				},
				distribution:"series",
				ticks:{
					source:"data",
  					callback:function(dateLabel,index){
						return index % 5==0? dateLabel:""
					} 
				}
			}],
			yAxes:[{
				gridLines:{
					
				},
				ticks:{
					suggestedMax:11,					
					suggestedMin:0,
					stepSize:1,
					callback:function(value,index,values){
						if (value==11){
							return "Zero"
						}
						if (value>=0) {
							return Duration[10-value]
						}
						if (value<0){
							return "UST30Y+"+(-value*100).toString()+"bp"
						}
					}
				}
			}]
		},
		tooltips:{
                        intersect:false,
                        mode:'index',
			callbacks:{
				title:function(tooltipItems,data){
					var date=data.datasets[0].data[tooltipItems[0].index].x
					options={month:'short',day:'numeric',year:'numeric'}
					return date.toLocaleDateString("en-US",options)
				},
				label:function(tooltipItem,data){
					return data.datasets[0].label+":"+data.datasets[0].data[tooltipItem.index].z
				}
			}
		}
	}
}
var vym= new Chart(ctx,cfg)
var chartData=[]
var left_verge_date=new Date()
var chartDate_length_monitor=0
left_verge_date.setDate(today.getDate()-100)
/* function initChart(from_date,to_date)
{ */
 	$.getJSON("/VYM/data.json?from="+formatDate(from)+"&to="+formatDate(today),function(result){
		$.each(result.data,function(index,field){
			var dot={x:"",y:"",z:""}
			dot.x=new Date(field.date)
			dot.z=field.dividend_yield
			if (dot.z<=field.UST1M ){
				dot.y=11-dot.z/field.UST1M
				chartData.push(dot)
			}
			if (dot.z>=field.UST30Y){
				dot.y=field.UST30Y-dot.z
				chartData.push(dot)
			}
			for (var i=0;i<10;i++){
				if ((dot.z>=field[Duration[i]] && dot.z<=field[Duration[i+1]]) ||
					(dot.z<=field[Duration[i]] && dot.z>=field[Duration[i+1]])) {
						if (field[Duration[i]]==field[Duration[i+1]]){
							dot.y=10-i
							chartData.push(dot)
							dot.y=9-i
							chartData.push(dot)
						}
						else {
							dot.y=10-i-(dot.z-field[Duration[i]])/(field[Duration[i+1]]-field[Duration[i]])
							chartData.push(dot)
						}
					}
			}
		})
		vym.config.data.datasets[0].data=chartData

	
		vym.config.options.scales.xAxes[0].time.min=left_verge_date
		vym.update()
		chartDate_length_monitor=chartData.length
	})
/* } */
/* initChart(from,today) */
var slider=$("#slider").dateRangeSlider({
	bounds:{
		min:new Date("2018-1-30"),
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
$("#slider").on("valuesChanging",function(e,data){
	if (chartDate_length_monitor!=0) {
		if (data.values.min<from) {
			var chartData_append=[]
			var to_date=from
			to_date.setDate(from.getDate()-1)
			from=data.values.min
			from.setDate(data.values.min.getDate()-400)			
			$.getJSON("/VYM/data.json?from="+formatDate(from)+"&to="+formatDate(to_date),function(result){
				$.each(result.data,function(index,field){
					var dot={x:"",y:"",z:""}
					dot.x=new Date(field.date)
					dot.z=field.dividend_yield
					if (dot.z<=field.UST1M ){
						dot.y=11-dot.z/field.UST1M
						chartData_append.push(dot)
					}
					if (dot.z>=field.UST30Y){
						dot.y=field.UST30Y-dot.z
						chartData_append.push(dot)
					}
					for (var i=0;i<10;i++){
						if ((dot.z>=field[Duration[i]] && dot.z<=field[Duration[i+1]]) ||
							(dot.z<=field[Duration[i]] && dot.z>=field[Duration[i+1]])) {
								if (field[Duration[i]]==field[Duration[i+1]]){
									dot.y=10-i
									chartData_append.push(dot)
									dot.y=9-i
									chartData_append.push(dot)
								}
								else {
									dot.y=10-i-(dot.z-field[Duration[i]])/(field[Duration[i+1]]-field[Duration[i]])
									chartData_append.push(dot)
								}
							}
					}
				})
				chartData=chartData_append.concat(chartData)
				vym.config.data.datasets[0].data=chartData
				vym.config.options.scales.xAxes[0].time.min=data.values.min
				vym.config.options.scales.xAxes[0].time.max=data.values.max
				vym.update()
			})
			
		}
		else{			
			vym.config.options.scales.xAxes[0].time.min=data.values.min
			vym.config.options.scales.xAxes[0].time.max=data.values.max
			vym.update()			
		}
	}	
})
