

manager = Group(name="Manager")
manager.save()
user = User.objects.get(pk=2)
user.save()
user.groups.add(manager)
