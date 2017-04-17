from behave import *
import json
import shopcart as server

# Status Codes
HTTP_200_OK = 200
HTTP_201_CREATED = 201
HTTP_204_NO_CONTENT = 204
HTTP_400_BAD_REQUEST = 400
HTTP_404_NOT_FOUND = 404
HTTP_409_CONFLICT = 409

@when(u'I visit the "home page"')
def step_impl(context):
    context.resp = context.app.get('/')

@then(u'I should see "{message}"')
def step_impl(context, message):
	assert message in context.resp.data

@then(u'I should not see "{message}"')
def step_impl(context, message):
    assert message not in context.resp.data

@when(u'I create a new shopcart for uid "{uid}"')
def step_impl(context,uid):
	new_shopcart = { "uid": int(uid)}
	data = json.dumps(new_shopcart)
	context.resp = context.app.post('/shopcarts', data=data, content_type='application/json')

@when(u'I create a new shopcart without a uid')
def step_impl(context):
	new_shopcart = {}
	data = json.dumps(new_shopcart)
	context.resp = context.app.post('/shopcarts', data=data, content_type='application/json')

@when(u'I create a new shopcart with uid "{id}" having a product with sku "{sku}", quantity "{quantity}", name "{name}" and unitprice "{unitprice}"')
def step_impl(context,id,sku,quantity,name,unitprice):
	new_shopcart = { "uid": int(id), "products": [{"sku" : int(sku), "quantity" : int(quantity), "name" : name , "unitprice" : float(unitprice)}] }
	data = json.dumps(new_shopcart)
	context.resp = context.app.post('/shopcarts', data=data, content_type='application/json')

@then(u'I should see a new shopcart with uid "{id}"')
def step_impl(context,id):
	new_json = json.loads(context.resp.data)
	assert context.resp.status_code == HTTP_201_CREATED
	assert int(new_json['uid']) == int(id)

@then(u'I should see a product having sku "{sku}", quantity "{quantity}", name "{name}" and unitprice "{unitprice}"')
def step_impl(context,sku,quantity,name,unitprice):
	new_json = json.loads(context.resp.data)
	for i in range(0,len(new_json['products'])):
		if new_json['products'][0]['sku'] == int(sku):
			assert new_json['products'][0]['quantity'] == int(quantity)
			assert new_json['products'][0]['name'] == name
			assert new_json['products'][0]['unitprice'] == int(unitprice)

@then(u'I should see shopcart with id "{id}"')
def step_impl(context, id):
    data = json.loads(context.resp.data)
    found_id = False
    for cart in data:
        if cart["sid"] == int(id):
            found_id = True
    assert found_id

@when(u'I visit "{url}"')
def step_impl(context, url):
    context.resp = context.app.get(url)
    assert context.resp.status_code == 200
