from django.db import models
from django.contrib.auth.models import User, Group, Permission


class Client(models.Model):

    objects = models.Manager()

    ORG_TYPES = (
        (u'Государственная', (
                             (u'Силовики', u'Силовики'),
                             (u'Гос. компания', u'Гос. компания'),
                             (u'Гос. учреждение', u'Гос. учреждение'),
                              )),
        (u'Негосударственная', (
                              (u'Ген. подрядчик', u'Ген. подрядчик'),
                              (u'Частная компания', u'Частная компания'),
                              (u'SMB', u'SMB'),
                              )),
        )

    ORG_FORMS = (
        (u'ООО', u'ООО'),
        (u'ОАО', u'ОАО'),
        (u'ПАО', u'ПАО'),
        (u'ЗАО', u'ЗАО'),
        (u'АО', u'АО'),
    )
    
    DANET = (
        (u'Да', u'Да'),
        (u'Нет', u'Нет'),
    )

    form = models.CharField(verbose_name=u'Форма', max_length=16, choices=ORG_FORMS)  # !!! дополнить выпадающий список
    name = models.CharField(verbose_name=u'Название организации', max_length=128)
    inn = models.IntegerField(verbose_name=u'ИНН')  # посмотреть API налоговой для проверки фирмы

    basic_survey = models.BooleanField(verbose_name=u'Базовый опрос пройден', default=False)
    type = models.CharField(verbose_name=u'Тип организации', max_length=64, choices=ORG_TYPES, blank=True)
    sanctions = models.CharField(verbose_name=u'Санкции', max_length=6, blank=True, choices=DANET)
    crimea = models.CharField(verbose_name=u'Крым', max_length=6, blank=True, choices=DANET)
    imp = models.CharField(verbose_name=u'Импортозамещение', max_length=6, blank=True, choices=DANET)

    added_at = models.DateTimeField(auto_now_add=True)
    changed_at = models.DateTimeField(auto_now=True)
    manager = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True)

    class Meta:
        verbose_name = u'Клиент'
        verbose_name_plural = u'Клиенты'
        ordering = ['name']

    def get_field_names(self):
        fields = [f.name for f in self._meta.get_fields()]
        for i in ['id', 'form', 'name', 'inn', 'basic_survey', 'manager', 'changed_at', 'added_at']:
            fields.remove(i)
        return fields


class ClientChange(models.Model):

    objects = models.Manager()

    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    manager = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True)
    changed_at = models.DateTimeField(auto_now_add=True)
    change = models.TextField(blank=True)

    type = models.CharField(verbose_name=u'Тип организации(old)', max_length=64, blank=True)
    sanctions = models.CharField(verbose_name=u'Санкции(old)', max_length=6, blank=True)
    crimea = models.CharField(verbose_name=u'Крым(old)', max_length=6, blank=True)
    imp = models.CharField(verbose_name=u'Импортозамещение(old)', max_length=6, blank=True)

    class Meta:
        ordering = ['-id']


class Contact(models.Model):

    objects = models.Manager()

    first_name = models.CharField(verbose_name=u'Имя', max_length=64)
    father_name = models.CharField(verbose_name=u'Отчество', max_length=64)
    last_name = models.CharField(verbose_name=u'Фамилия', max_length=64)
    phone_number = models.CharField(verbose_name=u'Телефон', max_length=14, blank=True)
    phone_number2 = models.CharField(verbose_name=u'Доп. телефон', max_length=14, blank=True)
    email = models.EmailField(verbose_name=u'E-mail', blank=True)
    position = models.CharField(verbose_name=u'Должность', max_length=128)
    client_id = models.ForeignKey(Client, on_delete=models.CASCADE)

    class Meta:
        verbose_name = u'Контактное лицо'
        verbose_name_plural = u'Контактые лица'
        ordering = ['last_name']


class Item(models.Model):

    objects = models.Manager()

    KRITERII = (
        ('+','+'),
        ('-','-'),
        ('?','?'),
    )

    PRICE_CATEGORIES = (
        (u'(1)Premium', u'(1)Premium'),
        (u'(2)Средняя цен. кат.', u'(2)Средняя цен. кат.'),
        (u'(3)No name', u'(3)No name'),
    )

    PR_TYPES = (
        ('server', u'Сервера'),
        ('shd', u'СХД'),
    )

    CERTIFICATE = (
        ('none', u'нет'),
        ('torp', u'ТОРП'),
        ('st1', u'СТ1'),
        ('eac', u'EAC'),
    )

    product_type = models.CharField(verbose_name=u'Направление', max_length=64, choices=PR_TYPES)
    group = models.CharField(max_length=64)
    model_row = models.CharField(max_length=64)
    vendor1 = models.CharField(max_length=64)
    model = models.CharField(max_length=64)
    SKU = models.CharField(max_length=64)
    vendor2 = models.CharField(max_length=64)
    model2 = models.CharField(max_length=64)
    SKU2 = models.CharField(max_length=64)
    imp = models.CharField(verbose_name=u'Импортозамещение', max_length=8, choices=KRITERII)
    certificate = models.CharField(verbose_name=u'Сертификация', max_length=32, choices=CERTIFICATE)
    #ST1 = models.CharField(verbose_name=u'СТ1 ГОС образца', max_length=8, choices=KRITERII)
    #torp = models.CharField(verbose_name=u'Сертификат ТОРП', max_length=8, choices=KRITERII)
    #eac = models.CharField(verbose_name=u'EAC', max_length=8, choices=KRITERII)
    sanctions = models.CharField(verbose_name=u'Санкции', max_length=8, choices=KRITERII)
    crimea = models.CharField(verbose_name=u'Крым', max_length=8, choices=KRITERII)
    price_bracket = models.CharField(verbose_name=u'Бюджет', max_length=64, choices=PRICE_CATEGORIES)

    class Meta:
        verbose_name = u'Товар'
        verbose_name_plural = u'Товары'
        ordering = ['group', 'price_bracket', 'vendor2']


class Query(models.Model):

    objects = models.Manager()

    STATUSES = (
        (u'Запрос', u'Запрос'),
        (u'Лид', u'Лид'),
        (u'Заявка', u'Заявка'),
        (u'Отказ', u'Отказ'),
        (u'Успешно реализован', u'Успешно реализован'),
    )
    PR_TYPES = (
        ('server', u'Сервера'),
        ('shd', u'СХД'),
    )

    PRICE_CAT = (
        ('noname', u'No name'),
        ('avrg', u'Средняя цена'),
        ('premium', u'Premium'),
    )

    CERTIFICATE = (
        ('none', u'нет'),
        ('torp', u'ТОРП'),
        ('st1', u'СТ1'),
        ('eac', u'EAC'),
    )

    DANET = (
        (u'Да', u'Да'),
        (u'Нет', u'Нет'),
    )

    name = models.CharField(verbose_name=u'Название заказа', max_length=128, blank=True)
    client = models.ForeignKey(Client, on_delete=models.DO_NOTHING)
    manager = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    status = models.CharField(verbose_name=u'Статус', max_length=64, choices=STATUSES)
    added_at = models.DateTimeField(auto_now_add=True)
    changed_at = models.DateTimeField(auto_now=True)

    query_items = models.ManyToManyField(Item, verbose_name=u'Запрос', related_name='q_items', symmetrical=False)
    lead_items = models.ManyToManyField(Item, verbose_name=u'Лид', related_name='l_items', symmetrical=False)
    order_items = models.ManyToManyField(Item, verbose_name=u'Заявка', related_name='o_items', symmetrical=False, blank=True)

    decline_reason = models.TextField(verbose_name=u'Причина отказа', blank=True)
    comments = models.TextField(verbose_name=u'Примечания к заказу', blank=True)

    survey = models.BooleanField(verbose_name=u'Опрос пройден', default=False)
    product_type = models.CharField(verbose_name=u'Направление', max_length=64, choices=PR_TYPES)
    upgrade = models.BooleanField(verbose_name=u'Апгрейд', choices=DANET)
    fav_brands = models.CharField(verbose_name=u'Ценовая категория предпочитаемых брендов', max_length=128, choices=PRICE_CAT)
    certificate = models.CharField(verbose_name=u'Сертификация', max_length=32, choices=CERTIFICATE)
    survey_comments = models.TextField(verbose_name=u'Примечания к опросу', blank=True)

    class Meta:
        verbose_name = u'Заявка'
        verbose_name_plural = u'Заявки'
        ordering = ['-added_at']
