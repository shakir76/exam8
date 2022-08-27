from django.urls import path

from webapp.views import ListProduct, CreateProduct, ProductView, UpdateProduct, DeleteProduct, AddReview, UpdateReview, \
    DeleteReview

app_name = 'webapp'

urlpatterns = [
    path('', ListProduct.as_view(), name="index"),
    path('product/create/', CreateProduct.as_view(), name="create_product"),
    path('product/<int:pk>/', ProductView.as_view(), name="view_product"),
    path('product/<int:pk>/update', UpdateProduct.as_view(), name="update_product"),
    path('product/<int:pk>/delete', DeleteProduct.as_view(), name="delete_product"),
    path('product/<int:pk>/add/review', AddReview.as_view(), name="add_review"),
    path('product/<int:pk>/update/review', UpdateReview.as_view(), name="update_review"),
    path('product/<int:pk>/delete/review', DeleteReview.as_view(), name="delete_review")

]
