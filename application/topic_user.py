from application.models import User, Following, Topics

def topic_user(user_id):
    tags = list( User.objects.aggregate(*[
            {
                '$lookup': {
                    'from': 'following', 
                    'localField': 'user_id', 
                    'foreignField': 'user_id', 
                    'as': 'u1'
                }
            }, {
                '$unwind': {
                    'path': '$u1', 
                    'includeArrayIndex': 'u1_id', 
                    'preserveNullAndEmptyArrays': False
                }
            }, {
                '$lookup': {
                    'from': 'articles', 
                    'localField': 'u1.topic_id', 
                    'foreignField': 'topic_via_channel', 
                    'as': 'u2'
                }
            }, {
                '$unwind': {
                    'path': '$u2', 
                    'preserveNullAndEmptyArrays': False
                }
            }, {
                '$match': {
                    'user_id': user_id
                }
            }, {
                '$sort': {
                    'published_date': 1
                }
            }
        ]))
    return tags

def get_other_topic(user_id):
    subscribed_topics = list(Following.objects(user_id=user_id).fields(topic_id=1,id=0))
    # all_topics = list(Topics.objects.all().fields(topic_id=1,id=0))
    user_topics = []
    for topic in subscribed_topics:
        user_topics.append(topic['topic_id'])
    topics = list(Topics.objects(topic_id__nin=user_topics).fields(topic_id=1,name=1))
    return topics


