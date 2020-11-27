import json


class Model(object):
    def __repr__(self):
        cls_name = self.__class__.__name__
        properties = ['{}: ({})'.format(k, v) for k, v in self.__dict__.items()]
        s = '\n'.join(properties)
        return '< {}\n{} >\n'.format(cls_name, s)

    @staticmethod
    def save_file(data, path):
        s = json.dumps(data, indent=2, ensure_ascii=False)
        with open(path, 'w+', encoding='utf-8') as f:
            f.write(s)

    @staticmethod
    def load_file(path):
        with open(path, 'r', encoding='utf-8') as f:
            s = f.read()
            return json.loads(s)

    @classmethod
    def db_path(cls):
        """
        :return: path
        """
        classname = cls.__name__
        path = 'data/{}.txt'.format(classname)
        return path

    @classmethod
    def new(cls, form):
        m = cls(form)
        return m

    @classmethod
    def all(cls):
        path = cls.db_path()
        models = cls.load_file(path)
        ms = [cls.new(m) for m in models]
        return ms

    @classmethod
    def find_by(cls, **kwargs):
        for key, value in kwargs.items():
            pass
        all = cls.all()
        for m in all:
            if value == getattr(m, key):
                return m
        return None

    def save(self):
        models = self.all()
        if getattr(self, 'id') is None:
            if len(models) > 0:
                self.id = models[-1].id + 1
            else:
                self.id = 0
            models.append(self)
        else:
            for i, m in enumerate(models):
                if m.id == self.id:
                    models[i] = self
                    break
        l = [m.__dict__ for m in models]
        path = self.db_path()
        self.save_file(l, path)

    def remove(self):
        models = self.all()
        if getattr(self, 'id') is not None:
            for i, m in enumerate(models):
                if m.id == self.id:
                    del models[i]
                    break
        l = [m.__dict__ for m in models]
        path = self.db_path()
        self.save_file(l, path)


class User(Model):
    def __init__(self, form):
        self.id = form.get('id', None)
        if self.id is not None:
            self.id = int(self.id)
        self.username = form.get('username', '')
        self.password = form.get('password', '')

    def validate_login(self):
        u = User.find_by(username=self.username)
        return u is not None and u.password == self.password
