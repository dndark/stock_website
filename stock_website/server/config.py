
import os
class Config:
    """默认配置 主要是对数据库进行相关配置
    对象关系映射（Object Relational Mapping，简称ORM）是通过使用描述对象和数据库之间映射的元数据，
    将面向对象语言程序中的对象自动持久化到关系数据库中。
    这样，我们在具体的操作业务对象的时候，就不需要再去和复杂的SQL语句打交道，只要像平时操作对象一样操作它就可以了。
　　ORM框架就是用于实现ORM技术的程序。
    SQLAlchemy是Python编程语言下的一款开源软件。提供了SQL工具包及对象关系映射（ORM）工具，使用MIT许可证发行。
    
    SQLAlchmey采用了类似于Java里Hibernate的数据映射模型，
    """
    FLATPAGES_AUTO_RELOAD = True
    FLATPAGES_EXTENSION = '.md'
    # SECRET_KEY = os.environ.get('SECRET_KEY') or 'can you guess it'
    DEBUG = True
    # sqlalchemy两个主要配置
    # ORM底层所访问数据库URI
    # SQLALCHEMY_DATABASE_URI =  'mysql+pymysql://root:admin@localhost:3306/test?charset=utf8'
    # 当关闭数据库是否自动提交事务
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    # 是否追踪修改
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    @staticmethod
    def init_app(app):
        # app.logger.setLevel(logging.DEBUG)
        # app.logger.addHandler(get_handler)
        pass


class DevelopmentConfig(Config):
    """开发环境配置
    """

    #可以通过修改SQLALCHEMY_DATABASE_URI来控制访问不同数据库
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@localhost:3306/test?charset=utf8'
    SQLALCHEMY_BINDS = {
        'ItemStorage': 'mysql+pymysql://root:root@localhost:3306/run_admin_itemstorage?charset=utf8',
        'DB2019': 'mysql+pymysql://root:root@localhost:3306/run_admin_2019?charset=utf8',
        'DB2018': 'mysql+pymysql://root:root@localhost:3306/run_admin_2018?charset=utf8',
    }
    

class ProductionConfig(Config):
    """生产环境
    """
    #可以通过修改SQLALCHEMY_DATABASE_URI来控制访问不同数据库
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:fengjunguo@192.168.1.223:3306/test?charset=utf8'
    SQLALCHEMY_BINDS = {
        'ItemStorage': 'mysql+pymysql://root:fengjunguo@192.168.1.223:3306/run_admin_itemstorage?charset=utf8',
        'DB2019': 'mysql+pymysql://root:fengjunguo@192.168.1.223:3306/run_admin_db_2019?charset=utf8',
        'DB2018': 'mysql+pymysql://root:fengjunguo@192.168.1.223:3306/run_admin_db_2018?charset=utf8',
    }


# 设置配置映射
config = {
    'production': DevelopmentConfig,
    'default': DevelopmentConfig
    # 'ItemStorage':ItemStorage
}