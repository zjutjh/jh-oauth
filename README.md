# jh-oauth
第三方应用的oauth2.0授权，含开发者中心和用户授权中心

dev: 开发版本请转到分支dev

preview: 测试版本（预览版本）请转到分支preview

stable: 稳定版本请转到分支stable

## 开发说明

前端应用代码请写在目录front内，后端代码写在backend内。

请注意，首次创建应用是请手动更新.gitignore文件，并做相应的文件配置声明

### 导出依赖包

```python
pip freeze > requirements.txt
```

### 配置开发环境

#### 创建虚拟环境

设置Project Interperter（推荐使用虚拟环境）

#### 初始化依赖和数据库

```python
pip install ./requirement.txt  # 安装依赖
python manage.py migrate  # 完成数据库的创建
```
#### 创建启动模板

当你使用PyCharm时，可使用Django server作为应用启动模板

