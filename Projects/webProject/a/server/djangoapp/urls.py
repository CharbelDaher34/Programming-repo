from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'
urlpatterns = [
    # route is a string contains a URL pattern
    # view refers to the view function
    # name the URL
    path('', view=views.get_dealerships, name='index'),
    path('dealer/<int:dealer_id>/', views.get_dealership_id, name='get_dealer_by_id'),

    # path for about view
    path('about/', views.about, name='about_view'),
  
    # path for contact us view
    path('contact/', views.contact, name='contact_view'),

    # path for registration
    path("registration/", views.registration_request,name='registration_view'),
    # path for login
    path('login/',views.login_request, name='login_view'),
    # path for logout
    path('logout/',views.logout_request, name='logout_view'),


    # path for dealer reviews view
    path('dealer_reviews/<int:dealer_id>/',views.get_dealer_details,name='dealer_reviews_by_id'),

    # path for add a review view
    path('post_review/<int:dealer_id>',views.add_review,name='post_reviews_by_id'),
    path("post_review_view/<int:dealer_id>",views.post_review_view,name="post_review_view")

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)