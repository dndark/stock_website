from app import app, db
from .models import Item, ItemOut, PendingDetail, PendingLocation
from datetime import datetime
import random
from flask import jsonify, request, abort, make_response
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import or_

# item is NEW DATABASE
# itemOut is the OLD DATABASE

@app.route('/item/<key>/<value>', methods=['GET'])
def item(key,value):
    value = str(value)
    if key.lower() == "id":
        item = Item.query.filter_by(id=value).first_or_404()
    try:
        item = item.as_dict()
    except Exception as e:
        abort(404)

    return  jsonify(item)

@app.route('/out_item/<key>/<value>', methods=['GET'])
def getItemOut(key,value):
    '''
    getItemOut is the API use for getting a list of out storage data from the `item_out` table
    '''

    result = []
    items = []
    value = str(value)

    if key.lower() == "id":
        items = ItemOut.query.filter_by(out_id=value).all()
    # out storage number
    elif key.lower() == "out_code":
        items = ItemOut.query.filter_by(out_code=value).all()
    elif key.lower() == "brand":
        items = ItemOut.query.filter(or_(ItemOut.out_item_brand1==value, ItemOut.out_item_brand2==value, 
                                    ItemOut.out_item_brand3==value, ItemOut.out_item_brand4==value, 
                                    ItemOut.out_item_brand5==value)).all()
    # contract number
    elif key.lower() == "contract":
        items = ItemOut.query.filter_by(sc_code=value).all()
    try:
        if len(items) == 0:
            raise Exception
        for item in items:
            result.append(item.as_dict())
    except Exception as e:
        print(e)
        abort(404)
    return jsonify(result)


    
@app.route('/stocks/type/<t>/<value>', methods=['GET'])
def stockFilter(t, value):
    if (t == "id"):
        obj = Item.id
    elif (t == "productType"):
        obj = Item.productType
    elif (t == "company"):
        obj = Item.company
    elif (t == "modelNumber"):
        obj = Item.modelNumber
    elif (t == "stockNumber"):
        obj = Item.stockNumber
    elif (t == "location"):
        obj = Item.location

    result = Item.query.filter(obj.like('%{}%'.format(value))).all()
    
    for i in range(len(result)):
        result[i] = result[i].as_dict()
    return jsonify(items = result)

@app.route('/stocks/', methods=['GET','PUT', 'POST'])
def stocks():
    if request.method == 'POST':
        post_data = request.get_json()
        # db.session.rollback()
        for x in post_data:
            # don't set the stockNumber when user first input it 
            if x.get("stockNumber"):
                stockNumber = x["stockNumber"]
            else:
                stockNumber = 0

            ts = datetime.fromtimestamp(x["lastModifiedDate"]/1000)
            newobj = Item(id=str(x["id"]), company=x["company"], modelNumber=x["modelNumber"],
                        lastModifiedDate=ts, info=x["info"], 
                        stockNumber = stockNumber, productType = x["productType"],
                        location = x["location"])
            db.session.add(newobj)

        try:
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            error = str(e.__dict__['orig'])
            return make_response(jsonify(error), 400)
        items = Item.query.all()
        return jsonify(result= "add success")
    elif request.method == 'PUT':
        post_data = request.get_json()
        for x in post_data:
            # only modified the stockNumber and the lastModifiedData
            ts = datetime.fromtimestamp(x["lastModifiedDate"]/1000)
            newobj = Item.query.filter_by(id=str(x["id"])).first()
            newobj.stockNumber = x["stockNumber"]
            # newobj.company = x["company"]
            # newobj.info = x["info"]
            # newobj.location = x["location"]
            # newobj.modelNumber = x["modelNumber"]
            # newobj.productType = x["productType"]
            newobj.lastModifiedDate = ts
        db.session.commit()
        return jsonify(result= "update success")
    elif request.method == 'GET':
        items = []
        for x in Item.query.all():
            items.append(x.as_dict())
    return jsonify(items = items)

@app.route('/pendingLocations', methods=['GET'])
def pengdingLocations():
    isExpire = request.args.get('isExpire')
    isAll = request.args.get('isAll')
    now = datetime.now()

    result = []

    if isAll:
        result = PendingLocation.query.all()
    elif isExpire and isExpire.lower() == 'true':
        result = PendingLocation.query.filter(PendingLocation.pickupTime <= now).all()
    elif isExpire  and isExpire.lower() == 'false':
        result = PendingLocation.query.filter(or_(PendingLocation.pickupTime > now, 
                                            PendingLocation.pickupTime == None)).all()

    for i in range(len(result)):
        result[i] = result[i].as_dict()
    return make_response(jsonify(result))

    
@app.route('/pendingLocation/<id>', methods=['GET'])
def pengdingLocation(id):
    result = PendingLocation.query.filter_by(id=str(id)).first()
    return make_response(jsonify(result.as_dict()))


@app.route('/pendingDetail/<pendingID>', methods=['GET'])
def getPendingDetail(pendingID):
    result = PendingDetail.query.filter_by(pending_id=str(pendingID)).all()
    for i in range(len(result)):
        result[i] = result[i].as_dict()
    return make_response(jsonify(result))



@app.route('/pendingDetail/', methods=['PUT', 'POST'])
def pending():
    if request.method == 'POST':
        post_data = request.get_json()
        # db.session.rollback()
        pt = datetime.fromtimestamp(post_data["pickupTime"]/1000)
        pl = PendingLocation(id=post_data["id"], location=post_data["location"], pickupTime=pt)
        
        db.session.add(pl)
        for x in post_data["scanItems"]:
            ts = datetime.fromtimestamp(x["lastModifiedDate"]/1000)
            newobj = PendingDetail(itemID=x["id"], company=x["company"], modelNumber=x["modelNumber"],
                                    lastModifiedDate=ts, info=x["info"],
                                    amount=x["amount"], productType=x["productType"],
                                    pendingLocation=pl)
            db.session.add(newobj)
        try:
            result = db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            error = str(e.__dict__['orig'])
            return make_response(jsonify(error), 400)
        return make_response(jsonify(result))
    elif request.method == 'PUT':
        post_data = request.get_json()
        for x in post_data:
            # only modified the stockNumber and the lastModifiedData
            ts = datetime.fromtimestamp(x["lastModifiedDate"]/1000)
            newobj = Item.query.filter_by(id=str(x["id"])).first()
            newobj.stockNumber = x["stockNumber"]
            newobj.lastModifiedDate = ts
        db.session.commit()
        return jsonify(result= "update success")
    # elif request.method == 'GET':
    #     items = []
    #     for pd in PendingDetail.query.all():
    #         item = pd.as_dict()
    #         # item["pendingID"] = pd.pendingLocation.id
    #         item["location"] = pd.pendingLocation.location
    #         items.append(item)
    return jsonify(items = items)
