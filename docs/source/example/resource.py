import infosystem

class Foo(infosystem.Resource):
    name = Column(db.String(80), nullable=False)
