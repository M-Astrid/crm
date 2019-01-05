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
        (u'?', u'?'),
    )

    form = models.CharField(verbose_name=u'Форма', max_length=16, choices=ORG_FORMS)  # !!! дополнить выпадающий список
    name = models.CharField(verbose_name=u'Название организации', max_length=128)
    inn = models.IntegerField(verbose_name=u'ИНН')  # посмотреть API налоговой для проверки фирмы

    basic_survey = models.BooleanField(verbose_name=u'Базовый опрос пройден', default=False)
    type = models.CharField(verbose_name=u'Тип организации', max_length=64, choices=ORG_TYPES, blank=True)
    sanctions = models.CharField(verbose_name=u'Санкции', max_length=6, blank=True, choices=DANET)
    crimea = models.CharField(verbose_name=u'Крым', max_length=6, blank=True, choices=DANET)
    imp = models.CharField(verbose_name=u'Импортозамещение', max_length=6, blank=True, choices=DANET)

    added_at = models.DateTimeField(verbose_name=u'Клиент добавлен', auto_now_add=True)
    changed_at = models.DateTimeField(auto_now=True)
    manager = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    #query = models.ForeignKey(, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = u'Клиент'
        verbose_name_plural = u'Клиенты'
        ordering = ['name']

    def get_field_names(self):
        fields = [f.name for f in self._meta.get_fields()]
        for i in ['id', 'form', 'name', 'inn', 'basic_survey', 'manager', 'changed_at', 'added_at']:
            fields.remove(i)
        return fields

    def get_absolute_url(self):
        return "/clients/%i/add-contact/" % self.pk


# DELETE!
class Contact(models.Model):                      # DELETE!

    objects = models.Manager()

    first_name = models.CharField(verbose_name=u'Имя', max_length=64)
    father_name = models.CharField(verbose_name=u'Отчество', max_length=64)
    last_name = models.CharField(verbose_name=u'Фамилия', max_length=64)
    phone_number = models.CharField(verbose_name=u'Телефон', max_length=14, blank=True)
    phone_number2 = models.CharField(verbose_name=u'Доп. телефон', max_length=14, blank=True)
    email = models.EmailField(verbose_name=u'E-mail', blank=True)
    position = models.CharField(verbose_name=u'Должность', max_length=128)

    class Meta:
        verbose_name = u'Контактное лицо'
        verbose_name_plural = u'Контактые лица'
        ordering = ['last_name']


class Person(models.Model):

    objects = models.Manager()

    first_name = models.CharField(verbose_name=u'Имя', max_length=64)
    father_name = models.CharField(verbose_name=u'Отчество', max_length=64)
    last_name = models.CharField(verbose_name=u'Фамилия', max_length=64)
    phone_number = models.CharField(verbose_name=u'Телефон', max_length=14, blank=True)
    phone_number2 = models.CharField(verbose_name=u'Доп. телефон', max_length=14, blank=True)
    email = models.EmailField(verbose_name=u'E-mail', blank=True)
    position = models.CharField(verbose_name=u'Должность', max_length=128)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = u'Контакт'
        verbose_name_plural = u'Контакты'
        ordering = ['pk']

    def get_absolute_url(self):
        return "/clients/%i/" % self.client.pk


# DELETE!
class PersonChange(models.Model):

    objects = models.Manager()

    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    manager = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True)
    changed_at = models.DateTimeField(auto_now_add=True)
    change = models.TextField(blank=True)


class ClientChange(models.Model):

    objects = models.Manager()

    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    manager = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True)
    changed_at = models.DateTimeField(auto_now_add=True)
    ch_type = models.CharField(max_length=64)
    change = models.TextField(blank=True)

    type = models.CharField(verbose_name=u'Тип организации(old)', max_length=64, blank=True)
    sanctions = models.CharField(verbose_name=u'Санкции(old)', max_length=6, blank=True)
    crimea = models.CharField(verbose_name=u'Крым(old)', max_length=6, blank=True)
    imp = models.CharField(verbose_name=u'Импортозамещение(old)', max_length=6, blank=True)

    first_name = models.CharField(verbose_name=u'Имя', max_length=64, blank=True)
    father_name = models.CharField(verbose_name=u'Отчество', max_length=64, blank=True)
    last_name = models.CharField(verbose_name=u'Фамилия', max_length=64, blank=True)
    phone_number = models.CharField(verbose_name=u'Телефон', max_length=14, blank=True)
    phone_number2 = models.CharField(verbose_name=u'Доп. телефон', max_length=14, blank=True)
    email = models.EmailField(verbose_name=u'E-mail', blank=True)
    position = models.CharField(verbose_name=u'Должность', max_length=128, blank=True)

    class Meta:
        ordering = ['-id']


class Item(models.Model):

    objects = models.Manager()

    KRITERII = (
        ('+','+'),
        ('-','-'),
        ('?','?'),
    )

    PRICE_CAT = (
        (u'(1)Premium', u'(1)Premium'),
        (u'(2)Средняя цен. кат.', u'(2)Средняя цен. кат.'),
        (u'(3)No name', u'(3)No name'),
    )

    PR_TYPES = (
        (u'Сервера', u'Сервера'),
        (u'СХД', u'СХД'),
    )

    CERTIFICATE = (
        (u'?', u'?'),
        (u'ТОРП', u'ТОРП'),
        (u'СТ1', u'СТ1'),
        (u'EAC', u'EAC'),
    )

    FORM_FACT = (
        (u'Форм-фактор Rack', u'Форм-фактор Rack'),
        (u'Форм-фактор Tower', u'Форм-фактор Tower'),
        (u'Блейд-сервер', u'Блейд-сервер'),
    )

    SHD_TYPES = (
        (u'СХД начального уровня', u'СХД начального уровня'),
        (u'СХД общего назначения', u'СХД общего назначения'),
        (u'Гибридная СХД', u'Гибридная СХД'),
        (u'СХД для резервного копирования', u'СХД для резервного копирования'),
        (u'СХД высокопроизводительного класса', u'СХД высокопроизводительного класса'),
        (u'СХД система NAS', u'СХД система NAS'),
        (u'СХД для расширения VMware', u'СХД для расширения VMware'),
        (u'Программно-определяемая СХД', u'Программно-определяемая СХД'),
        (u'СХД для видеоконтента', u'СХД для видеоконтента'),
    )

    DANET = (
        (u'Да', u'Да'),
        (u'Нет', u'Нет'),
        (u'?', u'?'),
    )

    group = models.CharField(max_length=64)
    model_row = models.CharField(max_length=64)
    vendor1 = models.CharField(max_length=64)
    model = models.CharField(max_length=64)
    SKU = models.CharField(max_length=64)
    vendor2 = models.CharField(max_length=64)
    model2 = models.CharField(max_length=64)
    SKU2 = models.CharField(max_length=64)

    product_type = models.CharField(verbose_name=u'Направление', max_length=64, null=True, choices=PR_TYPES)
    form_factor = models.CharField(verbose_name=u'Форм-фактор сервера', max_length=64, blank=True, null=True, choices=FORM_FACT)
    type = models.CharField(verbose_name=u'Тип СХД', max_length=64, blank=True, null=True, choices=SHD_TYPES)
    certificate = models.CharField(verbose_name=u'Сертификация', max_length=32, default=u'?', choices=CERTIFICATE)
    upgrade = models.CharField(verbose_name=u'Апгрейд', max_length=6, null=True, choices=DANET)
    #ST1 = models.CharField(verbose_name=u'СТ1 ГОС образца', max_length=8, choices=KRITERII)
    #torp = models.CharField(verbose_name=u'Сертификат ТОРП', max_length=8, choices=KRITERII)
    #eac = models.CharField(verbose_name=u'EAC', max_length=8, choices=KRITERII)
    sanctions = models.CharField(verbose_name=u'Санкции', max_length=8, choices=DANET)
    crimea = models.CharField(verbose_name=u'Крым', max_length=8, choices=DANET)
    imp = models.CharField(verbose_name=u'Импортозамещение', max_length=6, blank=True, choices=DANET)
    price_bracket = models.CharField(verbose_name=u'Бюджет', max_length=64, choices=PRICE_CAT)


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
        (u'Сервера', u'Сервера'),
        (u'СХД', u'СХД'),
    )

    FORM_FACT = (
        (u'Форм-фактор Rack', u'Форм-фактор Rack'),
        (u'Форм-фактор Tower', u'Форм-фактор Tower'),
        (u'Блейд-сервер', u'Блейд-сервер'),
    )

    SHD_TYPES = (
        (u'СХД начального уровня', u'СХД начального уровня'),
        (u'СХД общего назначения', u'СХД общего назначения'),
        (u'Гибридная СХД', u'Гибридная СХД'),
        (u'СХД для резервного копирования', u'СХД для резервного копирования'),
        (u'СХД высокопроизводительного класса', u'СХД высокопроизводительного класса'),
        (u'СХД система NAS', u'СХД система NAS'),
        (u'СХД для расширения VMware', u'СХД для расширения VMware'),
        (u'Программно-определяемая СХД', u'Программно-определяемая СХД'),
        (u'СХД для видеоконтента', u'СХД для видеоконтента'),
    )

    PRICE_CAT = (
        (u'(1)Premium', u'(1)Premium'),
        (u'(2)Средняя цен. кат.', u'(2)Средняя цен. кат.'),
        (u'(3)No name', u'(3)No name'),
    )

    CERTIFICATE = (
        (u'?', u'?'),
        (u'ТОРП', u'ТОРП'),
        (u'СТ1', u'СТ1'),
        (u'EAC', u'EAC'),
    )

    DANET = (
        (u'Да', u'Да'),
        (u'Нет', u'Нет'),
        (u'?', u'?'),
    )

    name = models.CharField(verbose_name=u'Название заказа', max_length=128, blank=True)
    client = models.ForeignKey(Client, null=True, on_delete=models.SET_NULL, related_name='queries')
    manager = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    status = models.CharField(verbose_name=u'Статус', max_length=64, choices=STATUSES)
    added_at = models.DateTimeField(auto_now_add=True)
    changed_at = models.DateTimeField(auto_now=True)

    query_items = models.ManyToManyField(Item, verbose_name=u'Запрос', null=True, related_name='q_items')
    lead_items = models.ManyToManyField(Item, verbose_name=u'Лид', null=True, related_name='l_items')
    order_items = models.ManyToManyField(Item, verbose_name=u'Заявка', null=True, related_name='o_items')

    decline_reason = models.TextField(verbose_name=u'Причина отказа', blank=True)
    comments = models.TextField(verbose_name=u'Примечания к заказу', blank=True)

    survey = models.BooleanField(verbose_name=u'Опрос пройден', default=False)

    product_type = models.CharField(verbose_name=u'Направление', max_length=64, null=True, choices=PR_TYPES)
    form_factor = models.CharField(verbose_name=u'Форм-фактор сервера', blank=True, max_length=64, null=True, choices=FORM_FACT)
    type = models.CharField(verbose_name=u'Тип СХД', max_length=64, blank=True, null=True, choices=SHD_TYPES)
    upgrade = models.CharField(verbose_name=u'Апгрейд', max_length=6, null=True, choices=DANET)
    certificate = models.CharField(verbose_name=u'Сертификация', max_length=32, default=u'EAC', choices=CERTIFICATE)
    fav_brands = models.CharField(verbose_name=u'Ценовая категория предпочитаемых брендов', max_length=128, choices=PRICE_CAT)

    survey_comments = models.TextField(verbose_name=u'Примечания к опросу', blank=True)

    class Meta:
        verbose_name = u'Заявка'
        verbose_name_plural = u'Заявки'
        ordering = ['-added_at']


class Block(models.Model):

    server = models.TextField(verbose_name=u'Сервера', blank=True)
    shd = models.TextField(verbose_name=u'СХД', blank=True)
    server_rack = models.TextField(verbose_name=u'Сервер в форм факторе Rack', blank=True)
    server_tower = models.TextField(verbose_name=u'Сервер в форм факторе Tower', blank=True)
    blade_server = models.TextField(verbose_name=u'Блейд-сервер', blank=True)
    conv_inf = models.TextField(verbose_name=u'Конвергентная инфраструктура', blank=True)
    shd_high = models.TextField(verbose_name=u'СХД высокопроизводительного класса', blank=True)
    shd_common = models.TextField(verbose_name=u'СХД общего назначения', blank=True)
    shd_begin = models.TextField(verbose_name=u'СХД начального уровня', blank=True)
    shd_nas = models.TextField(verbose_name=u'СХД система NAS', blank=True)
    shd_hybrid = models.TextField(verbose_name=u'Гибридная СХД', blank=True)
    shd_reserv = models.TextField(verbose_name=u'СХД для резервного копирования', blank=True)
    shd_vmware = models.TextField(verbose_name=u'СХД для расширения VMware', blank=True)
    shd_video = models.TextField(verbose_name=u'СХД для видеоконтента', blank=True)
    shd_program = models.TextField(verbose_name=u'Программно-определяемая СХД', blank=True)
    new = models.TextField(verbose_name=u'Покупка новых готовых систем', blank=True)
    upgrade = models.TextField(verbose_name=u'Upgrade', blank=True)
    early_dell = models.TextField(verbose_name=u'Ранее закупали Dell', blank=True)
    early_emc = models.TextField(verbose_name=u'Ранее закупали EMC', blank=True)
    early_huawei = models.TextField(verbose_name=u'Ранее закупали Huawei', blank=True)
    early_sugon = models.TextField(verbose_name=u'Ранее закупали SUGON', blank=True)
    dell = models.TextField(verbose_name=u'Заказывают Dell', blank=True)
    emc = models.TextField(verbose_name=u'Заказывают EMC', blank=True)
    huawei = models.TextField(verbose_name=u'Заказывают Huawei', blank=True)
    sugon = models.TextField(verbose_name=u'Заказывают SUGON', blank=True)
    ending = models.TextField(verbose_name=u'Завершающий блок', blank=True)

    class Meta:
        verbose_name = u'Текстовые блоки'
        verbose_name_plural = u'Текстовые блоки'

