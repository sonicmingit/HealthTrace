import os
import glob
import re
import json
import pdfplumber

def map_item_name(raw_name):
    name = raw_name.strip()
    name_lower = name.lower()

    # 排除掉不相关的或仅仅是分类名称的词
    blacklist = ["血清", "测定", "正常", "参考", "项目", "结果", "单位", "异常", "范围", "提示", "血脂", "血糖", "肝功", "肾功", "尿常规", "血常规", "常规"]
    for word in blacklist:
        if name_lower == word:
            return None
            
    if "体重" in name:
        if "指数" in name or "bmi" in name_lower:
            return "BMI"
        return "体重"
    if "收缩压" in name or "高压" in name:
        return "血压收缩压"
    if "舒张压" in name or "低压" in name:
        return "血压舒张压"
    
    if "空腹血糖" in name or "葡萄糖" in name or "glu" in name_lower:
        return "空腹血糖"
        
    if "总胆固醇" in name or "tc" in name_lower or "cho" in name_lower:
        if "高密度" not in name and "低密度" not in name:
            return "总胆固醇"
    if "甘油三酯" in name or "tg" in name_lower:
        return "甘油三酯"
    if "高密度脂蛋白" in name or "hdl" in name_lower:
        return "HDL"
    if "低密度脂蛋白" in name or "ldl" in name_lower:
        return "LDL"

    # 更精确匹配尿酸，防止匹配到尿常规里的尿胆原等
    if "尿酸" in name or "ua" in name_lower:
        if "血尿酸" in name or name == "尿酸":
            return "尿酸"

    if ("丙氨酸" in name and "氨基转移酶" in name) or "谷丙转氨酶" in name or "alt" in name_lower or "gpt" in name_lower:
        return "ALT"
    if ("天门冬" in name and "氨基转移酶" in name) or "谷草转氨酶" in name or "ast" in name_lower or "got" in name_lower:
        return "AST"
        
    return None

def extract_data_from_pdf(filepath):
    extracted_data = {}
    print(f"  正在解析: {filepath}")
    
    try:
        with pdfplumber.open(filepath) as pdf:
            for page_num, page in enumerate(pdf.pages):
                # 尝试提取表格
                tables = page.extract_tables()
                for table in tables:
                    for row in table:
                        if not row:
                            continue
                        
                        # 清理行数据
                        clean_row = [str(cell).replace('\n', '') if cell else '' for cell in row]
                        
                        for i, cell in enumerate(clean_row):
                            mapped_name = map_item_name(cell)
                            if mapped_name and mapped_name not in extracted_data:
                                # 尝试在当前单元格的右侧寻找数值
                                for val_cell in clean_row[i+1:]:
                                    # 提取第一个浮点数
                                    match = re.search(r'\d+(\.\d+)?', val_cell)
                                    if match:
                                        extracted_data[mapped_name] = float(match.group())
                                        break
                                
                # 文本如果没提取完全，从纯文本再次匹配
                text = page.extract_text()
                if text:
                    lines = text.split('\n')
                    for line in lines:
                        # 常见的格式可能是 "体重 70.5 kg" 或者 "空腹血糖 5.1"
                        parts = re.split(r'\s+', line.strip())
                        for i, part in enumerate(parts):
                            mapped_name = map_item_name(part)
                            if mapped_name and mapped_name not in extracted_data:
                                # 找后面的数字
                                for p in parts[i+1:]:
                                    match = re.search(r'\d+(\.\d+)?', p)
                                    if match:
                                        extracted_data[mapped_name] = float(match.group())
                                        break
                                        
    except Exception as e:
        print(f"  读取 PDF {filepath} 时出错: {e}")
        
    return extracted_data

def main(report_dir):
    pdf_files = glob.glob(os.path.join(report_dir, "*.pdf"))
    if not pdf_files:
        print(f"未在目录 {report_dir} 下找到 PDF 文件。")
        return

    yearly_data = {}
    
    for pdf_file in pdf_files:
        filename = os.path.basename(pdf_file)
        
        # 从文件名提取年份
        year_match = re.search(r'(20\d{2})', filename)
        year = year_match.group(1) if year_match else "Unknown"
        
        data = extract_data_from_pdf(pdf_file)
        
        if year != "Unknown":
            # 简单的去重/选取逻辑：如果同一年有多份报告，取提取到有效数据最多的那份
            if year in yearly_data:
                if len(data) > len(yearly_data[year]):
                    yearly_data[year] = data
            else:
                yearly_data[year] = data

    # 按年份排序
    sorted_years = sorted(yearly_data.keys())
    final_data = [{"year": y, "metrics": yearly_data[y]} for y in sorted_years]

    # 保存提取的结构化数据
    output_file = os.path.join('data', 'health_data.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(final_data, f, ensure_ascii=False, indent=2)
    
    print(f"解析完成！从 {len(pdf_files)} 个文件中处理了 {len(yearly_data)} 个年度的数据。\n报告已保存为 {output_file}")

if __name__ == '__main__':
    # reports folder parameter, absolute or relative
    # Update back to original parent directory call format since it runs straight from root
    main(os.path.join("report"))
