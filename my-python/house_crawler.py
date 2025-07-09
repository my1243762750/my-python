#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
租房信息爬虫
爬取房源数据：价格、面积、位置、设施等
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import json
from datetime import datetime

class HouseCrawler:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.houses = []
    
    def crawl_lianjia(self, area='北京', page_count=3):
        """爬取链家租房数据"""
        print(f"开始爬取{area}租房信息...")
        
        for page in range(1, page_count + 1):
            try:
                # 链家租房URL（示例）
                url = f"https://bj.lianjia.com/zufang/pg{page}/"
                print(f"正在爬取第 {page} 页...")
                
                response = requests.get(url, headers=self.headers, timeout=10)
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # 查找房源列表
                house_items = soup.select('.content__list--item')
                
                for item in house_items:
                    try:
                        # 提取房源信息
                        title = item.select_one('.content__list--item--title')
                        price = item.select_one('.content__list--item-price')
                        area = item.select_one('.content__list--item--des')
                        
                        if title and price:
                            house_info = {
                                '标题': title.text.strip(),
                                '价格': price.text.strip(),
                                '详情': area.text.strip() if area else '',
                                '来源': '链家',
                                '爬取时间': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            }
                            self.houses.append(house_info)
                            print(f"  - {house_info['标题']} ({house_info['价格']})")
                    
                    except Exception as e:
                        print(f"解析房源信息时出错: {e}")
                        continue
                
                time.sleep(2)  # 避免请求过快
                
            except Exception as e:
                print(f"爬取第 {page} 页时出错: {e}")
                continue
    
    def crawl_beike(self, area='北京', page_count=3):
        """爬取贝壳租房数据"""
        print(f"开始爬取贝壳{area}租房信息...")
        
        for page in range(1, page_count + 1):
            try:
                # 贝壳租房URL（示例）
                url = f"https://bj.ke.com/zufang/pg{page}/"
                print(f"正在爬取第 {page} 页...")
                
                response = requests.get(url, headers=self.headers, timeout=10)
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # 查找房源列表
                house_items = soup.select('.item')
                
                for item in house_items:
                    try:
                        # 提取房源信息
                        title = item.select_one('.item-title')
                        price = item.select_one('.item-price')
                        info = item.select_one('.item-info')
                        
                        if title and price:
                            house_info = {
                                '标题': title.text.strip(),
                                '价格': price.text.strip(),
                                '详情': info.text.strip() if info else '',
                                '来源': '贝壳',
                                '爬取时间': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            }
                            self.houses.append(house_info)
                            print(f"  - {house_info['标题']} ({house_info['价格']})")
                    
                    except Exception as e:
                        print(f"解析房源信息时出错: {e}")
                        continue
                
                time.sleep(2)
                
            except Exception as e:
                print(f"爬取第 {page} 页时出错: {e}")
                continue
    
    def save_to_excel(self, filename='house_data.xlsx'):
        """保存数据到Excel"""
        if not self.houses:
            print("没有爬取到任何房源数据")
            return False
        
        try:
            df = pd.DataFrame(self.houses)
            df.to_excel(filename, index=False)
            print(f"数据已保存到 {filename}")
            print(f"共爬取 {len(self.houses)} 条房源信息")
            return True
        except Exception as e:
            print(f"保存Excel文件时出错: {e}")
            return False
    
    def save_to_json(self, filename='house_data.json'):
        """保存数据到JSON"""
        if not self.houses:
            return False
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.houses, f, ensure_ascii=False, indent=2)
            print(f"数据已保存到 {filename}")
            return True
        except Exception as e:
            print(f"保存JSON文件时出错: {e}")
            return False
    
    def analyze_data(self):
        """分析房源数据"""
        if not self.houses:
            print("没有数据可分析")
            return
        
        print("\n=== 房源数据分析 ===")
        print(f"总房源数: {len(self.houses)}")
        
        # 价格分析
        prices = []
        for house in self.houses:
            price_text = house['价格']
            try:
                # 提取数字
                price_num = int(''.join(filter(str.isdigit, price_text)))
                prices.append(price_num)
            except:
                continue
        
        if prices:
            print(f"平均价格: {sum(prices)/len(prices):.0f}元")
            print(f"最高价格: {max(prices)}元")
            print(f"最低价格: {min(prices)}元")
        
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
    print("租房信息爬虫")
    print("=" * 50)
    
    crawler = HouseCrawler()
    
    # 爬取多个来源的数据
    crawler.crawl_lianjia('北京', 2)
    crawler.crawl_beike('北京', 2)
    
    # 保存数据
    crawler.save_to_excel()
    crawler.save_to_json()
    
    # 分析数据
    crawler.analyze_data()
    
    print("\n" + "=" * 50)
    print("爬取完成！")
    print("请查看生成的 house_data.xlsx 文件")
    print("=" * 50)

if __name__ == "__main__":
    main() 