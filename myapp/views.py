from django.shortcuts import render, redirect
from .models import *
from datetime import date,datetime
import json
from django.http import JsonResponse
from django. contrib import messages
from django.db.models import Q
from .utils import cookieCart, cartData, guestOrder
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# Create your views here.

def admin_login(request):
    if request.method == 'POST':
        username  = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username,password=password)
        if user is not None:
            request.session['SAdm_id'] = user.id
            return redirect('userhome')
        elif Admin_register.objects.filter(username=request.POST['username'], password=request.POST['password'], designation="admin").exists():
            member = Admin_register.objects.get(
                username=request.POST['username'], password=request.POST['password'])
            request.session['admid'] = member.reg_id
            return redirect('admin_dashboard')

        # elif Admin_register.objects.filter(username=request.POST['username'], password=request.POST['password'], designation="user").exists():
        #     member = Admin_register.objects.get(
        #         username=request.POST['username'], password=request.POST['password'])
        #     request.session['userid'] = member.reg_id
        #     return redirect('userhome')

        else:
            return redirect('admin_log')
    else:
        return redirect('admin_log')
def home(request):
    it = categories.objects.all()
    return render(request, 'home.html',{'it': it})

def search(request):
    if request.method == 'POST':
        usr = request.POST['search']
        pro = Q(category_name__icontains=usr)
        dsa = categories.objects.filter(pro).distinct()
        context = {'category': dsa}
        return render(request, 'search.html', context)

def userhome(request):
    if 'SAdm_id' in request.session:
        if request.session.has_key('SAdm_id'):
            SAdm_id = request.session['SAdm_id']
        else:
            return redirect('/')
        
        member = User.objects.get(id=SAdm_id)
        it = categories.objects.all()
        return render(request, 'loginhome.html',{'it': it, 'member': member})
    # else:
    #         return redirect('/')

def test_page(request):
    it = categories.objects.all()
    its = Product.objects.all()
    return render(request, 'test_page.html',{'it': it, 'its': its})


def modelshow(request, id):
    model = Product.objects.get(id=id)
    return render(request, 'modelshow.html', {'model': model})


def new_page(request, id):
    
        if request.session.has_key('SAdm_id'):
            SAdm_id = request.session['SAdm_id']
        else:
            return redirect('/')
        member = User.objects.get(id=SAdm_id)
        products = Product.objects.all()
        it = categories.objects.all()
        data = cartData(request)
        cartItems = data['cartItems']
        man1 = Product.objects.filter(category_id=id)
        man = categories.objects.filter(cat_id=id)
        sub = SubCategory.objects.all()
        # return render(request, 'new_page.html', {'it':it,'products':products,'cartItems':cartItems,'man': man, 'man1': man1})
        return render(request, 'new_page.html', {'sub':sub,'it':it,'products':products,'cartItems':cartItems,'man': man, 'man1': man1,'member':member})
    # else:
    #         return redirect('/')


def sub(request, id):
    if request.session.has_key('SAdm_id'):
        SAdm_id = request.session['SAdm_id']
    else:
        return redirect('/')
    member = User.objects.get(id=SAdm_id)
    products = Product.objects.all()
    it = categories.objects.all()
    data = cartData(request)
    cartItems = data['cartItems']
    man1 = Product.objects.filter(subcategory_id=id)
    man = categories.objects.filter(cat_id=id)
    subcate = SubCategory.objects.filter(id=id)
    sub1 = SubCategory.objects.all()
    return render(request, 'sub.html', {'subcate':subcate,'it':it,'data':data,'cartItems':cartItems,'member':member,'products':products,'sub':sub1,'man': man, 'man1': man1})


def admin_log(request):
    return render(request, 'admin_log.html')

def Signup_emailval(request):
    email = request.GET.get('email', None)
 
    data = {
        'is_taken': Admin_register.objects.filter(email=email).exists()
    }
    if data['is_taken']:
        data['error_message'] = 'Email already exists.'
    return JsonResponse(data)

def registration(request):
    if request.method == 'POST':
        firstname = request.POST['first_name']
        lastname = request.POST['last_name']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        confirmpassword = request.POST['cpassword']
        
        if password == confirmpassword:
            if User.objects.filter(username=username).exists():
                return redirect('admin_log')
            else:
                user = User.objects.create_user(first_name=firstname,last_name=lastname,email=email,username=username,password=password)
                user.save()
                msg_success = "Registration Successfull"
                messages.info(request, 'Registration successfully completed')
                return render(request,'registration.html',{'msg_success':msg_success})
        else:
            messages.info(request, 'password not matching')
            return redirect('registration')
   
    return render(request, 'registration.html')




def user_logout(request):
    if 'SAdm_id' in request.session:
        request.session.flush()
        it = categories.objects.all()
        return render(request, 'home.html',{'it': it})
    else:
        it = categories.objects.all()
        return render(request, 'home.html',{'it': it})

def admin_logout(request):
    if 'admid' in request.session:
        request.session.flush()
        return redirect('/')
    else:
        return redirect('/')

def admin_settings(request):
    if 'admid' in request.session:
        if request.session.has_key('admid'):
            admid = request.session['admid']
        else:
            return redirect('/')
        adm = Admin_register.objects.filter(reg_id=admid)
        return render(request, 'admin_settings.html', {'adm': adm})
    else:
        return redirect('/')

def admin_edit_profile(request):
    if 'admid' in request.session:
        if request.session.has_key('admid'):
            admid = request.session['admid']
        else:
            return redirect('/')
        adm = Admin_register.objects.filter(reg_id=admid)
        if request.method == 'POST':
            abb = Admin_register.objects.get(reg_id=admid)
            abb.fullname = request.POST['fullname']
            abb.email = request.POST['email']
            abb.username = request.POST['username']
            abb.save()
            return redirect("admin_settings")
        return render(request, 'admin_edit_profile.html', {'adm': adm})
    else:
        return redirect('/')

def admin_edit_picture(request):
    if 'admid' in request.session:
        if request.session.has_key('admid'):
            admid = request.session['admid']
        else:
            return redirect('/')
        adm = Admin_register.objects.filter(reg_id=admid)
        if request.method == 'POST':
            abb = Admin_register.objects.get(reg_id=admid)
            abb.photo = request.FILES['img']
            abb.save()
            return redirect("admin_settings")
        return render(request, 'admin_edit_picture.html', {'adm': adm})
    else:
        return redirect('/')

def admin_edit_password(request):
    if 'admid' in request.session:
        if request.session.has_key('admid'):
            admid = request.session['admid']
        else:
            return redirect('/')
        adm = Admin_register.objects.filter(reg_id=admid)
        if request.method == 'POST':
            ac = Admin_register.objects.get(reg_id=admid)
            oldps = request.POST['currentPassword']
            newps = request.POST['newPassword']
            cmps = request.POST.get('confirmPassword')
            if oldps != newps:
                if newps == cmps:
                    ac.password = request.POST.get('confirmPassword')
                    ac.save()
                    msg_success = "Password changed successfully"
                    return render(request, 'admin_settings.html', {'msg_success': msg_success})
            elif oldps == newps:
                messages.add_message(request, messages.INFO, 'Current and New password same')
            else:
                messages.info(request, 'Incorrect password same')
        return render(request, 'admin_edit_password.html', {'adm': adm})
    else:
        return redirect('/')

def admin_dashboard(request):
    if 'admid' in request.session:
        if request.session.has_key('admid'):
            admid = request.session['admid']
        else:
            return redirect('/')
        adm = Admin_register.objects.filter(reg_id=admid)
        users = Admin_register.objects.all().count()
        models = Product.objects.all().count()
        return render(request, 'admin_dashboard.html', {'adm': adm, 'users': users, 'models': models})
    else:
        return redirect('/')


def show_category(request):
    if 'admid' in request.session:
        if request.session.has_key('admid'):
            admid = request.session['admid']
        else:
            return redirect('/')
        adm = Admin_register.objects.filter(reg_id=admid)
        caty = categories.objects.all()
        return render(request, 'categories.html', {'caty': caty,'adm':adm})
    else:
        return redirect('/')

def Sub_categories(request):
    if 'admid' in request.session:
        if request.session.has_key('admid'):
            admid = request.session['admid']
        else:
            return redirect('/')
        adm = Admin_register.objects.filter(reg_id=admid)
        cate = categories.objects.all()
        subcate = SubCategory.objects.all()
        return render(request, 'Sub_categories.html', {'subcate':subcate,'caty': cate,'adm':adm})
    else:
        return redirect('/')

def add_category(request):
    try:

        if request.method == 'POST':
            category_name = request.POST['category_name']
            category_logo = request.FILES['category_logo']
            # sub_category1 = request.POST['sub_category1']
            # strippeddata1 = sub_category1.replace(" ", "")
            # sub_category2 = request.POST['sub_category2']
            # strippeddata2 = sub_category2.replace(" ", "")
            # sub_category3 = request.POST['sub_category3']
            # strippeddata3 = sub_category3.replace(" ", "")
            # sub_category4 = request.POST['sub_category4']
            # strippeddata4 = sub_category4.replace(" ", "")
            # sub_category5 = request.POST['sub_category5']
            # strippeddata5 = sub_category5.replace(" ", "")
            cat = categories(category_name=category_name, category_logo=category_logo)
            # cat = categories(category_name=category_name, category_logo=category_logo, sub_category1=strippeddata1,
            #                  sub_category2=strippeddata2, sub_category3=strippeddata3, sub_category4=strippeddata4, sub_category5=strippeddata5)
            cat.save()

            return redirect('category')
        else:
            return redirect('categories')
    except:
        return redirect('categories')

def add_subcategory(request):
        if request.method == 'POST':
            abc = SubCategory()
            abc.category_id  = request.POST['category']
            abc.subcategory = request.POST['subcategory']
            abc.save()
            msg_success = "Added successfull"
            return render(request, 'Sub_categories.html', {'msg_success': msg_success})
        return render(request, 'Sub_categories.html',) 
            

def cat_delete(request, cat_id):

    emp = categories.objects.get(cat_id=cat_id)
    emp.delete()
    return redirect('category')

def subcat_delete(request, id):
    
    emp = SubCategory.objects.get(id=id)
    emp.delete()
    return redirect('Sub_categories')


def admin_models(request):
    if 'admid' in request.session:
        if request.session.has_key('admid'):
            admid = request.session['admid']
        else:
            return redirect('/')
        adm = Admin_register.objects.filter(reg_id=admid)
        return render(request, 'admin_models.html',{'adm':adm})
    else:
        return redirect('/')


def addmodel(request):
    if 'admid' in request.session:
        if request.session.has_key('admid'):
            admid = request.session['admid']
        else:
            return redirect('/')
        adm = Admin_register.objects.filter(reg_id=admid)
        var = categories.objects.all()
        sub = SubCategory.objects.all()
        return render(request, "addmodel.html", {'sub':sub,'var': var,'adm':adm})
    else:
        return redirect('/')


def createmodel(request):
    if request.method == 'POST':

        modelname = request.POST['modelname']
        description = request.POST['description']
        gib = request.FILES['gib']
        price = request.POST['price']
        types = request.POST['types']
        format = request.POST['format']
        modeltype = request.POST['modeltype']
        category = request.POST['category']
        subcategory = request.POST['subcategory']
        fbx = request.FILES['fbx']

        item = Product(modelname=modelname, description=description, gib=gib, price=price, types=types, format=format, modeltype=modeltype, category_id=category,
                     subcategory_id=subcategory,fbx=fbx)
        item.save()
        return redirect('addmodel')
    else:
        return redirect('createmodel')


def admin_payment_history(request):
    if 'admid' in request.session:
        if request.session.has_key('admid'):
            admid = request.session['admid']
        else:
            return redirect('/')
        adm = Admin_register.objects.filter(reg_id=admid)
        return render(request, 'admin_payment_history.html',{'adm':adm})
    else:
        return redirect('/')


def payment_table(request):
    if 'admid' in request.session:
        if request.session.has_key('admid'):
            admid = request.session['admid']
        else:
            return redirect('/')
        adm = Admin_register.objects.filter(reg_id=admid)
        var = payment.objects.all()
        if request.method == "POST":
            fromdate = request.POST.get('fromdate')
            todate = request.POST.get('todate')
            var = payment.objects.filter(date__range=[fromdate, todate])
        return render(request, 'payment_table.html', {'var': var,'adm':adm})
    else:
        return redirect('/')


def registeredusers(request):
    if 'admid' in request.session:
        if request.session.has_key('admid'):
            admid = request.session['admid']
        else:
            return redirect('/')
        adm = Admin_register.objects.filter(reg_id=admid)
        use = Admin_register.objects.all()
        return render(request, 'registeredusers.html', {'use': use,'adm':adm})
    else:
        return redirect('/')


def delete(request, reg_id):
    admid = request.session['admid']
    use = Admin_register.objects.get(reg_id=reg_id)
    use.delete()
    return redirect('registeredusers')


def adminedit(request, id):
    if 'admid' in request.session:
        if request.session.has_key('admid'):
            admid = request.session['admid']
        else:
            return redirect('/')
        adm = Admin_register.objects.filter(reg_id=admid)
        item = Product.objects.filter(id=id)
        viva = categories.objects.all()
        return render(request, "adminedit.html", {'item': item, 'viva': viva})
    else:
        return redirect('/')

def admin_editmodel(request, id):
    if 'admid' in request.session:
        if request.session.has_key('admid'):
            admid = request.session['admid']
        else:
            return redirect('/')
        adm = Admin_register.objects.filter(reg_id=admid)
        item = Product.objects.filter(id=id)
        viva = categories.objects.all()
        return render(request, "admin_editmodel.html", {'item': item, 'viva': viva})
    else:
        return redirect('/')


def admin_current_models(request):
    if 'admid' in request.session:
        if request.session.has_key('admid'):
            admid = request.session['admid']
        else:
            return redirect('/')
        adm = Admin_register.objects.filter(reg_id=admid)
        category = categories.objects.all()
        item = Product.objects.all()
        return render(request, 'admin_current_models.html', {'category': category, 'item': item,'adm':adm})
    else:
        return redirect('/')


def model_delete(request, id):
    abc = Product.objects.get(id=id)
    abc.delete()
    return redirect('admin_current_models')


def modeledit(request, id):
    if request.session['admid'] == "":
        return redirect('logout')
    else:
        if request.method == "POST":
            item = Product.objects.get(id=id)
            item.modelname = request.POST.get('modelname', item.modelname)
            item.description = request.POST.get('description', item.description)
            item.gib = request.FILES.get('gib', item.gib)
            item.price = request.POST.get('price', item.price)
            item.types = request.POST.get('types', item.types)
            item.format = request.POST.get('format', item.format)
            item.modeltype = request.POST.get('modeltype', item.modeltype)
            item.category_id = request.POST.get('category_name', item.category_id)
            item.fbx = request.FILES.get('fbx', item.fbx)

            item.save()
            return redirect('admin_current_models')






# def login(request):
#     if request.method == 'POST':
#         username  = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(username=username,password=password)
#         if user is not None:
#             request.session['SAdm_id'] = user.id
#             return redirect('store')
        

        # elif Admin_register.objects.filter(username=request.POST['username'], password=request.POST['password'], designation="user").exists():
        #     member = Admin_register.objects.get(
        #         username=request.POST['username'], password=request.POST['password'])
        #     request.session['userid'] = member.reg_id
        #     return redirect('userhome')

#         else:
#             return redirect('login')
#     else:
#          return render(request,'login.html')

# def logout(request):
#     if 'user' in request.session:
#         request.session.flush()
#         return redirect('/')
#     else:
#         return redirect('/')

def store(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	products = Product.objects.all()
	context = {'products':products, 'cartItems':cartItems}
	return render(request, 'store/store.html', context)


def cart(request):
    if 'SAdm_id' in request.session:
        if request.session.has_key('SAdm_id'):
            SAdm_id = request.session['SAdm_id']
        else:
            return redirect('/')
        
        member = User.objects.get(id=SAdm_id)
        data = cartData(request)
        print(data['cartItems'])
        cartItems = data['cartItems']
        order = data['order']
        items = data['items']

        context = {'items':items, 'order':order, 'cartItems':cartItems,'member':member}
        return render(request, 'cart.html', context)

def checkout(request):
	if 'SAdm_id' in request.session:
		if request.session.has_key('SAdm_id'):
			SAdm_id = request.session['SAdm_id']
		else:
			return redirect('/')
		member = User.objects.get(id=SAdm_id)
		data = cartData(request)
		
		cartItems = data['cartItems']
		order = data['order']
		items = data['items']

		context = {'items':items, 'order':order, 'cartItems':cartItems,'member':member}
		return render(request, 'checkout.html', context)

def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	print('Action:', action)
	print('Product:', productId)

	customer = request.user.customer
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)

def processOrder(request):
    print("name")
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
    else:
        customer, order = guestOrder(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True
    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
        customer=customer,
        order=order,
        address=data['shipping']['address'],
        city=data['shipping']['city'],
        state=data['shipping']['state'],
        zipcode=data['shipping']['zipcode'],
        )

    return JsonResponse('Payment submitted..', safe=False)

def newcart(request):
    return render(request,'newcart.html')

def request(request):
    if 'SAdm_id' in request.session:
        if request.session.has_key('SAdm_id'):
            SAdm_id = request.session['SAdm_id']
        else:
            return redirect('/')
        
        member = User.objects.get(id=SAdm_id)
        it = categories.objects.all()
        return render(request, 'request.html',{'it': it, 'member': member})
    

def request_not_logedin(request):
    return render(request,'nologrequest.html')

def reqlist(request):
    re=Request.objects.all()
 
    return render(request,'requestli.html',{'re':re})


def savereq(request):
    if request.method=='POST':
        n=request.POST.get('name')
        nu=request.POST.get('number')
        em=request.POST.get('email')
        at=request.POST.get('about')
        images=request.FILES.get('image')
        req=Request(name=n, mobile=nu, email=em, about=at, image=images)
        req.save()
        return redirect('home')

def deletereq(request,id):
    re=Request.objects.get(id=id)
    re.delete()
    return redirect('reqlist')


