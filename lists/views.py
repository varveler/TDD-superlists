from django.shortcuts import redirect, render
from django.http import HttpResponse
from lists.models import Item

# Create your views here.
#
def home_page(request):

	# The problem with this solution is that creates a new Item
	# every time it loeads the home_page
	#item = Item()
	#item.text = request.POST.get('item_text', '')
	#item.save()

####################################################
	# The problem with this is that ugly new_item_text
	
	#if request.method == 'POST':
	#	new_item_text = request.POST['item_text']
	#	Item.objects.create(text=new_item_text)
	#else:
	#	new_item_text= ''


	
	#return render(request, 'home.html', {
	#	'new_item_text': request.POST.get('item_text', ''),

	#	})
####################################################3

	if request.method == 'POST':
		Item.objects.create(text=request.POST['item_text'])
		return redirect('/lists/the-only-list-in-the-world/')
	
	#items = Item.objects.all()
	#return render(request, 'home.html', {'items':items})
	return render(request, 'home.html')

def view_list(request):
	items = Item.objects.all()
	return render(request, 'list.html', {'items':items})