import json

def generate_dashboard():
    # Read the data
    with open("data/chart_data.json", "r", encoding="utf-8") as f:
        chart_data = json.load(f)
    with open("docs/health_report.md", "r", encoding="utf-8") as f:
        md_content = f.read()

    # Pass the JSON object to the frontend
    chart_json_str = json.dumps(chart_data)
    md_content_js = json.dumps(md_content)

    html_template = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>健康脉络 (HealthTrace) - 体检健康趋势深度分析</title>
    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
      tailwind.config = {
        theme: {
          extend: {
            colors: {
              primary: '#38bdf8',
              secondary: '#818cf8',
              dark: '#0f172a',
              card: '#1e293b'
            }
          }
        }
      }
    </script>
    <!-- ECharts -->
    <script src="https://cdn.jsdelivr.net/npm/echarts@5.5.0/dist/echarts.min.js"></script>
    <!-- Marked.js for Markdown parsing -->
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
    <style>
        body {
            background-color: #0f172a;
            color: #f8fafc;
            font-family: 'Inter', system-ui, -apple-system, sans-serif;
            background-image: 
                radial-gradient(at 0% 0%, rgba(56, 189, 248, 0.15) 0px, transparent 50%),
                radial-gradient(at 100% 0%, rgba(129, 140, 248, 0.15) 0px, transparent 50%);
            background-attachment: fixed;
        }
        .glass-panel {
            background: rgba(30, 41, 59, 0.6);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 1.25rem;
            box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.5);
        }
        .report-panel {
            background: linear-gradient(145deg, rgba(30, 41, 59, 0.8), rgba(15, 23, 42, 0.9));
            border-left: 2px solid rgba(56, 189, 248, 0.3);
        }
        
        .markdown-body { font-size: 0.95rem; }
        .markdown-body h1 { font-size: 2rem; font-weight: 800; margin-bottom: 1.5rem; background: -webkit-linear-gradient(45deg, #38bdf8, #818cf8); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .markdown-body h2 { font-size: 1.35rem; font-weight: 700; margin-top: 2.5rem; margin-bottom: 1rem; color: #f8fafc; border-bottom: 1px solid rgba(255,255,255,0.05); padding-bottom: 0.5rem; display: flex; align-items: center; gap: 0.5rem; }
        .markdown-body h2::before { content: ''; display: block; width: 4px; height: 1.1rem; background: #38bdf8; border-radius: 2px; }
        .markdown-body h3 { font-size: 1.15rem; font-weight: 600; margin-top: 1.5rem; margin-bottom: 0.75rem; color: #bae6fd; }
        .markdown-body p { margin-bottom: 1.25rem; line-height: 1.7; color: #94a3b8; }
        .markdown-body ul { list-style-type: none; padding-left: 0.5rem; margin-bottom: 1.5rem; color: #cbd5e1; }
        .markdown-body li { margin-bottom: 0.75rem; position: relative; padding-left: 1.5rem; line-height: 1.6; color: #cbd5e1; }
        .markdown-body li::before { content: '•'; position: absolute; left: 0; color: #38bdf8; font-weight: bold; font-size: 1.2rem; line-height: 1; }
        .markdown-body strong { color: #e2e8f0; font-weight: 600; }
        
        /* Custom Scrollbar for right panel */
        .scroller::-webkit-scrollbar { width: 6px; }
        .scroller::-webkit-scrollbar-track { background: transparent; }
        .scroller::-webkit-scrollbar-thumb { background: rgba(148, 163, 184, 0.2); border-radius: 10px; }
        .scroller::-webkit-scrollbar-thumb:hover { background: rgba(148, 163, 184, 0.4); }
    </style>
</head>
<body class="min-h-screen p-4 md:p-6 lg:p-8">
    <div class="max-w-[1600px] mx-auto space-y-8">
        
        <!-- Header Section -->
        <header class="text-center py-4 mb-4 relative">
            <h1 class="text-3xl md:text-5xl font-extrabold tracking-tight text-white relative z-10 drop-shadow-md">
                <span class="text-transparent bg-clip-text bg-gradient-to-r from-primary to-secondary">健康脉络</span> (HealthTrace)
            </h1>
            <p class="mt-3 text-slate-400 font-medium tracking-wide relative z-10">基于历年数据的深度 AI 分析与健康管理</p>
        </header>

        <div class="flex flex-col xl:flex-row gap-6 lg:gap-8 items-start">
            <!-- Left Column: Charts Area (Takes up more space) -->
            <div class="w-full xl:w-2/3 space-y-6">
                <div class="flex items-center justify-between px-2 mb-2">
                    <h2 class="text-2xl font-bold text-slate-100 flex items-center gap-2">
                        <svg class="w-6 h-6 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 12l3-3 3 3 4-4M8 21l4-4 4 4M3 4h18M4 4h16v12a1 1 0 01-1 1H5a1 1 0 01-1-1V4z"></path></svg>
                        历年指标追踪
                    </h2>
                </div>
                <!-- Responsive Grid for Charts: 1 col on mobile, 2 cols on md/lg desktop -->
                <div class="grid grid-cols-1 md:grid-cols-2 gap-6" id="charts-container">
                    <!-- Charts will be dynamically injected here -->
                </div>
            </div>

            <!-- Right Column: Report Panel -->
            <div class="w-full xl:w-1/3 glass-panel report-panel p-6 shadow-2xl sticky top-8 max-h-[85vh] overflow-y-auto scroller">
                <div class="flex items-center gap-3 mb-6 pb-4 border-b border-slate-700/50">
                    <div class="p-2 bg-primary/20 rounded-lg">
                        <svg class="w-6 h-6 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg>
                    </div>
                    <h2 class="text-xl font-bold text-slate-100 m-0">深度评估报告</h2>
                </div>
                <div id="report-content" class="markdown-body"></div>
            </div>
        </div>
    </div>

    <!-- Data Injection & Rendering Logic -->
    <script>
        // 1. Render Markdown Report
        const mdContent = _MD_CONTENT_INJECT_;
        document.getElementById('report-content').innerHTML = marked.parse(mdContent);

        // 2. Render Charts
        const rawChartData = _CHART_DATA_INJECT_;
        const chartsData = rawChartData.charts;
        const container = document.getElementById('charts-container');
        
        // Define color palettes for variety
        const colorPalettes = [
            { main: '#38bdf8', area: 'rgba(56, 189, 248, 0.5)' }, // Cyan
            { main: '#818cf8', area: 'rgba(129, 140, 248, 0.5)' }, // Indigo
            { main: '#34d399', area: 'rgba(52, 211, 153, 0.5)' }, // Emerald
            { main: '#fbbf24', area: 'rgba(251, 191, 36, 0.5)' }, // Amber
            { main: '#f472b6', area: 'rgba(244, 114, 182, 0.5)' }, // Pink
            { main: '#c084fc', area: 'rgba(192, 132, 252, 0.5)' }, // Purple
        ];

        const metrics = Object.keys(chartsData);
        let charts = [];
        
        metrics.forEach((metric, index) => {
            const dataPts = chartsData[metric];
            if (!dataPts || dataPts.length === 0) return;
            
            const palette = colorPalettes[index % colorPalettes.length];
            
            // Generate distinct card for each chart
            const chartIdx = 'chart-' + index;
            const wWrapper = document.createElement('div');
            // Make important metrics span full width if needed, or keep 1 col
            wWrapper.className = 'glass-panel p-5 shadow-lg relative group transition-all duration-300 hover:border-slate-600 hover:shadow-primary/10';
            wWrapper.innerHTML = `
                <div class="absolute top-0 right-0 p-3 opacity-20 group-hover:opacity-40 transition-opacity">
                    <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M7 12l3-3 3 3 4-4M8 21l4-4 4 4M3 4h18M4 4h16v12a1 1 0 01-1 1H5a1 1 0 01-1-1V4z"></path></svg>
                </div>
                <h3 class="text-lg font-semibold mb-1 text-slate-200">${metric}</h3>
                <p class="text-xs text-slate-500 mb-4 px-1">历年跟踪趋势</p>
                <div id="${chartIdx}" style="width: 100%; height: 260px;"></div>
            `;
            container.appendChild(wWrapper);

            // Initialize ECharts
            const chartDom = document.getElementById(chartIdx);
            const myChart = echarts.init(chartDom, 'dark');
            charts.push(myChart);

            const xData = dataPts.map(d => d.year);
            const yData = dataPts.map(d => d.value);

            // Calculate min/max for better dynamic Y-Axis scaling
            const yMin = Math.min(...yData);
            const yMax = Math.max(...yData);
            const padding = (yMax - yMin) * 0.2;

            const option = {
                backgroundColor: 'transparent',
                tooltip: {
                    trigger: 'axis',
                    backgroundColor: 'rgba(15, 23, 42, 0.9)',
                    borderColor: 'rgba(255,255,255,0.1)',
                    textStyle: { color: '#f8fafc' },
                    axisPointer: { type: 'cross', label: { backgroundColor: '#1e293b' } }
                },
                grid: {
                    left: '5%', right: '5%', top: '8%', bottom: '8%', containLabel: true
                },
                xAxis: [
                    {
                        type: 'category',
                        boundaryGap: false,
                        data: xData,
                        axisLine: { show: false },
                        axisTick: { show: false },
                        axisLabel: { color: '#64748b', margin: 12, fontWeight: 500 }
                    }
                ],
                yAxis: [
                    {
                        type: 'value',
                        splitLine: { lineStyle: { color: 'rgba(255,255,255,0.05)', type: 'dashed' } },
                        axisLabel: { color: '#64748b', formatter: (val) => Number.isInteger(val) ? val : val.toFixed(1) },
                        min: Math.floor(yMin - (padding > 0 ? padding : yMin * 0.1)),
                        max: Math.ceil(yMax + (padding > 0 ? padding : yMax * 0.1))
                    }
                ],
                series: [
                    {
                        name: metric,
                        type: 'line',
                        smooth: 0.4,
                        itemStyle: { color: palette.main },
                        lineStyle: { width: 3, shadowColor: palette.area, shadowBlur: 10, shadowOffsetY: 5 },
                        areaStyle: {
                            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                                { offset: 0, color: palette.main.replace(')', ', 0.4)').replace('rgb', 'rgba') },  /* Fallback */
                                { offset: 0, color: palette.main + '66' }, /* hex alpha 40% */
                                { offset: 1, color: palette.main + '00' }  /* transparent */
                            ])
                        },
                        data: yData,
                        symbol: 'circle',
                        symbolSize: 6,
                        showSymbol: yData.length === 1,
                        emphasis: {
                            focus: 'series',
                            itemStyle: { borderWidth: 2, borderColor: '#fff' }
                        }
                    }
                ]
            };

            myChart.setOption(option);
        });
        
        // Handle Resizing
        window.addEventListener('resize', () => {
            charts.forEach(chart => chart.resize());
        });
    </script>
</body>
</html>
"""
    
    html_content = html_template.replace("_MD_CONTENT_INJECT_", md_content_js).replace("_CHART_DATA_INJECT_", chart_json_str)

    with open("output/dashboard.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    print("Dashboard generated: output/dashboard.html")

if __name__ == "__main__":
    generate_dashboard()
