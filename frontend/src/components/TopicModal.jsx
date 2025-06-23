import React, { useEffect } from 'react';
import CommentCard from './CommentCard';  

const TopicModal = ({ topicName, sentimentData, comments, isOpen, onClose }) => {
    useEffect(() => {
        if (isOpen) {
            document.body.style.overflow = 'hidden';
        } else {
            document.body.style.overflow = 'auto';
        }
        return () => {
            document.body.style.overflow = 'auto';  
        };
    }, [isOpen]);
     
    useEffect(() => {
        const handleKeyDown = (e) => {
            if (e.key === 'Escape') {
                onClose();
            }
        };
        document.addEventListener('keydown', handleKeyDown);
        return () => {
            document.removeEventListener('keydown', handleKeyDown);
        };
    }, [onClose]);

    if (!isOpen) return null;

    return (
        <div className={`modal-overlay ${isOpen ? 'visible' : ''}`} onClick={onClose}>
            <div className="modal-content" onClick={(e) => e.stopPropagation()}>
                <div className="modal-header">
                    <h3 className="modal-title">
                        <span>📊</span>
                        <span id="topicName">{topicName} Analysis</span>
                    </h3>
                    <button className="close-btn" onClick={onClose}>&times;</button>
                </div>

                <div className="sentiment-section">
                    <h4 className="sentiment-header">
                        📈 Sentiment Analysis
                    </h4>
                    <div className="sentiment-bars">
                        <div className="sentiment-bar">
                            <div
                                className="sentiment-fill positive-fill"
                                style={{ width: `${sentimentData.positive}%` }}
                            >
                                {sentimentData.positive}%
                            </div>
                        </div>
                        <div className="sentiment-bar">
                            <div
                                className="sentiment-fill negative-fill"
                                style={{ width: `${sentimentData.negative}%` }}
                            >
                                {sentimentData.negative}%
                            </div>
                        </div>
                    </div>
                    <div className="sentiment-stats">
                        <span style={{ color: '#059669' }}>✅ Positive: <span id="positivePercent">{sentimentData.positive}%</span></span>
                        <span style={{ color: '#dc2626' }}>❌ Negative: <span id="negativePercent">{sentimentData.negative}%</span></span>
                    </div>
                </div>

                <div className="comments-section">
                    <h4 className="comments-header positive">
                        👍 Top Positive Comments
                    </h4>
                    <div id="positiveComments">
                        {comments.positive.map((comment, index) => (
                            <CommentCard key={index} comment={comment} type="positive" />
                        ))}
                    </div>
                </div>

                <div className="comments-section">
                    <h4 className="comments-header negative">
                        👎 Top Negative Comments
                    </h4>
                    <div id="negativeComments">
                        {comments.negative.map((comment, index) => (
                            <CommentCard key={index} comment={comment} type="negative" />
                        ))}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default TopicModal;