import unittest
from datetime import datetime, timedelta
from app import my_app, db
from app.models import User, Post
from hashlib import md5

class MyTestCase(unittest.TestCase):
    def setUp(self):
        my_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_password_hashing(self):
        u = User(username="Vasiliy")
        u.set_password("password")
        self.assertFalse(u.check_password("word"))
        self.assertTrue(u.check_password("password"))

    def test_avatar(self):
        u = User(username="John", email="connor@gmail.com")
        mail_hash = md5(u.email.lower().encode('utf-8')).hexdigest()
        self.assertEqual(u.avatar(128), "https://www.gravatar.com/avatar/"+mail_hash+"?d=identicon&s=128")

    def test_follow(self):
        u1 = User(username="Ivan", email="ivan@yandex.ru")
        u2 = User(username="Petya", email="petya@virus.ru")
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        self.assertEqual(u1.followed.all(), [])
        self.assertEqual(u1.followers.all(), [])

        u1.follow(u2)
        db.session.commit()
        self.assertTrue(u1.is_following(u2))
        self.assertEqual(u1.followed.count(), 1)
        self.assertEqual(u1.followed.first(), u2)
        self.assertEqual(u2.followers.count(), 1)
        self.assertEqual(u2.followers.first(), u1)

    def test_follow_posts(self):
        # 4 пользователя
        a = User(username="Albert", email="albert@mail.ru")
        b = User(username="Bob", email="bob@mail.ru")
        d = User(username="David", email="david@mail.ru")
        f = User(username="Fred", email="fred@mail.ru")

        # 4 поста
        now = datetime.utcnow()
        p1 = Post(body="Albert wants to say smth", author=a, timestamp=now+timedelta(seconds=40))
        p2 = Post(body="Bob wants to say smth too", author=b, timestamp=now+timedelta(seconds=48))
        p3 = Post(body="David said smth", author=d, timestamp=now+timedelta(seconds=45))
        p4 = Post(body="Fred wants to say smth to Bob", author=f, timestamp=now+timedelta(seconds=42))
        db.session.add_all([p1, p2, p3, p4])
        db.session.commit()

        # подписки
        a.follow(b)
        a.follow(f)
        b.follow(d)
        d.follow(f)
        db.session.commit()

        # проверка
        pa = a.followed_posts().all()
        pb = b.followed_posts().all()
        pd = d.followed_posts().all()
        pf = f.followed_posts().all()
        self.assertEqual(pa, [p2, p4, p1])
        self.assertEqual(pb, [p2, p3])
        self.assertEqual(pd, [p3, p4])
        self.assertEqual(pf, [p4])



if __name__ == '__main__':
    unittest.main(verbosity = 2)
