# NJU_electric
南大宿舍电量记录  

## Usage
- 在`config.json`中配置账户密码(统一身份验证)。
- `python main.py`运行即可，可设置每小时自动运行，即在`crontab -e`中添加以下内容：
	```
	0 * * * * cd path/to/nju_electric && python main.py
	```
- 会将数据保存到`.out`文件中，也会绘制趋势图。