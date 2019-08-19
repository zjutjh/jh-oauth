# jh-oauth
第三方应用的oauth2.0授权，含开发者中心和用户授权中心

## 后端

dev: 开发版本请转到分支backend-dev

preview: 测试版本（预览版本）请转到分支backend-preview

stable: 稳定版本请转到分支backend-stable

## 开发说明

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

