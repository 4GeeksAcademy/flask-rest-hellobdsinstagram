from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# en este trabajo me llevo bastante por que no sabia como hacer la relacion entre el estado del usuario y el usuario, al final lo hice con una clave foranea y me costo bastante entenderlo, pero al final lo logre y creo que quedo bastante bien, espero que les guste el resultado final
# me tuve que apoyar en la IA pero por motivos artisticos y de aprendizaje, ya que no tenia mucha experiencia con SQLAlchemy y me ayudo a entender mejor como funciona la relacion entre las tablas, ademas de que me dio ideas para mejorar el diseño de la base de datos, espero que les guste el resultado final


class EstadoUsuario(db.Model):
    __tablename__ = 'estado_usuario'

    IdEstate = db.Column(db.Integer, primary_key=True)
    NameEstate = db.Column(db.String(50), nullable=False)


class Usuario(db.Model):
    __tablename__ = 'usuario'

    IdUsuario = db.Column(db.Integer, primary_key=True)
    UserName = db.Column(db.String(50), unique=True, nullable=False)
    Name = db.Column(db.String(100), nullable=False)  # full_name
    Mail = db.Column(db.String(100), unique=True, nullable=False)
    Photo = db.Column(db.String(255))  # profile_picture_url
    PasswordHash = db.Column(db.String(255), nullable=False)
    RegisterDate = db.Column(db.DateTime, default=datetime.utcnow)
    Bio = db.Column(db.Text)  # bio
    Website = db.Column(db.String(255))  # website
    IsPrivate = db.Column(db.Boolean, default=False)  # is_private

    IdEstate = db.Column(
        db.Integer,
        db.ForeignKey('estado_usuario.IdEstate'),
        nullable=False
    )

    posts = db.relationship('Post', backref='author', lazy=True)
    comments = db.relationship('Comment', backref='commenter', lazy=True)
    likes = db.relationship('Like', backref='liker', lazy=True)
    followers = db.relationship(
        'Follower', foreign_keys='Follower.followed_id', backref='followed', lazy=True)
    following = db.relationship(
        'Follower', foreign_keys='Follower.follower_id', backref='follower', lazy=True)


class Post(db.Model):
    __tablename__ = 'post'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'usuario.IdUsuario'), nullable=False)
    # URL de la imagen/video esto costo bastante :/
    media_url = db.Column(db.String(255), nullable=False)
    caption = db.Column(db.Text)
    location = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relaciones
    comments = db.relationship('Comment', backref='post', lazy=True)
    likes = db.relationship('Like', backref='post', lazy=True)


class Comment(db.Model):
    __tablename__ = 'comment'

    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'usuario.IdUsuario'), nullable=False)
    text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Like(db.Model):
    __tablename__ = 'like'

    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'usuario.IdUsuario'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Follower(db.Model):
    __tablename__ = 'follower'

    id = db.Column(db.Integer, primary_key=True)
    follower_id = db.Column(db.Integer, db.ForeignKey(
        'usuario.IdUsuario'), nullable=False)
    followed_id = db.Column(db.Integer, db.ForeignKey(
        'usuario.IdUsuario'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


if __name__ == '__main__':
    from sqlalchemy import create_engine
    from sqlalchemy_schemadisplay import create_schema_graph

    engine = create_engine('sqlite:///:memory:')
    db.metadata.create_all(engine)

    graph = create_schema_graph(metadata=db.metadata, engine=engine, show_datatypes=True,
                                show_indexes=True, rankdir='LR', concentrate=False)
    graph.write_png('diagram.png')
    print("Diagrama generado: diagram.png")
