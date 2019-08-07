from app import app, db, db2018, db2017
from .models import Item, ItemOut, ItemIn,  PendingDetail, PendingLocation
from .models import SaleC, SaleC2018, SaleC2017
from .models import UnpaySaleStatus, UnpaySaleStatus2018, UnpaySaleStatus2017
from datetime import datetime, timedelta

import random
from flask import jsonify, request, abort, make_response
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import or_, and_

#####Overdue Item
@app.route('/OverDueItem', methods=['GET'])
def OverDueItem():
    result = []
    now = created_at = datetime.now().date()
    _90DayAgo = now - timedelta(days=90)
    
    # optional argument 
    year = request.args.get('year')

    if year == "2018":
        Sale_c = SaleC2018
    else:
        Sale_c = SaleC

    # fromDate = datetime.strftime(_90DayAgo, '%Y-%m-%d')
    items = Sale_c.query.filter(and_(Sale_c.sc_appd_date <= _90DayAgo, 
                                    Sale_c.sc_item_in > 99, 
                                    Sale_c.sc_item_out < 99, 
                                    Sale_c.sc_receive_company != "北京康瑞明科技有限公司")).all()
 
    for i in range(len(items)):
        items[i] = items[i].as_dict()
        # use sc_rec_money to replace sc_reca_money and sc_recr_money
        items[i]["sc_rec_money"] = items[i]["sc_reca_money"] + items[i]["sc_recr_money"]
        if (items[i]["sc_item_summoney"] == 0):
            items[i]["sc_recr_money_prec"] = 0
        else:
            items[i]["sc_recr_money_prec"] = items[i]["sc_rec_money"]/(items[i]["sc_item_summoney"])
        items[i].pop("sc_reca_money")
        items[i].pop("sc_recr_money")
    # return make_response(jsonify(items))
    return make_response(jsonify(items))

@app.route('/unPayItems', methods=['GET'])
def unPayItems():
    # optional argument 
    year = request.args.get('year')
    is_handled = request.args.get('handled')
    is_progress = request.args.get('progress')
    name = request.args.get('name', "所有人")

    #set db sale_c = SaleC
    sale_c = SaleC
    unpay_sale_status = UnpaySaleStatus
    if year == "2018":
        sale_c = SaleC2018
        unpay_sale_status = UnpaySaleStatus2018
        
    query = db.session().query(sale_c, unpay_sale_status)
    sale_c_joined = query.outerjoin(unpay_sale_status, sale_c.sc_code==unpay_sale_status.sc_code)

    handle_query = or_(unpay_sale_status.handled == 0, unpay_sale_status.handled == None)
    
    #handle status    
    # if handle == NONE mean not set in the unpay table
    # handle_query = or_(unpay_sale_status.handled == None)
    if is_progress: handle_query = unpay_sale_status.handled == 5 
    if is_handled: handle_query = unpay_sale_status.handled == 10
    
    # this is just a placeholder, just execute the handle_query twice
    
    name_query = sale_c.sc_sponsor is not None
    if name != "所有人": 
        name_query = sale_c.sc_sponsor == name

    result = []
    except_companys = ["北京康瑞明科技有限公司", "太原重工股份有限公司","泰安航天特种车有限公司"]
    now = datetime.now().date()
    _60DaysAgo = now - timedelta(days=60)
    items = sale_c_joined.filter(and_(
                                    #没收全
                                    #sale_c.sc_reca_money+ sale_c.sc_recr_money < sale_c.sc_item_summoney,
                                    #收了不到百分80
                                    sale_c.sc_reca_money+ sale_c.sc_recr_money <  sale_c.sc_item_summoney*0.98,
                                    name_query,
                                    # 出货超过百分99
                                    #  SaleC.sc_item_out >= 99, 
                                    # 大于60天交货期
                                    sale_c.sc_appd_date < _60DaysAgo,
                                    handle_query,
                                    sale_c.sc_receive_company.notin_(except_companys))).all()

    items2=[]
    unpay_d = {"handled": None,  "id": None, "remark": None }
    for x in items:
        d = x[0].as_dict()
        d.update(x[1].as_dict()) if x[1] else d.update(unpay_d)
        
        rec_money = d["sc_rec_money"] = d["sc_reca_money"] + d["sc_recr_money"]
        sc_recr_money_prec = 0 if (rec_money == 0) else rec_money/(d["sc_item_summoney"])
        d["sc_recr_money_prec"] = sc_recr_money_prec
        d.pop("sc_reca_money")
        d.pop("sc_recr_money")

        items2.append(d)
    return make_response(jsonify(items2))


@app.route('/paiedItems', methods=['GET'])
def paiedItems():
    # optional argument 
    year = request.args.get('year')    
    name = request.args.get('name', "所有人")

    items2 = []

    #set db sale_c = SaleC
    sale_c = SaleC
    unpay_sale_status = UnpaySaleStatus
    if year == "2018":
        sale_c = SaleC2018
        unpay_sale_status = UnpaySaleStatus2018
        
    query = db.session().query(sale_c, unpay_sale_status)
    sale_c_joined = query.outerjoin(sale_c, unpay_sale_status.sc_code==sale_c.sc_code)

    # handle_query = or_(unpay_sale_status.handled != 0)
    
    #handle status 
    name_query = sale_c.sc_sponsor is not None
    if name != "所有人": 
        name_query = sale_c.sc_sponsor == name

    result = []
    except_companys = ["北京康瑞明科技有限公司", "太原重工股份有限公司","泰安航天特种车有限公司"]
    now = datetime.now().date()
    _60DaysAgo = now - timedelta(days=60)
    items = sale_c_joined.filter(and_(
                                    #没收全
                                    # sale_c.sc_reca_money+ sale_c.sc_recr_money < sale_c.sc_item_summoney,
                                    #收了超过百分80
                                    sale_c.sc_reca_money+ sale_c.sc_recr_money > sale_c.sc_item_summoney*0.98,
                                    name_query,
                                    # 出货超过百分99
                                    #  SaleC.sc_item_out >= 99, 
                                    # 大于60天交货期
                                    sale_c.sc_appd_date < _60DaysAgo,
                                    # handle_query,
                                    sale_c.sc_receive_company.notin_(except_companys)
                                    )).all()
    for x in items:
        d = x[0].as_dict()
        d.update(x[1].as_dict())
        rec_money = d["sc_rec_money"] = d["sc_reca_money"] + d["sc_recr_money"]
        sc_recr_money_prec = 0 if (rec_money == 0) else rec_money/(d["sc_item_summoney"])
        d["sc_recr_money_prec"] = sc_recr_money_prec
        d.pop("sc_reca_money")
        d.pop("sc_recr_money")

        items2.append(d)
    return make_response(jsonify(items2))


@app.route('/unPayItem', methods=['GET'])
def unPayItem():
    # optional argument 
    sc_code = request.args.get('sc_code')
    # result = []
    if not sc_code:
        return abort(404)
    
    year = sc_code.split("-")[0]
    sale_c = SaleC
    unpay_sale_status = UnpaySaleStatus

    if year == "2018":
        sale_c = SaleC2018
        unpay_sale_status = UnpaySaleStatus2018
        
    
    query = db.session().query(sale_c, unpay_sale_status)
    sale_c_joined = query.outerjoin(unpay_sale_status, sale_c.sc_code==unpay_sale_status.sc_code)

    result = []
    now = datetime.now().date()
    _60DaysAgo = now - timedelta(days=60)
    item = sale_c_joined.filter(sale_c.sc_code == sc_code).first_or_404()

    unpay_d = {"handled": None,  "id": None, "remark": None }
    print(item)
    d = item[0].as_dict()
    d.update(item[1].as_dict()) if item[1] else d.update(unpay_d)
    rec_money = d["sc_rec_money"] = d["sc_reca_money"] + d["sc_recr_money"]
    d["sc_recr_money_prec"] = 0 if (rec_money == 0) else rec_money/(d["sc_item_summoney"])

    return make_response(jsonify(d))

@app.route('/updateUnPayItem', methods=['POST'])
def updateUnPayItem():
    now = datetime.now()
    post_data = request.get_json()
    # for item in post_data:
        # don't set the stockNumber when user first input it 
    remark = post_data.get("remark",'')
    sc_code = post_data.get("sc_code")
    handle_score = post_data.get("handle_score",0)

    year = sc_code.split("-")[0]
    
    unpay_sale_status = UnpaySaleStatus
    _db = db
    if year == "2018":
        unpay_sale_status = UnpaySaleStatus2018
        _db = db2018
    
    result = unpay_sale_status.query.filter(unpay_sale_status.sc_code == sc_code).first()
    # if find in the unpay table, than update the unpay table
    if result:
        result.handled = handle_score
        result.remark = result.remark + remark
        result.last_modified_date = now
        _db.session.commit()
    else:
        uppay_obj = unpay_sale_status(handled = handle_score, sc_code = sc_code, remark = remark, last_modified_date = now)
        _db.session.add(uppay_obj)
        _db.session.commit()


    return make_response(jsonify(result= "add success"))