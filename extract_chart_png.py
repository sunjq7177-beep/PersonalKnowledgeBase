#!/usr/bin/env python3
"""
从原始PDF中提取图表证据截图
"""
import fitz  # PyMuPDF
import os
import shutil

BASE_DIR = "/Users/sunjiaqi/个人项目程序/PersonalKnowledgeBase"

# 定义需要提取的图表
# 格式: (pdf_path, page_num, output_path, description)
# page_num 从 1 开始

CHARTS_TO_EXTRACT = [
    # 储能
    (
        "raw/研究报告/03-行业报告/01-电力设备与新能源/20260402-太平洋证券-太平洋证券新能源+AI展望（第5期）：重视储能产业链调整带来的机会.pdf",
        2,  # PDF第2页 - 电力设备及新能源相对表现
        "Resources/投研数据库/00-图表证据/行业/储能/01-电力设备及新能源相对表现.png",
        "电力设备及新能源相对表现"
    ),
    (
        "raw/研究报告/03-行业报告/01-电力设备与新能源/20260402-太平洋证券-太平洋证券新能源+AI展望（第5期）：重视储能产业链调整带来的机会.pdf",
        3,  # PDF第3页 - 河南新型储能政策核心措施
        "Resources/投研数据库/00-图表证据/行业/储能/02-河南新型储能政策核心措施.png",
        "河南新型储能政策核心措施"
    ),
    # AI算力链 - 光模块
    (
        "raw/研究报告/03-行业报告/04-算力与AI/20260406-东吴证券-东吴证券海外算力周跟踪：光互联CPO&OCS共振，PCB扩产加码迎技术升级新周期.pdf",
        4,  # 光模块市场规模CAGR预测
        "Resources/投研数据库/00-图表证据/行业/AI算力链/01-光模块市场规模CAGR预测.png",
        "光模块市场规模CAGR预测"
    ),
    (
        "raw/研究报告/03-行业报告/04-算力与AI/20260406-东吴证券-东吴证券海外算力周跟踪：光互联CPO&OCS共振，PCB扩产加码迎技术升级新周期.pdf",
        5,  # OCS市场预测大幅上调
        "Resources/投研数据库/00-图表证据/行业/AI算力链/02-OCS市场预测大幅上调.png",
        "OCS市场预测大幅上调"
    ),
    (
        "raw/研究报告/03-行业报告/06-光模块与通信/20260406-方正证券-方正证券光模块设备深度：光模块需求爆发，驱动设备进入发展快车道.pdf",
        6,  # 800G光模块设备爆发
        "Resources/投研数据库/00-图表证据/行业/AI算力链/03-800G光模块设备爆发.png",
        "800G光模块设备爆发"
    ),
    (
        "raw/研究报告/03-行业报告/04-算力与AI/20260406-东吴证券-东吴证券海外算力周跟踪：光互联CPO&OCS共振，PCB扩产加码迎技术升级新周期.pdf",
        8,  # 三大龙头PCB资本开支
        "Resources/投研数据库/00-图表证据/行业/AI算力链/04-三大龙头PCB资本开支.png",
        "三大龙头PCB资本开支"
    ),
    # 房地产
    (
        "raw/研究报告/03-行业报告/02-房地产/20260403-银河证券-银河证券房地产高质量发展跟踪系列之一：房地产市场筑底企稳了吗.pdf",
        4,  # 70城房价指数与调整周期
        "Resources/投研数据库/00-图表证据/行业/房地产/01-70城房价指数与调整周期.png",
        "70城房价指数与调整周期"
    ),
    (
        "raw/研究报告/03-行业报告/02-房地产/20260403-银河证券-银河证券房地产高质量发展跟踪系列之一：房地产市场筑底企稳了吗.pdf",
        5,  # 城市分级土拍溢价率
        "Resources/投研数据库/00-图表证据/行业/房地产/02-城市分级土拍溢价率.png",
        "城市分级土拍溢价率"
    ),
    (
        "raw/研究报告/03-行业报告/02-房地产/20260403-银河证券-银河证券房地产高质量发展跟踪系列之一：房地产市场筑底企稳了吗.pdf",
        6,  # 上海租金回报率突破关键阈值
        "Resources/投研数据库/00-图表证据/行业/房地产/03-上海租金回报率突破关键阈值.png",
        "上海租金回报率突破关键阈值"
    ),
    # 阳光电源
    (
        "raw/研究报告/03-行业报告/01-电力设备与新能源/20260401-东吴证券-阳光电源（300274.SZ）：2025年报点评，毛利率短期承压，储能高增持续，AIDC潜力可期.pdf",
        4,  # 收入与净利润趋势
        "Resources/投研数据库/00-图表证据/公司/阳光电源/01-收入与净利润趋势.png",
        "收入与净利润趋势"
    ),
    (
        "raw/研究报告/03-行业报告/01-电力设备与新能源/20260401-东吴证券-阳光电源（300274.SZ）：2025年报点评，毛利率短期承压，储能高增持续，AIDC潜力可期.pdf",
        5,  # 三大业务板块对比
        "Resources/投研数据库/00-图表证据/公司/阳光电源/02-三大业务板块对比.png",
        "三大业务板块对比"
    ),
    (
        "raw/研究报告/03-行业报告/01-电力设备与新能源/20260401-东吴证券-阳光电源（300274.SZ）：2025年报点评，毛利率短期承压，储能高增持续，AIDC潜力可期.pdf",
        6,  # 季度毛利率走势
        "Resources/投研数据库/00-图表证据/公司/阳光电源/03-季度毛利率走势.png",
        "季度毛利率走势"
    ),
    (
        "raw/研究报告/03-行业报告/01-电力设备与新能源/20260401-东吴证券-阳光电源（300274.SZ）：2025年报点评，毛利率短期承压，储能高增持续，AIDC潜力可期.pdf",
        7,  # 储能业务出货量预测
        "Resources/投研数据库/00-图表证据/公司/阳光电源/04-储能业务出货量预测.png",
        "储能业务出货量预测"
    ),
]


def extract_page_as_png(pdf_path, page_num, output_path):
    """从PDF中提取指定页面为PNG"""
    full_pdf_path = os.path.join(BASE_DIR, pdf_path)

    if not os.path.exists(full_pdf_path):
        print(f"[SKIP] PDF not found: {full_pdf_path}")
        return False

    # 确保输出目录存在
    os.makedirs(os.path.dirname(os.path.join(BASE_DIR, output_path)), exist_ok=True)

    try:
        doc = fitz.open(full_pdf_path)
        # page_num 从 1 开始，fitz 从 0 开始
        page = doc[page_num - 1]

        # 渲染页面为图像 (150 DPI for good quality)
        mat = fitz.Matrix(150/72, 150/72)  # 约2x缩放
        pix = page.get_pixmap(matrix=mat)

        full_output_path = os.path.join(BASE_DIR, output_path)
        pix.save(full_output_path)
        doc.close()

        print(f"[OK] Saved: {output_path}")
        return True
    except Exception as e:
        print(f"[ERROR] Failed to extract {output_path}: {e}")
        return False


def main():
    print("开始从PDF提取图表截图...")
    print("=" * 60)

    success_count = 0
    fail_count = 0

    for pdf_path, page_num, output_path, desc in CHARTS_TO_EXTRACT:
        print(f"\n提取: {desc}")
        print(f"  PDF页码: {page_num}")
        print(f"  输出: {output_path}")

        if extract_page_as_png(pdf_path, page_num, output_path):
            success_count += 1
        else:
            fail_count += 1

    print("\n" + "=" * 60)
    print(f"完成! 成功: {success_count}, 失败: {fail_count}")

    # 列出所有已提取的PNG
    print("\n已提取的PNG文件:")
    for _, _, output_path, _ in CHARTS_TO_EXTRACT:
        full_path = os.path.join(BASE_DIR, output_path)
        if os.path.exists(full_path):
            size = os.path.getsize(full_path) / 1024
            print(f"  {output_path} ({size:.1f} KB)")


if __name__ == "__main__":
    main()