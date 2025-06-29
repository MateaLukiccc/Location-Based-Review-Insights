import { useState } from 'react';

const SearchSection = ({ onSearch }) => {
    const [siteName, setSiteName] = useState('');

    const handleSearchClick = () => {
        if (!siteName.trim()) {
            alert('Please enter a tourist site name');
            return;
        }
        onSearch(siteName);
    };

    const handleKeyPress = (e) => {
        if (e.key === 'Enter') {
            handleSearchClick();
        }
    };

    return (
        <div className="search-section">
            <h2>🔍 Search Tourist Site</h2>
            <input
                type="text"
                className="search-input"
                placeholder="Enter tourist site name (e.g., Eiffel Tower, Machu Picchu)"
                value={siteName}
                onChange={(e) => setSiteName(e.target.value)}
                onKeyPress={handleKeyPress}
            />
            <button className="search-btn" onClick={handleSearchClick}>
                Analyze Site
            </button>
        </div>
    );
};

export default SearchSection;