from django.urls import path, include
from .views import(
    CategoryCreateView,
    SubCategoryCreateView,
    ProductCreateView,
    ProductImageCreateView,
    CategoryUpdateDeleteView,
    SubCategoryUpdateDeleteView,
    PopularProductListView,
    ProductbyCategoryListView,
    ProductbySubCategoryListView,
    ProductbyArtistListView,
    ParticularProductView,
    ParticularProductModifyView,
    AllCategoriesView,
    AllSubCategoriesView
)

urlpatterns = [
    path('create/product/', ProductCreateView.as_view()),
    path('create/product/add_image/', ProductImageCreateView.as_view()),
    path('create/category/', CategoryCreateView.as_view()),
    path('create/subcategory/', SubCategoryCreateView.as_view()),
    path('modify/category/<category>/', CategoryUpdateDeleteView.as_view()),
    path('modify/subcategory/<subcategory>/', SubCategoryUpdateDeleteView.as_view()),
    path('view/allcategories/', AllCategoriesView.as_view()),
    path('view/allsubcategories/<category>/', AllSubCategoriesView.as_view()),
    path('view/product/category/<category>/', ProductbyCategoryListView.as_view()),
    path('view/product/subcategory/<subcategory>/', ProductbySubCategoryListView.as_view()),
    path('view/product/artist/<artist>/', ProductbyArtistListView.as_view()),
    path('view/popular_products/', PopularProductListView.as_view()),
    path('view/product/<pid>/', ParticularProductView.as_view()),
    path('modify/product/<pid>/', ParticularProductModifyView.as_view()),
]
