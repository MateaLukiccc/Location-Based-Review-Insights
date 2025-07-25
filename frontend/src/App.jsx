import React, { useState, useEffect, useCallback } from 'react';
import Header from './components/Header';
import SearchSection from './components/SearchSection';
import SummaryCards from './components/SummaryCards';
import TopicsSection from './components/TopicsSection';
import CustomSearch from './components/CustomSearch';
import TopicModal from './components/TopicModal';
import './styles/App.css'; 

const API_BASE_URL = 'http://localhost:8003';

function App() {
    const [positiveSummary, setPositiveSummary] = useState('Search for a tourist site to see what visitors love about it!');
    const [negativeSummary, setNegativeSummary] = useState('Common concerns and issues mentioned by travelers will appear here.');
    const [summariesVisible, setSummariesVisible] = useState(false);
    const [topicsVisible, setTopicsVisible] = useState(false);
    const [allTopicAnalysis, setAllTopicAnalysis] = useState([]);
    const [modalTopicData, setModalTopicData] = useState(null);
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [customSearchResult, setCustomSearchResult] = useState({ text: '', sentiment: '' });

    const performSearch = useCallback(async (siteName) => {
        setSummariesVisible(false);
        setTopicsVisible(false);
        setPositiveSummary('Loading positive summary...');
        setNegativeSummary('Loading negative summary...');

        setAllTopicAnalysis([]);

        try {
            const goodSummaryResponse = await fetch(`${API_BASE_URL}/llm/good_summary`);
            if (!goodSummaryResponse.ok) {
                throw new Error(`HTTP error! status: ${goodSummaryResponse.status}`);
            }
            const goodSummaryData = await goodSummaryResponse.json();
            setPositiveSummary(goodSummaryData.summary || goodSummaryData); 
            const badSummaryResponse = await fetch(`${API_BASE_URL}/llm/bad_summary`);
            if (!badSummaryResponse.ok) {
                throw new Error(`HTTP error! status: ${badSummaryResponse.status}`);
            }
            const badSummaryData = await badSummaryResponse.json();
            setNegativeSummary(badSummaryData.summary || badSummaryData);
            const analyzeResponse = await fetch(`${API_BASE_URL}/topics/analyze`);
            if (!analyzeResponse.ok) {
                const errorText = await analyzeResponse.text();
                throw new Error(`HTTP error! status: ${analyzeResponse.status}, message: ${errorText}`);
            }
            const analyzeData = await analyzeResponse.json();
            const parsedAnalyzeData = analyzeData.map(topic => {
                let parsedName = topic.topic_name;
                try {
                    const nameObj = JSON.parse(topic.topic_name);
                    if (nameObj && typeof nameObj === 'object' && nameObj.name_of_topic) {
                        parsedName = nameObj.name_of_topic;
                    }
                } catch (e) {
                    console.warn("Could not parse topic_name as JSON, using raw string:", topic.topic_name);
                }
                return {
                    ...topic,
                    topic_name: parsedName
                };
            });
            setAllTopicAnalysis(parsedAnalyzeData);
            setSummariesVisible(true);
            setTopicsVisible(true);
        } catch (error) {
            console.error("Error fetching summaries:", error);
            setPositiveSummary("Failed to load positive summary. Please check backend connection.");
            setNegativeSummary("Failed to load negative summary. Please check backend connection.");
            setSummariesVisible(true); 
            setAllTopicAnalysis([]);
        }
    }, []);


    const openTopicModal = useCallback((topicId) => {
        const topicData = allTopicAnalysis.find(topic => topic.topic_id === topicId);

        if (topicData) {
            const formattedComments = {
                positive: topicData.positive_samples.map(text => ({
                    text: text,
                    rating: 5
                })),
                negative: topicData.negative_samples.map(text => ({
                    text: text,
                    rating: 1
                }))
            };

            setModalTopicData({
                topic_name: topicData.topic_name,
                sentiment_analysis: {
                    positive: parseFloat(topicData.sentiment_analysis.positive_percentage),
                    negative: parseFloat(topicData.sentiment_analysis.negative_percentage)
                },
                comments: formattedComments
            });
            setIsModalOpen(true);
        } else {
            console.error("Topic data not found for ID:", topicId);
        }
    }, [allTopicAnalysis]);

    const closeTopicModal = useCallback(() => {
        setIsModalOpen(false);
        setModalTopicData(null);
    }, []);

     const performCustomSearch = useCallback(async (keyword) => {
        setCustomSearchResult({ text: 'Searching...', sentiment: '' });

        try {
            const encodedKeyword = encodeURIComponent(keyword);
            const response = await fetch(`${API_BASE_URL}/llm/summary?keyword=${encodedKeyword}`);

            if (!response.ok) {
                const errorText = await response.text();
                throw new Error(`HTTP error! status: ${response.status}, message: ${errorText}`);
            }

            const data = await response.json();
            const critiqueText = data; 
            let sentimentType = 'mixed'; 
            if (critiqueText.toLowerCase().includes('positive') || critiqueText.toLowerCase().includes('good')) {
                sentimentType = 'positive';
            } else if (critiqueText.toLowerCase().includes('negative') || critiqueText.toLowerCase().includes('bad') || critiqueText.toLowerCase().includes('concerns')) {
                sentimentType = 'negative';
            } else if (critiqueText.toLowerCase().includes('no reviews')) {
                sentimentType = 'mixed';
            }  
            setCustomSearchResult({ text: critiqueText, sentiment: sentimentType });

        } catch (error) {
            console.error("Error fetching custom summary:", error);
            setCustomSearchResult({ text: `Error: ${error.message}. Could not fetch custom summary.`, sentiment: 'negative' });
        }
    }, []);


    return (
        <div className="container">
            <Header />

            <div className="main-content">
                <div className="left-panel">
                    <SearchSection onSearch={performSearch} />
                    <SummaryCards
                        positiveSummary={positiveSummary}
                        negativeSummary={negativeSummary}
                        isVisible={summariesVisible}
                    />
                </div>

                <div className="right-panel">
                    <TopicsSection
                        topics={allTopicAnalysis.map(topic => ({
                            id: topic.topic_id,
                            name: topic.topic_name 
                        }))}
                        onTopicClick={openTopicModal}
                        isVisible={topicsVisible}
                    />
                    <CustomSearch
                        onCustomSearch={performCustomSearch}
                        customSearchResult={customSearchResult}
                    />
                </div>
            </div>

            <TopicModal
                topicName={modalTopicData?.topic_name || ''}
                sentimentData={modalTopicData?.sentiment_analysis || { positive: 0, negative: 0 }}
                comments={modalTopicData?.comments || { positive: [], negative: [] }}
                isOpen={isModalOpen}
                onClose={closeTopicModal}
            />
        </div>
    );
}

export default App;