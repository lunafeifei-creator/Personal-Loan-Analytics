# 🚀 Streamlit 仪表板运行指南

## ⚡ 快速启动

### 在 PowerShell 中运行：

```powershell
cd "d:\Dubai\assignment\Personal Loan"
&"D:/Dubai/assignment/Personal Loan/.venv/Scripts/python.exe" -m streamlit run streamlit_dashboard.py
```

或者在命令行中运行：
```bash
streamlit run streamlit_dashboard.py
```

**仪表板会自动在浏览器中打开，地址是：http://localhost:8501**

---

## 📊 仪表板功能概览

### 1️⃣ **📊 Overview** - 总体概览
- **关键指标卡片**：总客户数、贷款率、平均收入、信用卡消费
- **快速洞察**：收入、消费、教育的核心发现
- **统计表格**：整体与筛选后的数据对比

### 2️⃣ **📈 Income Analysis** - 收入分析
- **收入分布直方图**：按贷款状态分布
- **箱线图**：收入的四分位数分布
- **收入统计**：贷款vs非贷款客户的详细对比
- **转化率分析**：按收入区间的转化率

### 3️⃣ **💳 Credit Card Analysis** - 信用卡消费分析
- **消费分布**：信用卡月均消费直方图
- **散点图**：收入vs消费的关系
- **异常值检测**：识别VIP高消费客户
- **VIP洞察**：高消费客户的转化率

### 4️⃣ **🎓 Education Analysis** - 教育程度分析
- **按教育水平的转化率**：柱状图比较
- **教育水平的收入分布**：箱线图
- **详细统计**：各教育水平的客户数、转化率、收入

### 5️⃣ **🎪 VIP Segment** - VIP细分分析
- **Tier 1 (VIP)**: 150k+收入、4k+消费、研究生/专业
- **Tier 2 (Core)**: 100-150k收入、2-4k消费、研究生/专业
- **High Spenders**: >5k/月消费的高端客户
- **对比可视化**：三个VIP群体的大小和转化率

### 6️⃣ **🎯 Customer Tiers** - 客户分层模型
- **3层分层**：完整的客户分层模型
- **分布和转化率**：各层的客户数和转化率
- **详细建议**：每层的营销策略和行动方案

### 7️⃣ **📋 Data Explorer** - 数据浏览器
- **原始数据**：查看和下载筛选后的数据
- **统计汇总**：数值统计和按贷款状态的对比
- **相关性矩阵**：变量间的相关性热力图

---

## 🎛️ 侧边栏功能

### 📊 导航部分
- 选择要查看的分析部分（7个选项）

### 🔍 筛选部分
- **收入范围**：$40k - $200k
- **CC消费范围**：$0 - $10k/月
- **教育水平**：本科、研究生、专业（多选）
- **贷款状态**：无贷款、已接受贷款（多选）

### 📈 实时统计
- 筛选后的记录数
- 筛选后的转化率

---

## 💡 使用技巧

### Tip 1: 快速过滤高潜力客户
```
收入: 100-200k
CC消费: 2-10k
教育: 研究生 + 专业
贷款: 显示全部
→ 查看"Customer Tiers"部分
```

### Tip 2: 发现VIP机会
```
CC消费: 5-10k
收入: 任意
教育: 任意
→ 查看"VIP Segment"部分
```

### Tip 3: 验证教育影响
```
教育: 依次选择 "本科" → "研究生" → "专业"
其他: 保持默认
→ 在"Education Analysis"中观察转化率变化
```

### Tip 4: 下载数据进行进一步分析
```
使用任何过滤条件
→ 进入"Data Explorer"
→ 点击"Download filtered data as CSV"
```

---

## 🎯 关键指标解读

### 什么是"好"的转化率？
- **<5%**：较差，不值得追求
- **8-12%**：可接受（Tier 3）
- **15-22%**：很好（Tier 2）
- **>30%**：优秀（Tier 1 和高消费客户）

### 收入的黄金法则
- **<$80k**：跳过
- **$80-120k**：次优先
- **$120-200k**：高优先
- **>$150k**：最高优先

### 消费能力指标
- **<$1k/月**：低购买力
- **$1-2k/月**：中等购买力
- **$2-4k/月**：活跃消费者
- **>$5k/月**：VIP/高消费

---

## 🔧 故障排除

### 问题1: "No module named 'streamlit'"
**解决**：重新安装依赖
```powershell
&"D:/Dubai/assignment/Personal Loan/.venv/Scripts/python.exe" -m pip install streamlit plotly
```

### 问题2: 仪表板加载缓慢
**解决**：数据已被缓存，刷新浏览器。首次加载需要几秒。

### 问题3: 某个图表显示不出来
**解决**：检查该节点的过滤条件是否结果为0。调整过滤器。

### 问题4: 下载CSV失败
**解决**：确保有足够的磁盘空间，或尝试刷新页面。

---

## 📱 浏览器兼容性

**推荐**：
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

**分辨率**：最佳体验 1920x1080 或以上

---

## ⚙️ 配置和自定义

### 修改筛选范围
编辑 `streamlit_dashboard.py` 的第 50-70 行：
```python
income_range = st.sidebar.slider(
    "Income Range ($k):",
    int(df['Income'].min()),
    int(df['Income'].max()),
    (40, 200)  # ← 修改这里的默认范围
)
```

### 修改颜色方案
查找 `color_discrete_map` 或 `color_continuous_scale`，修改颜色值。

### 添加新的分析部分
在导航菜单中添加选项，然后添加相应的 `elif section == "..."` 块。

---

## 📊 数据更新

### 更新仪表板数据：

1. 将新的 Excel 文件放在同一目录
2. 确保格式与原始文件相同
3. 重启 Streamlit 应用

**或者**：修改第 17 行的文件路径：
```python
df = pd.read_excel('新文件名.xls', sheet_name='Data', header=3)
```

---

## 🎬 实际使用场景

### 场景1：营销主管想看整体情况
1. 打开仪表板
2. 查看 **Overview** 部分
3. 查看 **Customer Tiers** 部分
4. 5分钟内获得完整认识

### 场景2：销售经理想找到目标客户
1. 在侧边栏设置 Tier 1 的过滤条件
2. 进入 **Data Explorer** → **Raw Data**
3. 下载 CSV 文件给销售团队
4. 使用下载的数据进行精准跟进

### 场景3：数据分析师想要深度分析
1. 在 **Data Explorer** 中查看所有统计
2. 查看相关性矩阵
3. 根据需要下载数据
4. 在外部工具（Python/R/SQL）中继续分析

### 场景4：市场部想要验证假设
1. 应用特定过滤条件
2. 观察各个分析部分的数据变化
3. 对比转化率和特征
4. 保存或记录重要发现

---

## 💾 导出和共享

### 生成报告
1. 在浏览器中按 `F12` 打开开发者工具
2. 或使用浏览器的"打印"功能 (Ctrl+P)
3. 保存为 PDF

### 共享仪表板
- 在网络共享驱动器中运行此仪表板
- 让团队成员访问该驱动器
- 他们可以运行 `streamlit run streamlit_dashboard.py` 打开仪表板

---

## 📚 相关文档

这个 Streamlit 仪表板补充了：
- **Personal_Loan_Marketing_Dashboard.png** - 静态仪表板
- **Quick_Reference_Guide.md** - 决策规则
- **Marketing_Analysis_Report_EN/CN.md** - 详细分析

---

## ❓ 常见问题

**Q: 仪表板可以离线使用吗？**  
A: 需要互联网连接来加载 Plotly 库，但数据本地存储。

**Q: 可以添加更多数据吗？**  
A: 可以，确保格式一致，修改文件路径即可。

**Q: 性能如何？**  
A: 5,000条记录，快速响应。100,000+条记录可能需要优化。

**Q: 可以设置密码保护吗？**  
A: 建议使用云部署平台（如 Streamlit Cloud、Heroku）来实现。

---

## 🚀 下一步

1. **运行仪表板**：按照快速启动步骤运行
2. **探索数据**：使用不同的过滤条件
3. **分享发现**：使用截图或 PDF 与团队分享
4. **采取行动**：根据 Tier 制定营销策略

---

*Streamlit Dashboard - Universal Bank Personal Loan Analytics*  
*Last Updated: December 16, 2025*
