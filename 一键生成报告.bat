@echo off
chcp 65001 >nul
echo =========================================
echo       个人体检健康趋势深度分析系统
echo =========================================
echo.

echo [1/3] 正在解析 PDF 报告并提取数�?(src\parser.py)...
call .\venv\Scripts\activate.bat
python src\parser.py
if %errorlevel% neq 0 (
    echo [错误] 解析 PDF 数据失败�?    pause
    exit /b %errorlevel%
)
echo.

echo [2/3] 正在分析健康指标、生�?Markdown 报告 (src\analyze_health.py)...
python src\analyze_health.py
if %errorlevel% neq 0 (
    echo [错误] 分析健康指标失败�?    pause
    exit /b %errorlevel%
)
echo.

echo [3/3] 正在生成可视�?HTML 仪表盘页�?(src\generate_dashboard.py)...
python src\generate_dashboard.py
if %errorlevel% neq 0 (
    echo [错误] 生成仪表盘失败！
    pause
    exit /b %errorlevel%
)
echo.

echo =========================================
echo  处理完成！所有报告已成功生成�?echo  请在浏览器中双击打开 output\dashboard.html 查看�?echo =========================================
pause
