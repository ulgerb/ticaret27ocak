from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from django.db.models import Q


def basketCount(request):
    if request.user.is_authenticated:
        return Shopbasket.objects.filter(user=request.user)
    else:
        return None


def index(request):

    context = {
        "shopbasket": basketCount(request),
    }
    return render(request,'index.html',context)

def About(request):
    context = {
        "shopbasket": basketCount(request) ,
    }
    return render(request,'about.html',context)

def Contact(request):
    context = {
        "shopbasket": basketCount(request),
    }
    return render(request,'contact.html',context)

def Shop(request):
    products = ProductStok.objects.all()
    
    query = request.GET.get("query")
    if query:
        products = products.filter(
            Q(product__title__icontains = query) |
            Q(product__brand__icontains = query) |
            Q(product__text__icontains=query) |
            Q(product__slug__icontains=query)
        )
        
    print(request.GET)
    
    context = {
        "shopbasket": basketCount(request),
        "products":products,
    }
    return render(request,'shop.html',context)

def ShopDetail(request,slug):
    product = get_object_or_404(ProductStok, product__slug = slug)
    prdct = Product.objects.get(slug=slug)
    comments = Comment.objects.filter(product=prdct).order_by("-star")
    puan=0
    if request.method == "POST":
        submit = request.POST.get("submit")
        
        # SEPET SHOPBASKET =========
        if submit == "buy":
            color = request.POST.get("color")
            size = request.POST.get("size")
            try:
                count = int(request.POST.get("count"))
            except:
                return redirect('/ShopDetail/' + slug + '/')
            
            if count>0:
                prod = SizeLetter.objects.filter(product__slug=slug,color__styletitle=color, size__title=size)
                if prod.exists():
                    prod = prod.get()
                    price_all = prod.price * count
                    shopprod = Shopbasket.objects.filter(user=request.user,product_letter=prod)
                    if shopprod.exists(): # filterlanan ürün varsa true
                        shopprod = shopprod.get()
                        shopprod.count += count
                        shopprod.price_all += price_all
                        shopprod.save()
                    else:
                        shopb = Shopbasket(user = request.user, product_letter = prod,price_all=price_all, count=count )
                        shopb.save()     
            return redirect('/ShopDetail/'+ slug + '/')
        # SEPET SHOPBASKET =========
        elif submit == "comment":
            text = request.POST.get("text")
            try:
                star = int(request.POST.get("star"))
            except:
                return redirect('/ShopDetail/' + slug + '/')
            
            comment = Comment(text=text, star=star, user=request.user, product=prdct)
            comment.save()
            
            print("TOPLAM YORUM SAYISI",len(comments))
            for i in comments:
                puan += i.star
            print("TOTAL PUAN", puan)

            prdct.stars = round(puan/len(comments),1)
            prdct.save()
            
            # for i in :
            #     print(i) 
            
            # prdct.stars = 
            
            return redirect('/ShopDetail/' + slug + '/')
            
            
    # SCTIPT ==================
    listprice = []
    listcolor = []
    listsize = []
    sizeprice = product.sizeletter.all()
    for i in range(len(sizeprice)):
        listprice.append(sizeprice[i].price)
        listcolor.append(sizeprice[i].color.styletitle)
        listsize.append(sizeprice[i].size.slug)
    # SCTIPT ==================
    
    context = {
        "shopbasket": basketCount(request),
        "product":product,
        "listprice": listprice,
        "listcolor": listcolor,
        "listsize": listsize,
        "comments": comments,
    }
    return render(request,'shop-single.html',context)

# search , shopbasked fonksiyon, detay yorum 
def ShopBasket(request):
    
    shopbasket = Shopbasket.objects.filter(user=request.user)
    total = 0
    for i in shopbasket:
        total += i.price_all
        
    if request.method == "POST":
        for k, v in dict(request.POST).items():
            if k != "csrfmiddlewaretoken":
                try:
                    v[0] = int(v[0])
                except:
                    return redirect('ShopBasket')
                
                shopb = shopbasket.get(id=k[5:])
                if v[0] == "0":
                    shopb.delete()
                elif v[0] > 0:
                    shopb.count = v[0]
                    shopb.price_all = shopb.product_letter.price * int(v[0])
                    shopb.save() 
                else:
                    return redirect('ShopBasket')
                    
        return redirect('ShopBasket')
                

    context = {
        "shopbasket": shopbasket,
        "total": total,
    }
    return render(request, 'user/shop-basket.html', context)


def ShopBasketDelete(request, sid):
    
    shopbasket = Shopbasket.objects.get(id=sid)
    shopbasket.delete()
    return redirect('ShopBasket')