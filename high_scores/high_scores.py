import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
#from datetime import datetime

def connect_db(path):
    # Fetch the service account key JSON file contents
    cred = credentials.Certificate('./db_key/spacewars-49e35-firebase-adminsdk-rrf8b-24a9906067.json')
    try:
        # Initialize the app with a service account, granting admin privileges
        firebase_admin.initialize_app(cred, {
            'databaseURL': "https://spacewars-49e35-default-rtdb.asia-southeast1.firebasedatabase.app/"
        })
    except:
        pass
    ref = db.reference(f'/{path}')
    return ref

#def high_scores_ stores the 'latest' score of each username
#    score_ref = connect_db('score')
#    score_snapshot = score_ref.order_by_value().get()
#    sorted_scores = sorted(score_snapshot.items(), key=lambda x: x[1], reverse=True)
#    
#    top5_scores = sorted_scores[:5]  # Retrieve only the top 5 scores
#    
#    # get values from high score record
#    highscore_ref = connect_db('highscore')
#    highscore_snapshot = highscore_ref.order_by_value().get()
#    sorted_highscores = sorted(highscore_snapshot.items(), key=lambda x: x[1], reverse=True)
#    
#    for key, val in top5_scores:
#        for i, (k, v) in enumerate(sorted_highscores):
#            if val > v:
#                highscore_ref.child(k).delete()
#                highscore_ref.update({key: val})
#                sorted_highscores[i] = (key, val)
#                break


#    firebase_admin.delete_app(firebase_admin.get_app())

def top_5():
    ref = connect_db('score')
    snapshot = ref.order_by_value().limit_to_last(5).get()
    snapshot = sorted(snapshot.items(), key=lambda x: x[1], reverse=True)

    firebase_admin.delete_app(firebase_admin.get_app())

    return snapshot


#def update_score(dic): #dct = {username:score}
#    connect_db('/score').update(dic)
#
#    #update high score after updated the score
#    high_scores_update_db()
#
#    try:
#        firebase_admin.delete_app(firebase_admin.get_app())
#    except:
#        pass

#def high_scores_top_list():
#    ref = connect_db('highscore')
#    snapshot = ref.order_by_value().get()
#    sorted_snapshot = sorted(snapshot.items(), key=lambda x: x[1], reverse=True)
#
#    firebase_admin.delete_app(firebase_admin.get_app())
#    return(sorted_snapshot)

def publish_online_score(name,score):
	ref = connect_db('score')
	ref.update({name:score})
	firebase_admin.delete_app(firebase_admin.get_app())

def save_train_data(data,username):
    ref = connect_db("/user_stat")
    #posts_ref = ref.child(username)
    #posts_ref.push().set(data)
    ref.push().set(data)

def check_data_after_timestamp(timestamp):
    ref = connect_db("/user_stat")
    snapshot = ref.order_by_child('timestamp').start_at(timestamp).get()
    value=[]
    for _, val in snapshot.items():
        value.append(val)
    firebase_admin.delete_app(firebase_admin.get_app())
    return (value) #if emptry value == []