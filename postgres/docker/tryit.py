from helper import db

class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column(db.String)
    password = db.Column(db.String)
    organization_id  = db.Column(db.Integer, db.ForeignKey('organization.id'))

class Organization(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

def test_foo():
    org = Organization(name='Veracode')
    db.session.add(org)
    db.session.commit()
    assert org.id is not None

    user1 = Users(name='pytest', password='X', organization_id=org.id)
    user2 = Users(name='jrtest', password='X', organization_id=org.id)
    db.session.add(user1)
    db.session.add(user2)
    db.session.commit()
    assert user1.id is not None
    assert user2.id is not None

    oid = db.session.query(Users.organization_id).filter(Users.name == 'pytest')
    query = db.session.query(Users.name).filter(Users.organization_id == oid)
    u = query.all()      # No database hit until we say ".all()"
    assert len(u) == 2
    assert set([x.name for x in u]) == set(['jrtest', 'pytest'])

    Users.query.delete()
    Organization.query.delete()
    db.session.commit()
