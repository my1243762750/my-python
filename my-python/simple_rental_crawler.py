#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化版租房信息爬虫 - 不依赖pandas
爬取重庆沙坪坝区租房数据
"""

import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook
import time
import json
from datetime import datetime
import re

class SimpleRentalCrawler:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.houses = []
    
    def crawl_58(self, page_count=3):
        """爬取58同城租房数据"""
        print(f"开始爬取58同城重庆沙坪坝区租房信息...")
        
        for page in range(1, page_count + 1):
            try:
                url = f"https://cq.58.com/chuzu/sha-ping-ba-qu/pn{page}/"
                print(f"正在爬取第 {page} 页...")
                
                response = requests.get(url, headers=self.headers, timeout=10)
                response.encoding = 'utf-8'
                soup = BeautifulSoup(response.text, 'html.parser')
                
                house_items = soup.select('.property')
                
                for item in house_items:
                    try:
                        title_elem = item.select_one('.property-content-title-name')
                        price_elem = item.select_one('.property-price')
                        
                        if title_elem:
                            house_info = {
                                '标题': title_elem.text.strip(),
                                '价格': price_elem.text.strip() if price_elem else '价格面议',
                                '来源': '58同城',
                                '爬取时间': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            }
                            self.houses.append(house_info)
                            print(f"  - {house_info['标题']} ({house_info['价格']})")
                    
                    except Exception as e:
                        continue
                
                time.sleep(3)
                
            except Exception as e:
                print(f"爬取第 {page} 页时出错: {e}")
                continue
    
    def save_to_excel(self, filename='重庆沙坪坝租房数据.xlsx'):
        """保存数据到Excel"""
        if not self.houses:
            print("没有爬取到任何房源数据")
            return False
        
        try:
            wb = Workbook()
            ws = wb.active
            ws.title = "重庆沙坪坝租房数据"
            
            # 添加表头
            headers = ['排名', '标题', '价格', '来源', '爬取时间']
            ws.append(headers)
            
            # 添加数据
            for i, house in enumerate(self.houses, 1):
                row = [i, house['标题'], house['价格'], house['来源'], house['爬取时间']]
                ws.append(row)
            
            # 调整列宽
            ws.column_dimensions['A'].width = 8
            ws.column_dimensions['B'].width = 50
            ws.column_dimensions['C'].width = 15
            ws.column_dimensions['D'].width = 10
            ws.column_dimensions['E'].width = 20
            
            wb.save(filename)
            print(f"数据已保存到 {filename}")
            print(f"共爬取 {len(self.houses)} 条房源信息")
            return True
            
        except Exception as e:
            print(f"保存Excel文件时出错: {e}")
            return False
    
    def analyze_data(self):
        """分析房源数据"""
        if not self.houses:
            print("没有数据可分析")
            return
        
        print("\n=== 房源数据分析 ===")
        print(f"总房源数: {len(self.houses)}")
        
        # 来源统计
        sources = {}
        for house in self.houses:
            source = house['来源']
            sources[source] = sources.get(source, 0) + 1
        
        print("\n来源统计:")
        for source, count in sources.items():
            print(f"  {source}: {count}条")

def main():
    """主函数"""
    print("=" * 50)
    print("重庆沙坪坝区租房信息爬虫 (简化版)")
    print("=" * 50)
    
    crawler = SimpleRentalCrawler()
    
    # 爬取数据
    crawler.crawl_58(3)
    
    # 保存数据
    crawler.save_to_excel()
    
    # 分析数据
    crawler.analyze_data()
    
    print("\n" + "=" * 50)
    print("爬取完成！")
    print("请查看生成的 重庆沙坪坝租房数据.xlsx 文件")
    print("=" * 50)

if __name__ == "__main__":
    main() 