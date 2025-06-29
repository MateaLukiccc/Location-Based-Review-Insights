import { useEffect } from 'react';
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
    const positivePercent = sentimentData.positive || 0;
    const negativePercent = sentimentData.negative || 0;

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
                                style={{ width: `${positivePercent}%` }}
                            >
                                {positivePercent.toFixed(0)}%
                            </div>
                        </div>
                        <div className="sentiment-bar">
                            <div
                                className="sentiment-fill negative-fill"
                                style={{ width: `${negativePercent}%` }}
                            >
                                {negativePercent.toFixed(0)}%
                            </div>
                        </div>
                    </div>
                    <div className="sentiment-stats">
                        <span style={{ color: '#059669' }}>✅ Positive: <span id="positivePercent">{positivePercent.toFixed(0)}%</span></span>
                        <span style={{ color: '#dc2626' }}>❌ Negative: <span id="negativePercent">{negativePercent.toFixed(0)}%</span></span>
                    </div>
                </div>

                <div className="comments-section">
                    <h4 className="comments-header positive">
                        👍 Top Positive Comments
                    </h4>
                    <div id="positiveComments">
                        {comments.positive && comments.positive.length > 0 ? (
                            comments.positive.map((comment, index) => (
                                <CommentCard key={index} comment={comment} type="positive" />
                            ))
                        ) : (
                            <p style={{ color: '#6b7280' }}>No positive comments available for this topic.</p>
                        )}
                    </div>
                </div>

                <div className="comments-section">
                    <h4 className="comments-header negative">
                        👎 Top Negative Comments
                    </h4>
                    <div id="negativeComments">
                        {comments.negative && comments.negative.length > 0 ? (
                            comments.negative.map((comment, index) => (
                                <CommentCard key={index} comment={comment} type="negative" />
                            ))
                        ) : (
                            <p style={{ color: '#6b7280' }}>No negative comments available for this topic.</p>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default TopicModal;