import React, { useState } from 'react';

const CustomSearch = ({ onCustomSearch, customSearchResult }) => {
    const [customTopic, setCustomTopic] = useState('');

    const handleCustomSearchClick = () => {
        if (!customTopic.trim()) {
            alert('Please enter a custom topic');
            return;
        }
        onCustomSearch(customTopic);
    };

    const handleKeyPress = (e) => {
        if (e.key === 'Enter') {
            handleCustomSearchClick();
        }
    };

    const getResultClass = (sentiment) => {
        if (sentiment === 'positive') return 'positive';
        if (sentiment === 'negative') return 'negative';
        if (sentiment === 'mixed') return 'mixed';
        return '';
    };

    return (
        <div className="custom-search">
            <h2>💭 Custom Topic Search</h2>
            <input
                type="text"
                className="custom-input"
                placeholder="Ask about specific aspects (e.g., 'food quality', 'parking', 'best time to visit')"
                value={customTopic}
                onChange={(e) => setCustomTopic(e.target.value)}
                onKeyPress={handleKeyPress}
            />
            <button className="custom-btn" onClick={handleCustomSearchClick}>
                Search Reviews
            </button>
            <div
                className={`custom-result ${customSearchResult.text ? 'visible' : ''} ${getResultClass(customSearchResult.sentiment)}`}
                id="custom-result"
            >
                {customSearchResult.text || "Enter a custom topic to get tailored insights from visitor reviews."}
            </div>
        </div>
    );
};

export default CustomSearch;