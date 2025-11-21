import altair as alt
import numpy as np
import pandas as pd
import streamlit as st
from datetime import datetime, timedelta

# 设置页面配置
st.set_page_config(page_title="多角色动态权限系统", layout="wide")

# 初始化会话状态
if 'role' not in st.session_state:
    st.session_state.role = '管理员'  # 默认角色为管理员
if 'filters' not in st.session_state:
    st.session_state.filters = {
        '管理员': {'date_range': None, 'categories': [], 'keyword': ''},
        '普通用户': {'date_range': None, 'categories': [], 'keyword': ''},
        '访客': {'date_range': None, 'categories': [], 'keyword': ''}
    }

# 创建示例数据集
np.random.seed(42)
dates = pd.date_range(start='2023-01-01', end='2023-12-31', periods=100)
categories = ['分类A', '分类B', '分类C', '分类D', '分类E']
products = [f'产品{i}' for i in range(1, 21)]

data = {
    '日期': dates,
    '分类': np.random.choice(categories, size=100),
    '产品': np.random.choice(products, size=100),
    '销售额': np.random.randint(1000, 10000, size=100),
    '利润': np.random.randint(100, 2000, size=100)
}

df = pd.DataFrame(data)

# 侧边栏：角色选择
st.sidebar.header("角色管理")
role_options = ['管理员', '普通用户', '访客']
selected_role = st.sidebar.selectbox(
    "选择您的角色",
    role_options,
    index=role_options.index(st.session_state.role)
)

# 切换角色时更新会话状态，但不刷新页面
if selected_role != st.session_state.role:
    st.session_state.role = selected_role

# 侧边栏：智能筛选面板
st.sidebar.header("智能筛选")

# 获取当前角色的筛选状态
current_filters = st.session_state.filters[st.session_state.role]

# 日期范围选择（仅管理员可见）
if st.session_state.role == '管理员':
    # 获取当前筛选器中的日期范围，如果存在则转换为date类型
    default_date_range = current_filters['date_range']
    if default_date_range and len(default_date_range) == 2:
        default_date_range = (default_date_range[0].date(), default_date_range[1].date())
    else:
        default_date_range = (df['日期'].min().date(), df['日期'].max().date())
    
    date_range = st.sidebar.date_input(
        "选择日期范围",
        value=default_date_range,
        min_value=df['日期'].min().date(),
        max_value=df['日期'].max().date()
    )
    # 将date类型转换为datetime64[ns]类型并保存到会话状态
    if date_range and len(date_range) == 2:
        current_filters['date_range'] = (pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1]))
    else:
        current_filters['date_range'] = None
else:
    date_range = current_filters['date_range']

# 多选分类标签（管理员和普通用户可见）
if st.session_state.role in ['管理员', '普通用户']:
    selected_categories = st.sidebar.multiselect(
        "选择分类",
        options=categories,
        default=current_filters['categories']
    )
    current_filters['categories'] = selected_categories
else:
    selected_categories = current_filters['categories']

# 实时关键词搜索框（所有角色可见）
keyword = st.sidebar.text_input(
    "关键词搜索（产品名称）",
    value=current_filters['keyword'],
    placeholder="输入产品名称关键词"
)
current_filters['keyword'] = keyword

# 更新会话状态中的筛选器
st.session_state.filters[st.session_state.role] = current_filters

# 应用筛选条件
filtered_df = df.copy()

# 应用日期筛选
if date_range and len(date_range) == 2:
    start_date, end_date = date_range
    # 将date类型转换为datetime64[ns]类型，确保类型匹配
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    filtered_df = filtered_df[(filtered_df['日期'] >= start_date) & (filtered_df['日期'] <= end_date)]

# 应用分类筛选
if selected_categories:
    filtered_df = filtered_df[filtered_df['分类'].isin(selected_categories)]

# 应用关键词筛选
if keyword:
    filtered_df = filtered_df[filtered_df['产品'].str.contains(keyword, case=False)]

# 主页面内容
st.title("多角色动态权限系统演示")

# 显示当前角色
st.write(f"当前角色：**{st.session_state.role}**")

# 显示筛选状态
st.subheader("筛选状态")
filter_info = []
if date_range and len(date_range) == 2:
    filter_info.append(f"日期范围：{date_range[0]} 至 {date_range[1]}")
if selected_categories:
    filter_info.append(f"分类：{', '.join(selected_categories)}")
if keyword:
    filter_info.append(f"关键词：{keyword}")

if filter_info:
    st.write("\n".join(filter_info))
else:
    st.write("未应用任何筛选条件，显示原始数据")

# 显示数据
st.subheader("数据展示")
st.dataframe(filtered_df, use_container_width=True)

# 数据可视化
st.subheader("数据可视化")

# 销售额趋势图
if not filtered_df.empty:
    sales_chart = alt.Chart(filtered_df).mark_line().encode(
        x='日期:T',
        y='销售额:Q',
        color='分类:N'
    ).properties(
        width=800,
        height=400
    )
    st.altair_chart(sales_chart, use_container_width=True)

    # 分类销售额占比
    category_sales = filtered_df.groupby('分类')['销售额'].sum().reset_index()
    pie_chart = alt.Chart(category_sales).mark_arc().encode(
        theta='销售额:Q',
        color='分类:N',
        tooltip=['分类', '销售额']
    ).properties(
        width=400,
        height=400
    )
    st.altair_chart(pie_chart, use_container_width=True)
