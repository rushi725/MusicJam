
"""
from django.shortcuts import render, get_object_or_404
from .models import Album, song

def index(request):
	all_albums = Album.objects.all()
	return render(request,'music/index.html',{'all_albums':all_albums,})
	

def detail(request,album_id):
	album = get_object_or_404(Album, pk=album_id)
	return render(request,'music/detail.html',{'album':album,})

def favorite(request, album_id):
	album = get_object_or_404(Album, pk=album_id)
	selected_song = album.song_set.get(pk=request.POST.get("song"))
	selected_song.is_favorite = True
	selected_song.save()
	return render(request,'music/detail.html',{'album':album,})
"""
# Generic Views

from django.views import generic
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login
from django.views.generic import View
from .forms import UserForm
from .models import Album

class IndexView(generic.ListView):
	template_name = 'music/index.html'
	context_object_name = 'all_albums'

	def get_queryset(self):
		return Album.objects.all()

class DetailView(generic.DetailView):
	model = Album
	template_name = 'music/detail.html'

class AlbumCreate(CreateView):
	model = Album
	fields = ['artist','album_title','genre','album_logo']

class AlbumUpdate(UpdateView):
	model = Album
	fields = ['artist','album_title','genre','album_logo']

class AlbumDelete(DeleteView):
	model = Album
	success_url = reverse_lazy('music:index')

class UserFormView(View):
	form_class = UserForm
	template_name = 'music/registration_form.html'	

	def get(self,request):
		form = self.form_class(None)
		return render(request,self.template_name,{'form':form})

	def post(self,request):
		form = self.form_class(request.POST)

		if form.is_valid():
			user = form.save(commit=False)

			#cleaned (normalized) data
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			user.set_password(password)
			user.save()

			#returns user objects if credential are correct
			user = authenticate(username=username,password=password)

			if user is not None:

				if user .is_active:
					login(request, user)
					return redirect('music:index')

		return render(request,self.template_name,{'form':form})

		
		






