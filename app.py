import numpy as np
import pickle
from flask import Flask,render_template,request
import os
picfolder = os.path.join('static', 'images')



popular_df=pickle.load(open('popular.pkl','rb'))
pt = pickle.load(open('pt.pkl','rb'))
similarity_score = pickle.load(open('similarity_score.pkl','rb'))
books = pickle.load(open('books.pkl','rb'))

app= Flask(__name__)

app.config['UPLOAD_FOLDER'] = picfolder
@app.route('/')
def index():
    return render_template('index.html',
                           book_name=list(popular_df['Book-Title'].values),
                           author=list(popular_df['Book-Author'].values),
                           image=list(popular_df['Image-URL-M'].values),
                           votes=list(popular_df['num_ratings'].values),
                           ratings=list(popular_df['avg_ratings'].values)
                           )

@app.route('/recommend')
def recommend_ui():
    pic1=os.path.join(app.config['UPLOAD_FOLDER'],'book logo 2.png')
    return render_template('recommend.html',methods=['POST'],user_image=pic1)

@app.route('/recommend_books',methods=['post'])
def recommend():

    user_input = request.form.get('user_input')
    index = np.where(pt.index == user_input)[0][0]
    similar_items = sorted(list(enumerate(similarity_score[index])), key=lambda x: x[1], reverse=True)[1:5]
    data = []
    for i in similar_items:
        itmes = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        itmes.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        itmes.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        itmes.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
        data.append(itmes)
    print(data)
    return render_template('recommend.html',data=data)

@app.route('/contact')
def details():
    return render_template('contact.html')

if __name__ == '__main__' :
    app.run(debug=True)

