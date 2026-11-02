<template>
  <h2 style="margin:0 0 20px 0; color:#2c3e50; font-size:26px; font-weight:600;">
  电商销售看板
  </h2>
  <div style="background-color: #eef1f6; min-height:100vh; padding:24px;">
  <!--月度销售下拉框-->
  <select v-model="currentIndication" style="padding: 8px 12px; border: 1px solid #cbd5e1; border-radius: 6px; font-size:15px; color:#333; margin-bottom:20px;">
    <option v-for="item in monthlyIndicatorList":key="item.value":value="item.value">
      {{item.label}}
    </option>
  </select>
  <!--月度趋势图容器-->
  <div class = "card" style="padding:20px; background:#fff; border-radius:12px; box-shadow: 0 2px 12px rgba(0,0,0,0.08); margin:16px 0;">
    <button @click = 'downloadMonthlyChart' style="padding:6px 12px; border:1px solid #0066cc;border-radius:6px;background:#fff; color:#0066cc; cursor:pointer; margin-bottom:12px;">
      下载
    </button>
    <div ref="monthlyChart" style="width:800px;height:400px;margin-bottom:20px;"></div>
  </div>
  <!--国家销售饼图容器-->
  <div class = "card" style="padding:20px; background:#fff; border-radius:12px; box-shadow: 0 2px 12px rgba(0,0,0,0.08); margin:16px 0;">
    <button @click="downloadCountryChart" style="padding:6px 12px; border:1px solid #0066cc; border-radius:6px; background:#fff; color:#0066cc; cursor:pointer; margin-bottom:12px;">
      下载
    </button>
    <div ref="countryChart" style="width:800px;height:400px;margin-bottom:20px;"></div>
  </div>
  <!--商品销量柱状图容器-->
  <div class = "card" style="padding:20px; background:#fff; border-radius:12px; box-shadow: 0 2px 12px rgba(0,0,0,0.08); margin:16px 0;">
    <button @click="downloadGoodsChart" style="padding:6px 12px; border:1px solid #0066cc; border-radius:6px; background:#fff; color:#0066cc; cursor:pointer; margin-bottom:12px;">
      下载
    </button>
    <div ref="goodsChart" style="width:800px;height:400px;margin-bottom:20px;"></div>
    </div>
  </div>
</template>

<script setup>
  import {ref,onMounted,watch} from 'vue'
  import axios from 'axios'
  import * as echarts from 'echarts'
  const monthlyChart = ref(null)
  const countryChart = ref(null)
  const goodsChart = ref(null)
  const monthlyData = ref([])
  //初始默认显示销售额
  const currentIndication = ref('sales_amount')
  //定义下拉框的选项
  const monthlyIndicatorList = ref([
    {label:'销售额',value:'sales_amount'},
    {label:'订单数量',value:'order_count'},
    {label:'客户数量',value:'customer_count'}
  ])
  //存储echart实例，并初始化-->
  let monthlyChartInstance = null
  let pieInstance = null
  let goodsInstance = null
  //渲染图表函数-->
  const renderMonthlyChart = () =>{
    if(!monthlyChartInstance){
      monthlyChartInstance = echarts.init(monthlyChart.value)
    }
    const xData = monthlyData.value.map(item => item.year_month)
    const yData = monthlyData.value.map(item => item[currentIndication.value])
    const nameMap = {
      sales_amount:'销售额',
      order_count:'订单数量',
      customer_count:'客户数量'
    }

    const option = {
      title:{
        text:'月度'+nameMap[currentIndication.value]+'趋势'
      },
      tooltip:{
        trigger:'axis'
      },
      xAxis:{
        type:'category',
        data:xData
      },
      yAxis:{
        type:'value'
      },
      series:[
        {
        type:'line',
        name:nameMap[currentIndication.value],
        data:yData,
        lineStyle:{
          color:'#0066cc'
        }
      }
      ]
    }
    monthlyChartInstance.setOption(option)
  }

  //监听 currentIndicator-->
  watch(currentIndication,() => {
    renderMonthlyChart()
  })
  
  //导出图片
  const downloadMonthlyChart = () =>{
    const imgUrl = monthlyChartInstance.getDataURL({
      pixeRatio:2,
      backgroundColor:'#fff'
    })
    const a = dccument.createElement('a')
    a.href = imgUrl
    a.download='月度'+nameMap[currentIndication.value]+'趋势图.png'
    a.click
  }

  // 导出饼图：各国销售额分布
const downloadCountryChart = () => {
  const imgUrl = pieInstance.getDataURL({
    pixelRatio: 2,
    backgroundColor: '#fff'
  })
  const a = document.createElement('a')
  a.href = imgUrl
  a.download = '各国销售额分布.png'
  a.click()
}

// 导出商品销量柱状图
const downloadGoodsChart = () => {
  const imgUrl = goodsInstance.getDataURL({
    pixelRatio: 2,
    backgroundColor: '#fff'
  })
  const a = document.createElement('a')
  a.href = imgUrl
  a.download = '商品销售排行.png'
  a.click()
}


  //国家名字转成中文
    const countryMap = {
      "United Kingdom": "英国",
      "France": "法国",
      "Germany": "德国",
      "Italy": "意大利",
      "Spain": "西班牙",
      "Netherlands": "荷兰",
      "Belgium": "比利时",
      "Sweden": "瑞典",
      "Denmark": "丹麦",
      "Norway": "挪威",
      "Finland": "芬兰",
      "Poland": "波兰",
      "Austria": "奥地利",
      "Czech Republic": "捷克共和国",
      "Slovakia": "斯洛伐克",
      "Hungary": "匈牙利",
      "Romania": "罗马尼亚",
      "Bulgaria": "保加利亚",
      "Greece": "希腊",
      "Portugal": "葡萄牙",
      "Ireland": "爱尔兰",
      "EIRE": "爱尔兰",
      "Switzerland": "瑞士",
      "Canada": "加拿大",
      "United States": "美国",
      "Brazil": "巴西",
      "Argentina": "阿根廷",
      "Australia": "澳大利亚",
      "Japan": "日本",
      "China": "中国",
      "Hong Kong": "中国香港",
      "Singapore": "新加坡",
      "Saudi Arabia": "沙特阿拉伯",
      "United Arab Emirates": "阿联酋",
      "Israel": "以色列",
      "Lebanon": "黎巴嫩",
      "Malta": "马耳他",
      "European Community": "欧洲共同体",
      "RSA": "南非",
      "Bahrain": "巴林",
      "Unspecified": "其他"
    }
  const getCountryName=(name)=>{
      return countryMap[name] || name
    }



  onMounted(async()=>{
    const [monthRes,countryRes,goodsRes]=await Promise.all([
      axios.get("http://127.0.0.1:8000/api/monthly"),
      axios.get("http://127.0.0.1:8000/api/country"),
      axios.get("http://127.0.0.1:8000/api/goods")
    ])
    monthlyData.value = monthRes.data.data
    renderMonthlyChart()
  const pieData = countryRes.data.data.map(item=>{
    return {name:getCountryName(item.Country),value:item.sales_amount}
  })
  pieInstance = echarts.init(countryChart.value)
  const pieOption = {
    title:{
      text:'各国销售额分布',
      left:'center'
    },
    tooltip:{
      trigger:'item'
    },
    series:[
      {
      type:'pie',
      radius:'60%',
      data:pieData
    }
    ]
  }
  pieInstance.setOption(pieOption)


  const topgoods = goodsRes.data.data.sort((a,b)=>b.quantity_total-a.quantity_total).slice(0,10)
  const goodX = topgoods.map(item => item.StockCode)
  const goodY = topgoods.map(item => item.quantity_total)
  goodsInstance = echarts.init(goodsChart.value)
  const goodsOption = {
    title:{
      text:'商品销售排行'
    },
    tooltip:{
      trigger:'item'
    },
    xAxis:{
      type:'category',
      data:goodX,
      axisLabel:{
        rotate:30
      }
    },
    yAxis:{
      type:'value'
    },
    series:[
      {
        type:'bar',
        data:goodY
      }
    ]
  }
  goodsInstance.setOption(goodsOption)
  })
</script>
