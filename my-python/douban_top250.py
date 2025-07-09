#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
豆瓣电影 Top 250 爬虫
作者：Python 初学者
功能：爬取豆瓣电影 Top 250 信息并保存为 Excel 文件
"""

import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook
import time
import sys

def get_movie_data():
    """爬取豆瓣电影 Top 250 数据"""
    movies = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    print("开始爬取豆瓣电影 Top 250...")
    
    # 豆瓣 Top 250 分页，每页 25 部电影
    for page in range(10):  # 10 页，每页 25 部 = 250 部
        start = page * 25
        url = f'https://movie.douban.com/top250?start={start}'
        
        try:
            print(f"正在爬取第 {page + 1} 页...")
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()  # 检查请求是否成功
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 查找所有电影条目
            movie_items = soup.select('.item')
            
            for item in movie_items:
                try:
                    # 提取电影标题
                    title_element = item.select_one('.title')
                    title = title_element.text if title_element else "未知标题"
                    
                    # 提取评分
                    rating_element = item.select_one('.rating_num')
                    rating = rating_element.text if rating_element else "暂无评分"
                    
                    # 提取链接
                    link_element = item.select_one('a')
                    link = link_element['href'] if link_element else ""
                    
                    # 提取导演和年份信息
                    info_element = item.select_one('.bd p')
                    info = info_element.text.strip() if info_element else ""
                    
                    movies.append([title, rating, link, info])
                    
                except Exception as e:
                    print(f"解析电影信息时出错: {e}")
                    continue
            
            # 添加延迟，避免请求过于频繁
            time.sleep(1)
            
        except requests.RequestException as e:
            print(f"请求第 {page + 1} 页时出错: {e}")
            continue
        except Exception as e:
            print(f"处理第 {page + 1} 页时出错: {e}")
            continue
    
    print(f"爬取完成！共获取 {len(movies)} 部电影信息")
    return movies

def save_to_excel(movies, filename='douban_top250.xlsx'):
    """保存电影数据到 Excel 文件"""
    try:
        wb = Workbook()
        ws = wb.active
        ws.title = "豆瓣 Top 250"
        
        # 添加表头
        headers = ['排名', '电影名称', '评分', '链接', '导演/年份信息']
        ws.append(headers)
        
        # 添加数据
        for i, movie in enumerate(movies, 1):
            row = [i] + movie
            ws.append(row)
        
        # 调整列宽
        ws.column_dimensions['A'].width = 8
        ws.column_dimensions['B'].width = 30
        ws.column_dimensions['C'].width = 10
        ws.column_dimensions['D'].width = 50
        ws.column_dimensions['E'].width = 40
        
        # 保存文件
        wb.save(filename)
        print(f"数据已保存到 {filename}")
        return True
        
    except Exception as e:
        print(f"保存 Excel 文件时出错: {e}")
        return False

def main():
    """主函数"""
    print("=" * 50)
    print("豆瓣电影 Top 250 爬虫")
    print("=" * 50)
    
    # 爬取数据
    movies = get_movie_data()
    
    if not movies:
        print("未获取到任何电影数据，程序退出")
        sys.exit(1)
    
    # 保存到 Excel
    if save_to_excel(movies):
        print("程序执行完成！")
        print(f"共爬取了 {len(movies)} 部电影信息")
        print("请查看生成的 douban_top250.xlsx 文件")
    else:
        print("保存文件失败")

if __name__ == "__main__":
    main() 