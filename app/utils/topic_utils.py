from typing import List, Tuple

def get_positive_negative_comments(topic_documents: List, sentiment_analyzer) -> Tuple[float, float, List, List]:
    sentiments = []
    positive_comments = [] 
    negative_comments = []
    
    for doc in topic_documents:
        sentiment = sentiment_analyzer(doc[:512])[0]
        sentiments.append(sentiment['label'])
        if sentiment['label'] == 'POSITIVE' and len(positive_comments) < 3:
            positive_comments.append(doc)
        elif sentiment['label'] == 'NEGATIVE' and len(negative_comments) < 3:
            negative_comments.append(doc)
            
        positive_percentage = sentiments.count('POSITIVE') / len(sentiments) * 100 if sentiments else 0
        negative_percentage = sentiments.count('NEGATIVE') / len(sentiments) * 100 if sentiments else 0
    return positive_percentage, negative_percentage, positive_comments, negative_comments