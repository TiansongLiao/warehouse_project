from pathlib import Path

# 项目根目录
BASE_DIR = Path(__file__).resolve().parent.parent

# 开发环境的安全密钥（生产环境请更改）
SECRET_KEY = 'django-insecure-your-secret-key'

# 允许访问的主机
DEBUG = True  # 开发环境可为 True，生产环境设置为 False
ALLOWED_HOSTS = ['*']  # 允许所有主机访问，生产环境根据实际情况设置为具体域名或IP地址

# 应用程序定义
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'corsheaders',  # ✅ CORS 中间件已添加
    'django.contrib.staticfiles',
    'rest_framework',  # ✅ DRF 已添加
    'api',  # ✅ API 应用
]

# 中间件
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # 确保在其他中间件之前
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# 根 URL 配置
ROOT_URLCONF = 'warehouse_project.urls'

# 模板配置
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],  # 如果有模板文件，配置文件夹路径
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# WSGI 应用
WSGI_APPLICATION = 'warehouse_project.wsgi.application'

# ✅ MySQL 数据库配置
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # 使用 MySQL
        'NAME': 'warehouse_management',       # 数据库名称
        'USER': 'root',                        # 数据库用户名
        'PASSWORD': 'limanli0266',            # 数据库密码
        'HOST': 'localhost',                   # MySQL 服务器地址
        'PORT': '3306',                        # MySQL 默认端口
    }
}

# 认证配置
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# 国际化配置
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# 静态文件配置
STATIC_URL = 'static/'

# 主键默认字段
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ✅ 配置 DRF
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',  # ⛔ 开发调试用，部署时必须换回 IsAuthenticated
    )
}



# CORS 配置
CORS_ALLOW_ALL_ORIGINS = True  # 允许所有源访问
# 如果想限制访问的源，可以改为以下配置：
# CORS_ALLOWED_ORIGINS = [
#     'http://localhost:3000',
#     'http://127.0.0.1:3000',
# ]
