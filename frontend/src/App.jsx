import React, { useState, useEffect, useCallback } from 'react';
import Header from './components/Header.jsx';
import SearchSection from './components/SearchSection.jsx';
import SummaryCards from './components/SummaryCards.jsx';
import TopicsSection from './components/TopicsSection.jsx';
import CustomSearch from './components/CustomSearch.jsx';
import TopicModal from './components/TopicModal.jsx';
import './styles/App.css'; 

const API_BASE_URL = 'http://localhost:8000';

const generateSentimentData = (topic) => {
    const sentimentProfiles = {
        'Accessibility': { positive: 65, negative: 35 },
        'Crowd Levels': { positive: 35, negative: 65 },
        'Photography': { positive: 85, negative: 15 },
        'Facilities': { positive: 70, negative: 30 },
        'Food Quality': { positive: 60, negative: 40 },
        'Parking': { positive: 40, negative: 60 },
        'Best Time': { positive: 75, negative: 25 },
        'Guided Tours': { positive: 80, negative: 20 },
        'Safety': { positive: 85, negative: 15 },
        'Value for Money': { positive: 55, negative: 45 },
        'Cleanliness': { positive: 70, negative: 30 },
        'Staff Service': { positive: 75, negative: 25 },
        'Architecture': { positive: 90, negative: 10 },
        'History': { positive: 85, negative: 15 },
        'Views': { positive: 90, negative: 10 },
        'Amenities': { positive: 65, negative: 35 }
    };
    
    return sentimentProfiles[topic] || { positive: 70, negative: 30 };
};

const generateComments = (topic) => {
    const commentTemplates = {
        'Accessibility': {
            positive: [
                "Wheelchair accessible throughout with ramps and elevators. Staff very helpful for visitors with mobility needs.",
                "Great accessibility features including audio guides and braille information. Well-designed for all visitors.",
                "Impressed by the thoughtful accessibility design. Wide pathways and accessible restrooms available."
            ],
            negative: [
                "Limited wheelchair access to upper levels. Some areas are challenging for visitors with mobility issues.",
                "Accessibility could be improved - steep paths and stairs without alternatives in some sections.",
                "Not very accessible for elderly visitors or those with walking difficulties. Better signage needed."
            ]
        },
        'Crowd Levels': {
            positive: [
                "Visited early morning and it was peaceful with manageable crowds. Great experience!",
                "Off-season visit was perfect - not crowded at all. Could really enjoy the atmosphere.",
                "Despite being popular, crowd management was excellent. Never felt overwhelmed."
            ],
            negative: [
                "Extremely crowded during peak hours. Hard to take photos or enjoy the experience properly.",
                "Way too many tourists! Impossible to appreciate the site with such massive crowds.",
                "Overcrowded to the point of being unsafe. Long queues everywhere and pushing crowds."
            ]
        },
        'Photography': {
            positive: [
                "Absolutely stunning photo opportunities from every angle! Professional photographers' dream location.",
                "Perfect lighting conditions and incredible backdrops. Got some of my best travel photos here.",
                "Amazing photogenic spots with great viewing platforms. Photography enthusiasts will love it!"
            ],
            negative: [
                "Photography restrictions in many areas. Limited spots where you can actually take good photos.",
                "Lighting is poor in the main areas. Photos didn't turn out as expected unfortunately.",
                "Too crowded to get good shots. People everywhere in the frame ruins the photos."
            ]
        },
        'Facilities': {
            positive: [
                "Clean restrooms, good cafeteria, and helpful information center. All facilities well-maintained.",
                "Excellent visitor facilities including gift shop, restaurant, and clean washrooms. Very convenient.",
                "Modern facilities with good accessibility. Information kiosks and maps very helpful for navigation."
            ],
            negative: [
                "Limited restroom facilities for such a popular attraction. Long queues and cleanliness issues.",
                "Facilities are outdated and poorly maintained. Gift shop overpriced and limited food options.",
                "Inadequate facilities for the number of visitors. Need more seating areas and better maintenance."
            ]
        },
    };
    
    const defaultComments = {
        positive: [
            "Really enjoyed this aspect of the visit. Exceeded my expectations and would recommend to others.",
            "Outstanding quality and service. This was definitely a highlight of our trip to this location.",
            "Impressive and well-managed. Clear that a lot of thought and effort goes into this area."
        ],
        negative: [
            "This area needs improvement. Several issues that detracted from the overall experience.",
            "Disappointing compared to expectations. Hope management addresses these concerns soon.",
            "Could be much better with some attention and investment. Currently below average standards."
        ]
    };
    
    const comments = commentTemplates[topic] || defaultComments;
    
    return {
        positive: comments.positive.map((text, index) => ({
            text,
            rating: 4 + Math.floor(Math.random() * 2), 
            author: `Traveler${index + 1}`
        })),
        negative: comments.negative.map((text, index) => ({
            text,
            rating: 1 + Math.floor(Math.random() * 2), 
            author: `Visitor${index + 1}`
        }))
    };
};

const topicSets = [
    ['Accessibility', 'Crowd Levels', 'Photography', 'Facilities'],
    ['Food Quality', 'Parking', 'Best Time', 'Guided Tours'],
    ['Safety', 'Value for Money', 'Cleanliness', 'Staff Service'],
    ['Architecture', 'History', 'Views', 'Amenities']
];


function App() {
    const [positiveSummary, setPositiveSummary] = useState('Loading positive summary...');
    const [negativeSummary, setNegativeSummary] = useState('Loading negative summary...');
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
                console.log(parsedAnalyzeData)
                setSummariesVisible(true);
                setTopicsVisible(true);
            } catch (error) {
                console.error("Error fetching summaries:", error);
                setPositiveSummary("Failed to load positive summary. Please check backend connection.");
                setNegativeSummary("Failed to load negative summary. Please check backend connection.");
                setAllTopicAnalysis([]); 
                setSummariesVisible(true); 
            }
        }, []); 


    const openTopicModal = useCallback((topicId) => {
        const topicData = allTopicAnalysis.find(topic => topic.topic_id === topicId);

        if (topicData) {
            const formattedComments = {
                positive: topicData.positive_samples.map(text => ({
                    text: text,
                    rating: 5, 
                    author: "AI Analysis" 
                })),
                negative: topicData.negative_samples.map(text => ({
                    text: text,
                    rating: 1, 
                    author: "AI Analysis"
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

            const critiqueText = await response.json();

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