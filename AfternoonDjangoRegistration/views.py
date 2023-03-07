from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserRegistrationForm
from django.contrib.auth.decorators import login_required
from .models import Product, Supplier



def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            form.save()
            messages.success(request, f'Account created for {username}')
            return redirect('user-registration')
    else:
        form = UserRegistrationForm()

    return render(request, 'register.html', {'form': form})


@login_required()
def home(request):
    return render(request, 'home.html')

@login_required()
def add_product(request):
    if request.method == "POST":
        product_name = request.POST.get('p_name')
        product_price = request.POST.get('p_price')
        product_quantity = request.POST.get('p_quantity')
        # save data into the database
        product = Product(prod_name=product_name,
                          prod_price=product_price,
                          prod_quantity=product_quantity)
        product.save()
        messages.success(request, "Data saved successfully")
        return redirect("add-product")

    return render(request, 'add-products.html')

@login_required
def view_products(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'products.html', context)

@login_required
def delete_product(request, id):
    product = Product.objects.get(id=id)
    product.delete()
    messages.success(request, 'Product deleted successfully')
    return redirect("products")

@login_required
def update_product(request, id):
    if request.method == "POST":
        # receive updated data from the form
        product_name = request.POST.get("p_name")
        product_price = request.POST.get("p_price")
        product_quantity = request.POST.get("p_quantity")

        # select the product you want to update
        product = Product.objects.get(id=id)

        # update the product
        product.prod_name = product_name
        product.prod_quantity = product_quantity
        product.prod_price = product_price

        # return the updated values back to the database
        product.save()
        messages.success(request, 'Product updated successfully')
        return redirect('products')

    product = Product.objects.get(id=id)
    return render(request, 'update.html', {'product': product})

@login_required
def add_supplier(request):
    # check if the form submitted has a method post
    if request.method == "POST":
        # receive data from the form
        name = request.POST.get('s_name')
        email = request.POST.get('s_email')
        phone = request.POST.get('s_phone')
        product = request.POST.get('s_product')

        # save the data into the suppliers' table
        supplier = Supplier(sup_name=name, sup_email=email,
                            sup_phone=phone, sup_product=product)
        supplier.save()
        # redirect back to supplier page with a success message
        messages.success(request, 'Supplier added successfully')
    return render(request, 'add-supplier.html')

@login_required
def view_supplier(request):
    suppliers = Supplier.objects.all()
    context = {'suppliers': suppliers}
    return render(request, 'suppliers.html', context)

@login_required
def delete_supplier(request, id):
    supplier = Supplier.objects.get(id=id)
    supplier.delete()
    messages.success(request, 'Supplier deleted successfully')
    return redirect("suppliers")

@login_required
def pay(request, id):
    # select the product being paid for
    product = Product.objects.get(id=id)
    return render(request, 'payment.html', {'product': product})
