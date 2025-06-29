import { useState } from 'react';

function CustomSearch({ onCustomSearch, customSearchResult }) {
    const [keyword, setKeyword] = useState('');

    const handleSubmit = (e) => {
        e.preventDefault(); 
        if (keyword.trim()) {
            onCustomSearch(keyword.trim());
        }
    };

    const isResultVisible = customSearchResult.text !== '';

    return (
        <div className="custom-search">
            <h2>Search by Keyword</h2>
            <form onSubmit={handleSubmit}>
                <input
                    type="text"
                    className="custom-input"
                    placeholder="E.g., 'staff service', 'parking', 'food'"
                    value={keyword}
                    onChange={(e) => setKeyword(e.target.value)}
                />
                <button type="submit" className="custom-btn">
                    Get Details
                </button>
            </form>

            <div className={`custom-result ${customSearchResult.sentiment} ${isResultVisible ? 'visible' : ''}`}>
                {customSearchResult.text}
            </div>
        </div>
    );
}

export default CustomSearch;