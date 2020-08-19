from django.shortcuts import render,redirect,get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import  ListView , DetailView , View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from .models import *
from .forms import *
import random
import string



#####################################  start work #######################################

class HomeListView(ListView):
    model = Product
    template_name = 'shops/home.html'


class ProductDetail(DetailView):
    model = Product
    template_name = 'shops/pro_detail.html'


class AddToCart(LoginRequiredMixin,View):
    def get(self,request,pk,*args,**kwargs):

        product = get_object_or_404(Product,product_id = pk )

        get_product , create = CardItem.objects.get_or_create(user_id=self.request.user, item = product , orders= False)

        order_query = Order.objects.filter(user_id = request.user , ordered= False)

        if order_query.exists():
            order = order_query[0]

            if order.items.filter(item__product_id = pk).exists():
                get_product.qty += 1
                get_product.save()
                #todo: msg product add successfully
            else:
                order.items.add(get_product)
                #todo: msg product add successfully
            return redirect('shop:order_summary')

        else:
            order = Order.objects.create(
                user_id= request.user,
                ordered=False,
                add_date= timezone.now(),
            )
            order.items.add(get_product)
            #todo: msg new product added successfulluy
            return redirect('shop:order_summary')



class OrderSummary(LoginRequiredMixin,View):
    def get(self,request,*args,**kwargs):

        try:
            order = Order.objects.get(user_id= self.request.user,ordered=False)
            context = {"order":order}
            return render(self.request,'shops/ordery_summary.html',context)
        except ObjectDoesNotExist:
            #todo: msg you have not active order
            return redirect('shop:home')


class Checkout(LoginRequiredMixin,View):
    def get(self,request,*args,**kwargs):
       try:
           order = Order.objects.get(user_id = self.request.user,ordered=False)
           form = AddressForm()
           context = {"form":form}
           return render(self.request,'shops/checkout.html',context)

       except ObjectDoesNotExist:
           #todo: msg you have not any actiove order
           return redirect('shop:home')

    def post(self,request,*args,**kwargs):
        form = AddressForm(self.request.POST or None)
        order = Order.objects.get(user_id = self.request.user,ordered=False)
        if form.is_valid():
            a = form.save(commit=False)
            a.user = self.request.user
            a.save()

            order.address = a
            order.save()
            return redirect('shop:payment')
        else:
            return redirect('shop:checkout')


class PaymentView(LoginRequiredMixin,View):
    def get(self,request,*args,**kwargs):
        order = Order.objects.get(user_id = self.request.user,ordered=False)
        if not order.address:
            return redirect("shop:checkout")
        return render(self.request,'shops/payment.html')

    def post(self,*args,**kwargs):
        order = Order.objects.get(user_id=self.request.user,ordered=False)


        if self.request.POST.get("payment") == "cod":
            p = Payment()
            p.user = self.request.user
            p.amount = order.get_total()
            p.order_id = order
            p.save()

            order_item = order.items.all()
            order_item.update( orders = True)
            for i in order_item:
                i.save()
            order.ordered = True
            order.save()
            return redirect('shop:my_order')
        else:
            return redirect('shop:home')



class MyOrder(View):
    def get(self,request,*args,**kwargs):

        context ={
            "order":Order.objects.filter(user_id = self.request.user,ordered=True)
        }

        return render(self.request,'shops/my_order.html',context)


class RemoveFormCart(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        item = get_object_or_404(Product,product_id = pk)

        order = Order.objects.filter(user_id=self.request.user, ordered=False)

        if order.exists():
            order_as = order[0]
            if order_as.items.filter(item__product_id = pk).exists():

                order_item = CardItem.objects.filter(item=item, user_id=self.request.user, orders=False)[0]
                if order_item.qty > 1:
                    order_item.qty -= 1
                    order_item.save()
                else:
                    order_as.items.remove(order_item)
                    return redirect("shop:home")
            else:
                return redirect("shop:order_summary")

        else:
            return redirect("shop:order_summary")
        return redirect('shop:order_summary')


class RemoveCart(LoginRequiredMixin,View):
    def get(self,request,pk,*args,**kwargs):
        item = get_object_or_404(Product,product_id = pk)

        order = Order.objects.filter(user_id= self.request.user,ordered=False)

        if order.exists():
            order_as = order[0]
            if order_as.items.filter(item__product_id = pk ).exists():
                order_item = CardItem.objects.filter(item = item ,user_id=self.request.user,orders=False)[0]
                order_as.items.remove(order_item)
                order_item.delete()
            return redirect('shop:home')
        return redirect('shop:order_summary')



################################ try for search #########################

# class SearchProduct(View):
#     def get(self,request, *args, **kwargs):
#         search = request.GET.get("search")
#
#         context = {"product":Product.objects.filter(product_name__icontains=search)}
#
#         return render(request,'shops/home.html',context)


def search(r):
    if r.method == "GET":
        search = r.GET.get("search")

        data = {"product": Product.objects.filter(product_name__icontains=search)| Product.objects.filter(brand__brand_name__icontains=search)}

        return render(r, 'shops/search_procuct.html', data)





