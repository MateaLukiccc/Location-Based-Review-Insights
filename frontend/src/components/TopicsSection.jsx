const TopicsSection = ({ topics, onTopicClick, isVisible }) => {
    return (
        <div className="topics-section">
            <h2>🎯 Popular Discussion Topics</h2>
            <div className={`topics-grid ${isVisible ? 'visible' : ''}`}>
                {}
                {topics.length > 0 ? (
                    topics.map((topic) => (
                        <div
                            key={topic.id} 
                            className="topic-card"
                            onClick={() => onTopicClick(topic.id)} 
                        >
                            {topic.name}
                        </div>
                    ))
                ) : (
                    <p style={{ color: '#1f2937', textAlign: 'center', gridColumn: '1 / -1' }}>
                        No topics found. Perform a search to analyze reviews.
                    </p>
                )}
            </div>
        </div>
    );
};

export default TopicsSection;