from app import db #db是在app/__init__.py生成的关联后的SQLAlchemy实例
import datetime
from sqlalchemy.sql.sqltypes import DECIMAL
from sqlalchemy.orm import relationship,backref
class parent():
    def as_dict(self):
        result = {}
        for c in self.__table__.columns:
            if c.name == "lastModifiedDate" or c.name == "pickupTime":
                epoch = datetime.datetime.utcfromtimestamp(0)
                # mysql_time_struct = time.strptime(getattr(self, c.name), '%Y-%m-%d %H:%M:%S')
                if getattr(self, c.name) != None:
                    result[c.name] = (getattr(self, c.name) - epoch).total_seconds() * 1000.0
            
            elif isinstance(c.type, db.Numeric):
                # c.type.asdecimal = False
                result[c.name] = float(getattr(self, c.name))
             
            else:
                result[c.name] =  getattr(self, c.name) 
        return result

class Item(db.Model,parent):
    __tablename__ = 'item'
    id = db.Column(db.String(40), primary_key=True)
    company = db.Column(db.String(320),  nullable=False)
    modelNumber = db.Column(db.String(320), nullable=False)
    productType = db.Column(db.String(320), nullable=False)
    lastModifiedDate = db.Column(db.DateTime)
    info = db.Column(db.String(320))
    # 应该default为0还是1呢？
    stockNumber = db.Column(db.Integer, nullable=False,  default=0)
    location = db.Column(db.String(80))
    __table_args__ = (db.UniqueConstraint( 'modelNumber', "company", name='_company_modelNumber_uc'),)

    def __repr__(self):
        return '<{}, {}, {},>'.format(self.id, self.company, self.modelNumber)

    # def as_dict(self):
    #     result = {}
    #     for c in self.__table__.columns:
    #         if c.name == "lastModifiedDate":
    #             epoch = datetime.datetime.utcfromtimestamp(0)
    #             # mysql_time_struct = time.strptime(getattr(self, c.name), '%Y-%m-%d %H:%M:%S')
    #             if getattr(self, c.name) != None:
    #                 result[c.name] = (getattr(self, c.name) - epoch).total_seconds() * 1000.0
                
    #         else:
    #             result[c.name] =  getattr(self, c.name) 
    #     return result
    
class PendingDetail(db.Model,parent):
    __tablename__ = 'Pending_detail'
     
   
    id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    itemID = db.Column(db.String(320),  nullable=False)
    company = db.Column(db.String(320),  nullable=False)
    modelNumber = db.Column(db.String(320), nullable=False)
    productType = db.Column(db.String(320), nullable=False)
    lastModifiedDate = db.Column(db.DateTime)
    info = db.Column(db.String(320))
    amount = db.Column(db.Integer, nullable=False)
    # location = db.Column(db.String(80))
    
    #出库单号
    pending_id = db.Column(db.ForeignKey(u'pending_location.id'), index=True)
    pendingLocation = relationship(u'PendingLocation',backref=backref('Pending_detail'))



class PendingLocation(db.Model,parent):
    __tablename__ = 'pending_location'
    #出库单号
    id = db.Column(db.String(60), primary_key=True)
    location = db.Column(db.String(80))
    pickupTime = db.Column(db.DateTime)

   
class SaleC(db.Model, parent):
    __tablename__ = 'sale_c'
    __bind_key__ = 'DB2019'
    sc_id = db.Column(db.String(60), primary_key=True)
    sc_code = db.Column(db.String(50))
    sc_sign_date = db.Column(db.DateTime) 
    sc_appd_date = db.Column(db.DateTime) 
    sc_ship_period = db.Column(db.Integer) 
    sc_item_in = db.Column(db.DECIMAL(11,1))
    sc_item_out = db.Column(db.DECIMAL(11,1))
    sc_receive_company = db.Column(db.String(50))
    sc_sponsor =  db.Column(db.String(50))
    sc_item_summoney = db.Column(db.DECIMAL(11,1))

    sc_reca_money = db.Column(db.DECIMAL(11,1))
    sc_recr_money = db.Column(db.DECIMAL(11,1))

class ItemIn(db.Model, parent):
    __tablename__ = 'item_in'
    __bind_key__ = 'ItemStorage'
    in_id = db.Column(db.String(60), primary_key=True)
    sc_code = db.Column(db.String(50))
    in_arrive_date = db.Column(db.DateTime)
    
    in_item_brand1 = db.Column(db.String(50))  #13入库产品品牌1 
    in_item_name1 = db.Column(db.String(50))    #14入库产品名称1 
    in_item_model1 = db.Column(db.String(120))	#15入库产品型号1  
    in_item_parameter1 = db.Column(db.String(50))	#16规格参数1  
    in_item_number1 = db.Column(db.Integer) #17入库产品数量1
    in_item_price1 =  db.Column(db.DECIMAL(8,2))	#18入库产品单价1
    
    in_item_brand2 = db.Column(db.String(50))  #13入库产品品牌1 
    in_item_name2 = db.Column(db.String(50))    #14入库产品名称1 
    in_item_model2 = db.Column(db.String(120))	#15入库产品型号1  
    in_item_parameter2 = db.Column(db.String(50))	#16规格参数1  
    in_item_number2 = db.Column(db.Integer) #17入库产品数量1
    in_item_price2 =  db.Column(db.DECIMAL(8,2))	#18入库产品单价1


    in_item_brand3 = db.Column(db.String(50))  #13入库产品品牌1 
    in_item_name3 = db.Column(db.String(50))    #14入库产品名称1 
    in_item_model3 = db.Column(db.String(120))	#15入库产品型号1  
    in_item_parameter3 = db.Column(db.String(50))	#16规格参数1  
    in_item_number3 = db.Column(db.Integer) #17入库产品数量1
    in_item_price3 =  db.Column(db.DECIMAL(8,2))	#18入库产品单价1
    
    in_item_brand4 = db.Column(db.String(50))  #13入库产品品牌1 
    in_item_name4 = db.Column(db.String(50))    #14入库产品名称1 
    in_item_model4 = db.Column(db.String(120))	#15入库产品型号1  
    in_item_parameter4 = db.Column(db.String(50))	#16规格参数1  
    in_item_number4 = db.Column(db.Integer) #17入库产品数量1
    in_item_price4 =  db.Column(db.DECIMAL(8,2))	#18入库产品单价1

    in_item_brand5 = db.Column(db.String(50))  #13入库产品品牌1 
    in_item_name5 = db.Column(db.String(50))    #14入库产品名称1 
    in_item_model5 = db.Column(db.String(120))	#15入库产品型号1  
    in_item_parameter5 = db.Column(db.String(50))	#16规格参数1  
    in_item_number5 = db.Column(db.Integer) #17入库产品数量1
    in_item_price5 =  db.Column(db.DECIMAL(8,2))	#18入库产品单价1

class ItemOut(db.Model,parent):
    __bind_key__ = 'ItemStorage'
    __tablename__ = 'item_out'
    
    out_id = db.Column(db.String(11), primary_key=True)
    out_page_number = db.Column(db.Integer)
    out_code = db.Column(db.String(50))
    sc_code = db.Column(db.String(50))
    sc_receive_company = db.Column(db.String(50))
    sc_reccom_tel = db.Column(db.String(25))
    sc_sponsor = db.Column(db.String(12)) #7销售合同主管人 	
    out_ship_date = db.Column(db.DateTime) #8发货日期
    out_ship_way = db.Column(db.String(100)) #9发货方式
    out_ship_fee = db.Column(db.DECIMAL(8,2))  #10发货运费
    out_ship_address = db.Column(db.String(200))   #11发货地址	 
    out_ship_man = db.Column(db.String(12))    #12发货人
    # out_ship_settle_method = db.Column(db.String(100)) #13发货结算方式 
    # out_ship_settle_date = db.Column(db.DateTime)
    out_item_brand1 = db.Column(db.String(50))	 #15出库产品品牌1		 
    out_item_name1 = db.Column(db.String(50))	 #16出库产品名称1		 
    out_item_model1 = db.Column(db.String(120)) #17出库产品型号1		 
    out_item_parameter1 = db.Column(db.String(50)) #18规格参数1		 
    out_item_number1 = db.Column(db.Integer) #19出库产品数量1	 
    sc_item_price1 = db.Column(db.DECIMAL(11,2)) #20销售单价1
    
    out_item_brand2 = db.Column(db.String(50))	 #15出库产品品牌1		 
    out_item_name2 = db.Column(db.String(50))	 #16出库产品名称1		 
    out_item_model2 = db.Column(db.String(120)) #17出库产品型号1		 
    out_item_parameter2 = db.Column(db.String(50)) #18规格参数1		 
    out_item_number2 = db.Column(db.Integer) #19出库产品数量1	 
    sc_item_price2 = db.Column(db.DECIMAL(11,2)) #20销售单价1

    out_item_brand3 = db.Column(db.String(50))	 #15出库产品品牌1		 
    out_item_name3 = db.Column(db.String(50))	 #16出库产品名称1		 
    out_item_model3 = db.Column(db.String(120)) #17出库产品型号1		 
    out_item_parameter3 = db.Column(db.String(50)) #18规格参数1		 
    out_item_number3 = db.Column(db.Integer) #19出库产品数量1	 
    sc_item_price3 = db.Column(db.DECIMAL(11,2)) #20销售单价1

    
    out_item_brand4 = db.Column(db.String(50))	 #15出库产品品牌1		 
    out_item_name4 = db.Column(db.String(50))	 #16出库产品名称1		 
    out_item_model4 = db.Column(db.String(120)) #17出库产品型号1		 
    out_item_parameter4 = db.Column(db.String(50)) #18规格参数1		 
    out_item_number4 = db.Column(db.Integer) #19出库产品数量1	 
    sc_item_price4 = db.Column(db.DECIMAL(11,2)) #20销售单价1

    out_item_brand5 = db.Column(db.String(50))	 #15出库产品品牌1		 
    out_item_name5 = db.Column(db.String(50))	 #16出库产品名称1		 
    out_item_model5 = db.Column(db.String(120)) #17出库产品型号1		 
    out_item_parameter5 = db.Column(db.String(50)) #18规格参数1		 
    out_item_number5 = db.Column(db.Integer) #19出库产品数量1	 
    sc_item_price5 = db.Column(db.DECIMAL(11,2)) #20销售单价1
    
    def __repr__(self):
        return '<{}, {}, {},>'.format(self.out_id, self.out_code, self.sc_receive_company)

    # def as_dict(self):
    #     result = {}
    #     for c in self.__table__.columns:
    #         if isinstance(c.type, db.Numeric):
    #             # c.type.asdecimal = False
    #             result[c.name] = float(getattr(self, c.name))
    #         else:
    #             result[c.name] = getattr(self, c.name) 
    #     return result

#     def __repr__(self):
#         return '<User %r>' % self.username
