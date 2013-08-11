import factory
from django.contrib.auth.hashers import make_password
from resrc.userprofile.models import Profile


class UserF(factory.django.DjangoModelFactory):
  FACTORY_FOR = Profile
  first_name = factory.Sequence(lambda n: "First%s" % n)
  last_name = factory.Sequence(lambda n: "Last%s" % n)
  email = factory.Sequence(lambda n: "email%s@example.com" % n)
  username = factory.Sequence(lambda n: "email%s@example.com" % n)
  password = make_password("password")
  show_email = False
  is_staff = False
