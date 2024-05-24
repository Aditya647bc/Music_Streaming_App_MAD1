import base64
from io import BytesIO
import os
from flask import Flask, session
from flask import render_template
from flask import request, redirect, url_for, current_app, flash 
from flask_sqlalchemy import SQLAlchemy
from matplotlib import pyplot as plt
current_dir = os.path.abspath(os.path.dirname(__file__))
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///"+os.path.join(current_dir, "testdb.sqlite3")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.secret_key='Aditya'

db = SQLAlchemy(app)

app.app_context().push()

# MODELS OF THE APP :-

class User(db.Model):
    __tablename__ = 'user'
    User_id = db.Column(db.Integer, primary_key=True)
    Email = db.Column(db.String, nullable=False)
    UserName = db.Column(db.String, unique=True, nullable=False)
    Name = db.Column(db.String, nullable=False)
    Password = db.Column(db.String, nullable=False)
    Status = db.Column(db.String, default='User')
    PlaylistR = db.relationship('Playlist', backref='user', lazy=True)
    RatingR = db.relationship('Rating', backref='user', lazy=True)
    AlbumR = db.relationship('Album', backref='user', lazy=True)
    SongR = db.relationship('Song', backref='user', lazy=True)

class Album(db.Model):
    __tablename__ = 'album'
    Album_id = db.Column(db.Integer, primary_key=True, autoincrement= True)
    Name = db.Column(db.String, nullable=False)
    Artist = db.Column(db.String, nullable=False)
    User_id = db.Column(db.Integer,db.ForeignKey('user.User_id'), nullable=False)
    SongR = db.relationship('Song', backref='album', lazy=True)


class Song(db.Model):
    __tablename__ = 'song'
    Song_id = db.Column(db.Integer, primary_key=True, autoincrement =True)
    Name = db.Column(db.String, nullable=False)
    Lyrics = db.Column(db.String, nullable=False)
    Artist = db.Column(db.String, nullable=False)
    Genre = db.Column(db.String, nullable=False)
    Song_path = db.Column(db.String, nullable=False)
    Rating = db.Column(db.Integer, default=0)
    User_id = db.Column(db.Integer,db.ForeignKey('user.User_id'), nullable=False)
    Album_id = db.Column(db.Integer, db.ForeignKey('album.Album_id'), nullable=False)
    Rating_relationship = db.relationship('Rating', backref='song', lazy=True)

class Playlist(db.Model):
    __tablename__ = 'playlist'
    Playlist_id = db.Column(db.Integer,primary_key = True)
    Name = db.Column(db.String, nullable=False)
    User_id = db.Column(db.Integer,db.ForeignKey('user.User_id'), nullable=False)
    Songs_list = db.Column(db.String, nullable=False)

class Rating(db.Model):
    __tablename__ = 'rating'
    Rating_id = db.Column(db.Integer,primary_key = True)
    User_id = db.Column(db.Integer, db.ForeignKey('user.User_id'))
    Song_id = db.Column(db.Integer, db.ForeignKey('song.Song_id'))
    Rating = db.Column(db.Integer)

# ROUTES OF THE APP :-

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/signup', methods=['GET','POST'])
def signup():
    if request.method=='POST':
        Email = request.form['email']
        UserName = request.form['username']
        Name = request.form['name']
        Password = request.form['password']
        user = User(Email = Email , UserName = UserName , Name = Name , Password = Password)
        db.session.add(user)
        db.session.commit()
        session['user'] = UserName
        u = User.query.filter_by(UserName = UserName , Password = Password).first()
        playlist = Playlist.query.filter_by(User_id = u.User_id).all()
        songs = Song.query.all()
        return render_template('home.html', user=u, songs=songs, playlist=playlist)
    
    return render_template("signup.html")

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method=='POST':
        UserName = request.form['username']
        Password = request.form['password']
        user = User.query.filter_by(UserName = UserName , Password = Password).first()
        if user and (user.Status == "User" or user.Status =="Creator"):
            session['user'] = UserName
            songs = Song.query.all()
            playlist = Playlist.query.filter_by(User_id = user.User_id).all()
            return render_template('home.html', user=user, songs=songs, playlist=playlist ,)
        
    return render_template("login.html")

@app.route('/logout')
def logout():
    session.pop('user', None)  
    return render_template("index.html")
  
@app.route('/registercreator', methods=['GET','POST'])
def creator():
    if request.method=='POST':
        UserName = request.form['username']
        Password = request.form['password']
        user = User.query.filter_by(UserName = UserName , Password = Password).first()
        user.Status = "Creator"
        db.session.commit()
        albums = Album.query.filter_by(User_id=user.User_id).all()
        return render_template('c_dashboard.html', albums=albums, song_count= 0, avg=0)
    

    UserName = session.get('user')
    user = User.query.filter_by(UserName = UserName).first()
    albums = Album.query.filter_by(User_id=user.User_id).all()

    song_count = Song.query.filter_by(User_id=user.User_id).all()
    sum = 0
    for i in song_count:
        sum+= i.Rating
    if len(song_count)>0:
        avg = sum/len(song_count)
        avg= round(avg,2)
    else: avg =0
    return render_template('c_dashboard.html', albums=albums, user=user, song_count= len(song_count), avg=avg)


@app.route('/addalbum', methods=['GET','POST'])
def addalbum():
    if request.method=='POST':
        Name = request.form['albumname']
        Artist = request.form['artist']
        UserName = session.get('user')
        user = User.query.filter_by(UserName = UserName).first()
        User_id = user.User_id

        album = Album(Name=Name, Artist=Artist, User_id=User_id)
        db.session.add(album)
        db.session.commit()
        
        UserName = session.get('user')
        user = User.query.filter_by(UserName = UserName).first()
        albums = Album.query.filter_by(User_id=user.User_id).all()

        song_count = Song.query.filter_by(User_id=user.User_id).all()
        sum = 0
        for i in song_count:
            sum+= i.Rating
        if len(song_count)>0:
            avg = sum/len(song_count)
            avg= round(avg,2)
        else: avg =0
        return render_template('c_dashboard.html', albums=albums, user=user, song_count= len(song_count), avg=avg)
    

@app.route('/updatealbum/<Album_id>', methods=['GET','POST'])
def updatealbum(Album_id):
    if request.method=='POST':
        album = Album.query.filter_by(Album_id=Album_id).first()
        album.Name = request.form['albumname']
        album.Artist = request.form['artist']

        db.session.commit()
        
        UserName = session.get('user')
        user = User.query.filter_by(UserName = UserName).first()
        albums = Album.query.filter_by(User_id=user.User_id).all()

        song_count = Song.query.filter_by(User_id=user.User_id).all()
        sum = 0
        for i in song_count:
            sum+= i.Rating
        if len(song_count)>0:
            avg = sum/len(song_count)
            avg= round(avg,2)
        else: avg =0
        return render_template('c_dashboard.html', albums=albums, user=user, song_count= len(song_count), avg=avg)
     
    album = Album.query.filter_by(Album_id=Album_id).first()
    return render_template("updatealbum.html", album=album)
    
@app.route('/deletealbum/<Album_id>', methods=['GET','POST'])
def deletealbum(Album_id):
        album = Album.query.filter_by(Album_id=Album_id).first()
        songs = Song.query.filter_by(Album_id=album.Album_id).all()
        for i in songs:
            deletesong(i.Song_id)
            
        db.session.delete(album)
        db.session.commit()
        return creator()

@app.route('/addsong/<Album_id>', methods=['GET','POST'])
def addsong(Album_id):
    if request.method=='POST':
        Name = request.form['name']
        Lyrics = request.form['lyrics']
        Artist = request.form['artist']
        Genre = request.form['genre']
        MP3_file =request.files['songmp3']  

        upload_folder = 'static'
        os.makedirs(upload_folder, exist_ok=True)

        filename = secure_filename(MP3_file.filename)
        file_path = os.path.join(upload_folder, filename)
        MP3_file.save(file_path)

        Song_path = filename

        UserName = session.get('user')
        user = User.query.filter_by(UserName = UserName).first()
        User_id = user.User_id

        song = Song(Name=Name, Artist=Artist, Lyrics=Lyrics, Genre=Genre, Song_path=Song_path, User_id=User_id,Album_id=Album_id)
        db.session.add(song)
        db.session.commit()

        songs = Song.query.filter_by(Album_id=Album_id).all()
        album = Album.query.filter_by(Album_id=Album_id).first()
        return render_template("addsong.html", album=album, songs=songs)
    
    songs = Song.query.filter_by(Album_id=Album_id).all()
    album = Album.query.filter_by(Album_id=Album_id).first()
    return render_template("addsong.html", album=album, songs=songs)

@app.route('/deletesong/<Song_id>', methods=['GET','POST'])
def deletesong(Song_id):
        song = Song.query.filter_by(Song_id=Song_id).first()
        s = Rating.query.filter_by(Song_id=Song_id).all()
        for i in s:
            db.session.delete(i)
            db.session.commit()
        Album_id = song.Album_id
        db.session.delete(song)
        db.session.commit()
    
        songs = Song.query.filter_by(Album_id=Album_id).all()
        album = Album.query.filter_by(Album_id=Album_id).first()
        return render_template("addsong.html", album=album, songs=songs)

@app.route('/updatesong/<Song_id>', methods=['GET','POST'])
def upadtesong(Song_id):
    if request.method=='POST':
        song = Song.query.filter_by(Song_id=Song_id).first()
        song.Name = request.form['name']
        song.Lyrics = request.form['lyrics']
        song.Artist = request.form['artist']
        song.Genre = request.form['genre']
        db.session.commit()

        songs = Song.query.filter_by(Album_id=song.Album_id).all()
        album = Album.query.filter_by(Album_id=song.Album_id).first()
        return render_template("addsong.html", album=album, songs=songs)
    
    song = Song.query.filter_by(Song_id=Song_id).first()
    return render_template("updatesong.html", song=song)

@app.route('/rate/<int:rate>/<Song_id>', methods=['GET','POST'])
def ratesong(rate,Song_id):
    UserName = session.get('user')
    user = User.query.filter_by(UserName = UserName).first()
    User_id = user.User_id

    rating = Rating.query.filter_by(User_id=User_id, Song_id=Song_id).first()

    if rating:
        rating.Rating = rate
    else:
        r = Rating(User_id=User_id, Song_id=Song_id, Rating=rate)
        db.session.add(r)
        db.session.commit()
    
    ratings = Rating.query.filter_by(Song_id=Song_id).all()
    sum = 0
    for a in ratings:
        sum+= a.Rating

    avg = sum/len(ratings)
    song = Song.query.filter_by(Song_id=Song_id).first()
    song.Rating = round(avg,2)
    db.session.commit()

    songs = Song.query.all()
    playlist = Playlist.query.filter_by(User_id = user.User_id).all()
    return render_template('home.html', songs=songs, user=user,playlist=playlist)

@app.route('/playlist/<Song_id>', methods=['GET','POST'])
def playlist(Song_id):
    if request.method=='POST':
        Name = request.form['name']
        playlist = request.form.get("playlist")

        UserName = session.get('user')
        user = User.query.filter_by(UserName = UserName).first()
        User_id = user.User_id

        if Name:
            p = Playlist(User_id=User_id, Name=Name, Songs_list = Song_id)
            db.session.add(p)
            db.session.commit()
        
        else:
            p = Playlist.query.filter_by(Playlist_id = playlist).first()
            songlist = p.Songs_list.split(', ')
            songlist.append(Song_id)
            songlist = list(set(songlist))
            p.Songs_list = ', '.join(songlist)
            db.session.commit()

        
        songs = Song.query.all()
        pp = Playlist.query.filter_by(User_id = user.User_id).all()
        return render_template('home.html', songs=songs, user=user,playlist=pp)
    
@app.route('/playlist_go/<Playlist_id>', methods=['GET','POST'])
def playlist_go(Playlist_id):
    playlist = Playlist.query.filter_by(Playlist_id=Playlist_id).first()
    songs = []
    for i in playlist.Songs_list.split(', '):
        songs.append(Song.query.filter_by(Song_id= i).first())

    user = User.query.filter_by(UserName = session.get('user')).first()
    pp = Playlist.query.filter_by(User_id = user.User_id).all()
    return render_template('playlist.html', songs=songs, p = playlist)

@app.route('/deleteplaylist/<Playlist_id>/<p>/<id>', methods=['GET','POST'])
def deleteplaylist(Playlist_id, p,id):
    if p == 'whole':
        db.session.delete(Playlist.query.filter_by(Playlist_id = id).first())
        db.session.commit()

        user = User.query.filter_by(UserName = session.get('user')).first()
        songs = Song.query.all()
        pp = Playlist.query.filter_by(User_id = user.User_id).all()
        return render_template('home.html', songs=songs, user=user,playlist=pp)

    elif p =='song':
        playlist = Playlist.query.filter_by(Playlist_id = Playlist_id).first()
        if len(playlist.Songs_list.split(', ')) == 1:

            db.session.delete(Playlist.query.filter_by(Playlist_id = Playlist_id).first())
            db.session.commit()

            user = User.query.filter_by(UserName = session.get('user')).first()
            songs = Song.query.all()
            pp = Playlist.query.filter_by(User_id = user.User_id).all()
            return render_template('home.html', songs=songs, user=user,playlist=pp)
        else:
            p= playlist.Songs_list.split(', ')
            p.remove(id)
            playlist.Songs_list = ', '.join(p)
            db.session.commit()
            return playlist_go(Playlist_id)
        

@app.route('/adminlogin', methods=['GET', 'POST'])
def adminlogin():
    if request.method == 'POST':
        UserName = request.form['username']
        Password = request.form['password']
        admin = User.query.filter_by(UserName=UserName, Password=Password, Status="Admin").first()

        if admin:
            creator_count = User.query.filter_by(Status="Creator").count()
            user_count = User.query.filter_by(Status="User").count()
            song_count = Song.query.count()
            album_count = Album.query.count()
            genres_count = db.session.query(Song.Genre).distinct().count()

            songs = Song.query.all()
            song_names = [song.Name for song in songs]
            ratings = [song.Rating for song in songs]

            plt.figure(figsize=(10, 6))
            plt.bar(song_names, ratings, color='blue')
            plt.xlabel('Songs')
            plt.ylabel('Ratings')
            plt.title('Songs and Ratings')
            plt.xticks(rotation=45, ha='right')

            img_bar = BytesIO()
            plt.savefig(img_bar, format='png')
            img_bar.seek(0)

            graph_html = base64.b64encode(img_bar.getvalue()).decode()

            labels = ['Creator', 'User']
            sizes = [creator_count, user_count]
            colors = ['blue', 'skyblue']

            plt.figure(figsize=(6, 6))
            plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%')
            plt.axis('equal')

            img_pie = BytesIO()
            plt.savefig(img_pie, format='png')
            img_pie.seek(0)

            pie_chart_html = base64.b64encode(img_pie.getvalue()).decode()

            return render_template("admin_dashboard.html" , creator_count=creator_count, user_count=user_count,
                                   song_count=song_count, album_count=album_count, genre_count=genres_count,
                                   graph_html=graph_html, pie_chart_html=pie_chart_html)

    return render_template('adminlogin.html')


@app.route('/flagsongs', methods=['GET','POST'])
def flagsongs():
    genres = db.session.query(Song.Genre).distinct().all()
    songs = []
    for g in genres:
        s= Song.query.filter_by(Genre=g[0]).all()
        obj = {"genre":g[0], "songs":s}
        songs.append(obj)
    return render_template("flagsongs.html", songs=songs, genres=genres)

@app.route('/deletesong_byadmin/<Song_id>', methods=['GET','POST'])
def deletesong_byadmin(Song_id):
    deletesong(Song_id)
    return flagsongs()

@app.route('/search', methods=['GET','POST'])
def search():
    if request.method == 'POST':
        search_field = request.form['search'] 
        songs_g = Song.query.filter(Song.Genre.ilike(search_field)).all()
        songs_n = Song.query.filter(Song.Name.ilike(search_field)).all()


        return render_template('search.html', songs_g=songs_g, songs_n=songs_n)
    
    
if __name__ == '__main__':
    app.debug=True
    app.run () 

