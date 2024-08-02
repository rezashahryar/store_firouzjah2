import factory
import random

from faker import Faker
from factory.django import DjangoModelFactory
from django.utils.text import slugify

from . import models


faker = Faker()


class ProductAnswerCommentFactory(DjangoModelFactory):
    class Meta:
        model = models.ProductAnswerComment
    
    text = factory.Faker('text')


class ProductCommentFactory(DjangoModelFactory):
    class Meta:
        model = models.ProductComment

    text = factory.Faker('text')
    


class ColorFactory(DjangoModelFactory):
    class Meta:
        model = models.Color
    name = factory.Faker('word')
    code_of_color = factory.Faker('word')


class SizeFactory(DjangoModelFactory):
    class Meta:
        model = models.Size
    size = factory.Faker('word')


class SubCategoryProductFactory(DjangoModelFactory):
    class Meta:
        model = models.SubCategoryProduct
    name = factory.Faker(
        "sentence",
        nb_words=5,
        variable_nb_words=True
    )
    slug = slugify(name)


class BrandFactory(DjangoModelFactory):
    class Meta:
        model = models.Brand
    name = factory.Faker("name")


class ProductPropertiesFactory(DjangoModelFactory):
    class Meta:
        model = models.ProductProperties
    title = factory.Faker("name")

    @factory.post_generation
    def properties(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for tournament in extracted:
                self.tournaments.add(tournament)


class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = models.CategoryProduct

    name = factory.Faker(
        "sentence",
        nb_words=2,
        variable_nb_words=True
    )
    slug = slugify(name)
    # properties = factory.RelatedFactoryList(
    #     ProductPropertiesFactory,
    #     factory_related_name='categories',
    #     size=lambda: random.randint(1, 25)
    # )


class BaseProductFactory(DjangoModelFactory):
    class Meta:
        model = models.BaseProduct

    product_code = random.randint(10000, 99999)
    title_farsi = factory.Faker("name")
    title_english = factory.Faker("word")
    description = factory.Faker('paragraph', nb_sentences=5, variable_nb_sentences=True)
    product_authenticity = 'o'
    product_warranty = factory.LazyFunction(lambda: random.choice([0, 1]))

    sending_method = factory.LazyFunction(
        lambda: random.choice(
            [
                models.BaseProduct.SendingMethod.TIPAX,
                models.BaseProduct.SendingMethod.POST_PISHTAZ,
                models.BaseProduct.SendingMethod.BAARBARI,
                models.BaseProduct.SendingMethod.PEYK_MOTORI,
            ]
        )
    )


class ProductFactory(DjangoModelFactory):
    class Meta:
        model = models.Product

    inventory = factory.LazyFunction(lambda: random.randint(1, 1000))
    unit = factory.LazyFunction(
        lambda: random.choice(
            [
                models.Product.ProductUnit.PAIR,
                models.Product.ProductUnit.NUMBER,
            ]
        )
    )
    price = factory.LazyFunction(
        lambda: random.randint(1000, 10000000)
    )
    product_status = factory.LazyFunction(
        lambda: random.choice(
            [
                models.Product.ProductStatus.CONFIRM,
                models.Product.ProductStatus.WAITING,
                models.Product.ProductStatus.NOT_CONFIRMED,
            ]
        )
    )
