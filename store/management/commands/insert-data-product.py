import random

from django.core.management.base import BaseCommand
from django.db import transaction
from django.contrib.auth import get_user_model

from store.models import CategoryProduct, ProductComment, ProductProperties, ProductAnswerComment

from store.factories import (
    CategoryFactory, BaseProductFactory, BrandFactory, SubCategoryProductFactory, ProductFactory,
    SizeFactory, ColorFactory, ProductPropertiesFactory, ProductCommentFactory,
    ProductAnswerCommentFactory
)

# create your command here

list_of_models = [CategoryProduct, ProductProperties]

NUM_CATEGORIES = 100
NUM_BASE_PRODUCTS = 100
NUM_BRANDS = 100
NUM_SUB_CATEGORIES = 100
NUM_PRODUCTS = 100
NUM_SIZES = 100
NUM_COLORS = 100
NUM_PRODUCT_PROPERTIES = 100
NUM_COMMENT_OF_PRODUCTS = 100
NUM_ANSWER_COMMENT_OF_PRODUCT = 100


class Command(BaseCommand):

    # def add_arguments(self, parser) -> None:
    #     parser.add_argument('enter', nargs='+', type=int)

    @transaction.atomic()
    def handle(self, *args, **kwargs):
        self.stdout.write('deleting old data...')

        for m in list_of_models:
            m.objects.all().delete()

        self.stdout.write('creating new data \n')


        # product properties data
        print(f'adding {NUM_PRODUCT_PROPERTIES} product properties...')
        all_product_properties = [ProductPropertiesFactory() for _ in range(NUM_PRODUCT_PROPERTIES)]
        print('DONE')


        # size data
        print(f'adding {NUM_SIZES} sizes...')
        all_sizes = [SizeFactory() for _ in range(NUM_SIZES)]
        print('DONE')


        # color data
        print(f'adding {NUM_COLORS} colors...')
        all_colors = [ColorFactory() for _ in range(NUM_COLORS)]
        print('DONE')


        # brand data
        print(f'adding {NUM_BRANDS} brands...')
        all_brands = [BrandFactory() for _ in range(NUM_CATEGORIES)]
        print('Done')


        # categories data
        print(f'adding {NUM_CATEGORIES} categories ...')
        all_categories = [
            CategoryFactory() for _ in range(NUM_CATEGORIES)
        ]
        print('Done')


        # sub categories data
        print(f'adding {NUM_SUB_CATEGORIES} sub categories...')
        all_sub_categories = [
            SubCategoryProductFactory(category_id=random.choice(all_categories).id)
        ]
        print("DONE")


        # base products data
        print(f'adding {NUM_BASE_PRODUCTS} base products...')
        all_base_products = list()

        for _ in range(NUM_BASE_PRODUCTS):
            new_base_product = BaseProductFactory(
                category_id=random.choice(all_categories).id,
                sub_category_id=random.choice(all_sub_categories).id,
                brand_id=random.choice(all_brands).id,
            )
            new_base_product.save()
            all_base_products.append(new_base_product)
        print('DONE')


        # add products
        print(f'adding {NUM_PRODUCTS} products...')
        all_products = list()

        for _ in range(NUM_PRODUCTS):
            new_product = ProductFactory(
                base_product_id=random.choice(all_base_products).id,
                color_id=random.choice(all_colors).id,
                size_id=random.choice(all_sizes).id,
            )
            all_products.append(new_product)
        print('DONE...')


        # comments data
        print(f'adding {NUM_COMMENT_OF_PRODUCTS} comments for products...')
        for product in all_products:
            for _ in range(random.randint(1, 5)):
                comment = ProductCommentFactory(
                    product_id=product.id,
                    user_id=get_user_model().objects.all().first().id,
                )
                comment.save()
        print('DONE')


        # answer comment data
        print(f'adding {NUM_ANSWER_COMMENT_OF_PRODUCT} answer of comments...')
        for comment in ProductComment.objects.all():
            for _ in range(random.randint(1, 2)):
                answer = ProductAnswerCommentFactory(
                    comment_id=comment.id,
                    user_id=get_user_model().objects.all().first().id,
                )
                answer.save()
        print('DONE')
