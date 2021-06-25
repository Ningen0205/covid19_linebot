from models import Users,Posts

Users.objects.create(name="harano")
Users.objects.create(name="yoshino")
Users.objects.create(name="ariyama")
Users.objects.create(name="tyosokabe")

Posts.objects.create(user_id=1,content="こんばんは")
Posts.objects.create(user_id=2,content="おはよう")
Posts.objects.create(user_id=4,content="めしうまい")