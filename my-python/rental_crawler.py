#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
实用租房信息爬虫
爬取58同城、赶集网等真实租房数据
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import json
from datetime import datetime
import re

class RentalCrawler:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
        self.houses = []
    
    def crawl_58(self, city='重庆', area='沙坪坝区', page_count=3):
        """爬取58同城租房数据"""
        print(f"开始爬取58同城{city}{area}租房信息...")
        
        for page in range(1, page_count + 1):
            try:
                # 58同城租房URL - 重庆沙坪坝
                url = f"https://cq.58.com/chuzu/sha-ping-ba-qu/pn{page}/"
                print(f"正在爬取第 {page} 页...")
                
                response = requests.get(url, headers=self.headers, timeout=10)
                response.encoding = 'utf-8'
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # 查找房源列表
                house_items = soup.select('.property')
                
                for item in house_items:
                    try:
                        # 提取房源信息
                        title_elem = item.select_one('.property-content-title-name')
                        price_elem = item.select_one('.property-price')
                        area_elem = item.select_one('.property-content-info')
                        location_elem = item.select_one('.property-content-info-comm-name')
                        
                        if title_elem:
                            house_info = {
                                '标题': title_elem.text.strip(),
                                '价格': price_elem.text.strip() if price_elem else '价格面议',
                                '面积': self.extract_area(area_elem.text.strip()) if area_elem else '',
                                '位置': location_elem.text.strip() if location_elem else '',
                                '详情': area_elem.text.strip() if area_elem else '',
                                '来源': '58同城',
                                '爬取时间': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            }
                            self.houses.append(house_info)
                            print(f"  - {house_info['标题']} ({house_info['价格']})")
                    
                    except Exception as e:
                        print(f"解析房源信息时出错: {e}")
                        continue
                
                time.sleep(3)  # 避免请求过快
                
            except Exception as e:
                print(f"爬取第 {page} 页时出错: {e}")
                continue
    
    def crawl_ganji(self, city='重庆', area='沙坪坝区', page_count=3):
        """爬取赶集网租房数据"""
        print(f"开始爬取赶集网{city}{area}租房信息...")
        
        for page in range(1, page_count + 1):
            try:
                # 赶集网租房URL - 重庆
                url = f"https://cq.ganji.com/fang1/p{page}/"
                print(f"正在爬取第 {page} 页...")
                
                response = requests.get(url, headers=self.headers, timeout=10)
                response.encoding = 'utf-8'
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # 查找房源列表
                house_items = soup.select('.f-list-item')
                
                for item in house_items:
                    try:
                        # 提取房源信息
                        title_elem = item.select_one('.item-title')
                        price_elem = item.select_one('.item-price')
                        info_elem = item.select_one('.item-desc')
                        
                        if title_elem:
                            house_info = {
                                '标题': title_elem.text.strip(),
                                '价格': price_elem.text.strip() if price_elem else '价格面议',
                                '详情': info_elem.text.strip() if info_elem else '',
                                '来源': '赶集网',
                                '爬取时间': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            }
                            self.houses.append(house_info)
                            print(f"  - {house_info['标题']} ({house_info['价格']})")
                    
                    except Exception as e:
                        print(f"解析房源信息时出错: {e}")
                        continue
                
                time.sleep(3)
                
            except Exception as e:
                print(f"爬取第 {page} 页时出错: {e}")
                continue
    
    def crawl_lianjia(self, city='重庆', area='沙坪坝区', page_count=3):
        """爬取链家租房数据"""
        print(f"开始爬取链家{city}{area}租房信息...")
        
        for page in range(1, page_count + 1):
            try:
                # 链家租房URL - 重庆沙坪坝
                url = f"https://cq.lianjia.com/zufang/sha-ping-ba-qu/pg{page}/"
                print(f"正在爬取第 {page} 页...")
                
                response = requests.get(url, headers=self.headers, timeout=10)
                response.encoding = 'utf-8'
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # 查找房源列表
                house_items = soup.select('.content__list--item')
                
                for item in house_items:
                    try:
                        # 提取房源信息
                        title_elem = item.select_one('.content__list--item--title')
                        price_elem = item.select_one('.content__list--item-price')
                        area_elem = item.select_one('.content__list--item--des')
                        
                        if title_elem:
                            house_info = {
                                '标题': title_elem.text.strip(),
                                '价格': price_elem.text.strip() if price_elem else '价格面议',
                                '详情': area_elem.text.strip() if area_elem else '',
                                '来源': '链家',
                                '爬取时间': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            }
                            self.houses.append(house_info)
                            print(f"  - {house_info['标题']} ({house_info['价格']})")
                    
                    except Exception as e:
                        print(f"解析房源信息时出错: {e}")
                        continue
                
                time.sleep(3)
                
            except Exception as e:
                print(f"爬取第 {page} 页时出错: {e}")
                continue
    
    def crawl_beike(self, city='重庆', area='沙坪坝区', page_count=3):
        """爬取贝壳租房数据"""
        print(f"开始爬取贝壳{city}{area}租房信息...")
        
        for page in range(1, page_count + 1):
            try:
                # 贝壳租房URL - 重庆沙坪坝
                url = f"https://cq.ke.com/zufang/sha-ping-ba-qu/pg{page}/"
                print(f"正在爬取第 {page} 页...")
                
                response = requests.get(url, headers=self.headers, timeout=10)
                response.encoding = 'utf-8'
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # 查找房源列表
                house_items = soup.select('.item')
                
                for item in house_items:
                    try:
                        # 提取房源信息
                        title_elem = item.select_one('.item-title')
                        price_elem = item.select_one('.item-price')
                        info_elem = item.select_one('.item-info')
                        
                        if title_elem:
                            house_info = {
                                '标题': title_elem.text.strip(),
                                '价格': price_elem.text.strip() if price_elem else '价格面议',
                                '详情': info_elem.text.strip() if info_elem else '',
                                '来源': '贝壳',
                                '爬取时间': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            }
                            self.houses.append(house_info)
                            print(f"  - {house_info['标题']} ({house_info['价格']})")
                    
                    except Exception as e:
                        print(f"解析房源信息时出错: {e}")
                        continue
                
                time.sleep(3)
                
            except Exception as e:
                print(f"爬取第 {page} 页时出错: {e}")
                continue
    
    def crawl_anjuke(self, city='重庆', area='沙坪坝区', page_count=3):
        """爬取安居客租房数据"""
        print(f"开始爬取安居客{city}{area}租房信息...")
        
        for page in range(1, page_count + 1):
            try:
                # 安居客租房URL - 重庆沙坪坝
                url = f"https://cq.anjuke.com/community/sha-ping-ba-qu/"
                print(f"正在爬取第 {page} 页...")
                
                response = requests.get(url, headers=self.headers, timeout=10)
                response.encoding = 'utf-8'
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # 查找房源列表
                house_items = soup.select('.list-item')
                
                for item in house_items:
                    try:
                        # 提取房源信息
                        title_elem = item.select_one('.item-title')
                        price_elem = item.select_one('.item-price')
                        info_elem = item.select_one('.item-desc')
                        
                        if title_elem:
                            house_info = {
                                '标题': title_elem.text.strip(),
                                '价格': price_elem.text.strip() if price_elem else '价格面议',
                                '详情': info_elem.text.strip() if info_elem else '',
                                '来源': '安居客',
                                '爬取时间': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            }
                            self.houses.append(house_info)
                            print(f"  - {house_info['标题']} ({house_info['价格']})")
                    
                    except Exception as e:
                        print(f"解析房源信息时出错: {e}")
                        continue
                
                time.sleep(3)
                
            except Exception as e:
                print(f"爬取第 {page} 页时出错: {e}")
                continue
    
    def extract_area(self, text):
        """从文本中提取面积信息"""
        if not text:
            return ''
        
        # 匹配面积模式：如 "2室1厅 80平米"
        area_pattern = r'(\d+)\s*平米'
        match = re.search(area_pattern, text)
        if match:
            return f"{match.group(1)}平米"
        return ''
    
    def extract_price(self, text):
        """从文本中提取价格信息"""
        if not text:
            return ''
        
        # 匹配价格模式：如 "3000元/月"
        price_pattern = r'(\d+)\s*元'
        match = re.search(price_pattern, text)
        if match:
            return f"{match.group(1)}元/月"
        return text
    
    def save_to_excel(self, filename='rental_data.xlsx'):
        """保存数据到Excel"""
        if not self.houses:
            print("没有爬取到任何房源数据")
            return False
        
        try:
            df = pd.DataFrame(self.houses)
            
            # 添加价格分析列
            df['价格数字'] = df['价格'].apply(lambda x: self.extract_price_number(x))
            
            # 按价格排序
            df = df.sort_values('价格数字', ascending=True)
            
            df.to_excel(filename, index=False)
            print(f"数据已保存到 {filename}")
            print(f"共爬取 {len(self.houses)} 条房源信息")
            return True
        except Exception as e:
            print(f"保存Excel文件时出错: {e}")
            return False
    
    def extract_price_number(self, price_text):
        """提取价格数字用于排序"""
        if not price_text or price_text == '价格面议':
            return 0
        
        # 提取数字
        numbers = re.findall(r'\d+', price_text)
        if numbers:
            return int(numbers[0])
        return 0
    
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
            price_num = self.extract_price_number(house['价格'])
            if price_num > 0:
                prices.append(price_num)
        
        if prices:
            print(f"平均价格: {sum(prices)/len(prices):.0f}元/月")
            print(f"最高价格: {max(prices)}元/月")
            print(f"最低价格: {min(prices)}元/月")
            
            # 价格区间分析
            price_ranges = {
                '1000以下': len([p for p in prices if p < 1000]),
                '1000-3000': len([p for p in prices if 1000 <= p < 3000]),
                '3000-5000': len([p for p in prices if 3000 <= p < 5000]),
                '5000以上': len([p for p in prices if p >= 5000])
            }
            
            print("\n价格区间分布:")
            for range_name, count in price_ranges.items():
                if count > 0:
                    print(f"  {range_name}: {count}套")
        
        # 来源统计
        sources = {}
        for house in self.houses:
            source = house['来源']
            sources[source] = sources.get(source, 0) + 1
        
        print("\n来源统计:")
        for source, count in sources.items():
            print(f"  {source}: {count}条")
    
    def find_best_deals(self, max_price=5000, min_area=50):
        """找出性价比高的房源"""
        print(f"\n=== 性价比推荐 (价格<{max_price}元, 面积>{min_area}平米) ===")
        
        good_deals = []
        for house in self.houses:
            price = self.extract_price_number(house['价格'])
            area_text = house.get('面积', '')
            area_match = re.search(r'(\d+)', area_text)
            area = int(area_match.group(1)) if area_match else 0
            
            if price > 0 and price <= max_price and area >= min_area:
                good_deals.append({
                    '房源': house['标题'],
                    '价格': house['价格'],
                    '面积': house.get('面积', ''),
                    '位置': house.get('位置', ''),
                    '来源': house['来源']
                })
        
        if good_deals:
            for i, deal in enumerate(good_deals[:10], 1):  # 显示前10个
                print(f"{i}. {deal['房源']}")
                print(f"   价格: {deal['价格']} | 面积: {deal['面积']} | 位置: {deal['位置']}")
                print(f"   来源: {deal['来源']}")
                print()
        else:
            print("没有找到符合条件的房源")

def main():
    """主函数"""
    print("=" * 50)
    print("重庆沙坪坝区租房信息爬虫")
    print("=" * 50)
    
    crawler = RentalCrawler()
    
    # 爬取多个来源的数据
    print("开始爬取重庆沙坪坝区租房信息...")
    crawler.crawl_58('重庆', '沙坪坝区', 3)
    crawler.crawl_ganji('重庆', '沙坪坝区', 3)
    crawler.crawl_lianjia('重庆', '沙坪坝区', 3)
    crawler.crawl_beike('重庆', '沙坪坝区', 3)
    crawler.crawl_anjuke('重庆', '沙坪坝区', 3)
    
    # 保存数据
    crawler.save_to_excel('重庆沙坪坝租房数据.xlsx')
    
    # 分析数据
    crawler.analyze_data()
    
    # 找出性价比房源（重庆价格相对较低）
    crawler.find_best_deals(max_price=3000, min_area=40)
    
    print("\n" + "=" * 50)
    print("爬取完成！")
    print("请查看生成的 重庆沙坪坝租房数据.xlsx 文件")
    print("=" * 50)

if __name__ == "__main__":
    main() 