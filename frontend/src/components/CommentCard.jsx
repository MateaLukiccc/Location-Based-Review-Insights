const CommentCard = ({ comment, type }) => {
    const stars = '★'.repeat(comment.rating) + '☆'.repeat(5 - comment.rating);

    return (
        <div className={`comment-card ${type}`}>
            <div className="comment-text">{comment.text}</div>
            <div className="comment-meta">
                <span className="rating-stars">{stars}</span>
                <span>• {comment.author}</span>
            </div>
        </div>
    );
};

export default CommentCard;