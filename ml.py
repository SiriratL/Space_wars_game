import sklearn
from sklearn.preprocessing import StandardScaler
import numpy as np
from high_scores import high_scores
from river import cluster
from river import naive_bayes
import pickle

# Cluster Label Assignment
LABELS = {
    0: 'Hardcore Achiever',
    1: 'Hardcore Killer',
    2: 'Casual Achiever',
    3: 'Casual Killer',
}

def scale_data(data):
    # data > X = [[a0, a1, a2, a3, a4, a5, a6, a7, a8, a9, a10]]
    scaler = StandardScaler()
    X_scale = scaler.fit_transform(np.array(data).reshape(-1, 1))
    X_scale = {i: value[0] for i, value in enumerate(X_scale)}
    return(X_scale)

def write_model(model):
    # Save the clustering model
    #print('model=',model)
    with open(f'./model/{model}_model.pkl', 'wb') as f:
        pickle.dump(model, f)

def load_model(path_to_filename):
    # Load the clustering model
    with open(path_to_filename, 'rb') as f:
        model = pickle.load(f)
    return model

#def train_model(data,streamkmeans,classifier): # expecting data = list of dict
#    data = scale_data(data)
#    data = [dict(data)]
#    #print('data=',data)
#    # Continue training the clustering model
#    for x in data:
#        streamkmeans = streamkmeans.learn_one(x)
#    # Continue training the classification model
#    for x in data:
#        cluster_id = streamkmeans.predict_one(x)
#        label = LABELS[cluster_id]
#        classifier = classifier.learn_one(x, label)
#    return streamkmeans, classifier

def train_model(streamkmeans,classifier,timestamp):
    data_all = high_scores.check_data_after_timestamp(timestamp)
    if data_all == []:
        pass
    else:
        for data in data_all:

            keys_to_extract = ['a10', 'a2', 'a3', 'a4', 'a5', 'a6', 'a7', 'a8', 'a9']
            extracted_data = {key: data[key] for key in keys_to_extract}
            

            streamkmeans = streamkmeans.learn_one(extracted_data)
            # Continue training the classification model
            cluster_id = streamkmeans.predict_one(extracted_data)
            label = LABELS[cluster_id]

            classifier = classifier.learn_one(extracted_data, label)
    return streamkmeans, classifier

def predict_gamer(new_data, classifier): #expecting new data = dict 
    #data = scale_data(new_data)
    data = new_data 
    try:
        #print('data',data)
        prediction = classifier.predict_one(data)
        #print("check1")
    except:
        #print("check2")
        prediction = "Beginner"
    return prediction
