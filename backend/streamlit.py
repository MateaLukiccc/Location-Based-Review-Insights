import streamlit as st
import requests
import json

# --- Configuration ---
API_BASE_URL = "http://localhost:8000"  # Replace with your FastAPI server URL

# --- Helper Functions ---
def fetch_data(endpoint, method="GET", params=None, json_data=None):
    url = f"{API_BASE_URL}{endpoint}"
    try:
        if method == "GET":
            response = requests.get(url, params=params)
        elif method == "POST":
            response = requests.post(url, params=params, json=json_data)
        else:
            st.error(f"Unsupported HTTP method: {method}")
            return None

        response.raise_for_status()  # Raise an exception for bad status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to the API: {e}")
        return None
    except requests.exceptions.HTTPError as e:
        st.error(f"API Error: {e}")
        try:
            return response.json()  # Try to get error details from JSON
        except:
            return None
    except json.JSONDecodeError:
        st.error("Error decoding JSON response from the API.")
        return None

# --- Sidebar Navigation ---
st.sidebar.title("API Explorer")
selected_route = st.sidebar.radio("Select an API Endpoint",
                                  ["Topic Analysis", "LLM Operations", "ChromaDB Operations"])

# --- Main Area ---
st.title("Backend API Showcase")

if selected_route == "Topic Analysis":
    st.header("Topic Analysis (/topics)")
    if st.button("Analyze Reviews"):
        with st.spinner("Analyzing reviews..."):
            results = fetch_data("/topics/analyze", method="GET")
            if results:
                st.subheader("Topic Analysis Results")
                for topic in results:
                    st.markdown(f"**Topic ID:** {topic['topic_id']}")
                    st.markdown(f"**Topic Words:** {topic['topic_words']}")
                    st.subheader("Sentiment Analysis")
                    st.write(f"Positive: {topic['sentiment_analysis']['positive_percentage']}")
                    st.write(f"Negative: {topic['sentiment_analysis']['negative_percentage']}")
                    if topic['positive_samples']:
                        st.markdown("**Positive Samples:**")
                        for sample in topic['positive_samples']:
                            st.markdown(f"- *{sample}*")
                    if topic['negative_samples']:
                        st.markdown("**Negative Samples:**")
                        for sample in topic['negative_samples']:
                            st.markdown(f"- *{sample}*")
                    st.divider()
            else:
                st.info("No topic analysis results to display.")

elif selected_route == "LLM Operations":
    st.header("LLM Operations (/llm)")

    st.subheader("Get Summary (/summary)")
    keyword = st.text_input("Enter keyword for summary:")
    distance_bound = st.slider("Distance Bound for Summary", min_value=0.1, max_value=2.0, value=1.1, step=0.1)
    if st.button("Get Summary"):
        if keyword:
            with st.spinner("Fetching summary..."):
                params = {"keyword": keyword, "distance_bound": distance_bound}
                summary = fetch_data("/llm/summary", params=params)
                if summary:
                    st.subheader(f"Summary for '{keyword}' (Distance <= {distance_bound})")
                    st.write(summary)
                else:
                    st.info("No relevant reviews found for the given keyword.")
        else:
            st.warning("Please enter a keyword to get a summary.")

    st.subheader("Get Good Summary (/good_summary)")
    if st.button("Get Positive Summary"):
        with st.spinner("Fetching positive summary..."):
            good_summary = fetch_data("/llm/good_summary")
            if good_summary:
                st.subheader("Positive Review Summary")
                st.write(good_summary)
            else:
                st.info("Could not fetch positive review summary.")

    st.subheader("Get Bad Summary (/bad_summary)")
    if st.button("Get Negative Summary"):
        with st.spinner("Fetching negative summary..."):
            bad_summary = fetch_data("/llm/bad_summary")
            if bad_summary:
                st.subheader("Negative Review Summary")
                st.write(bad_summary)
            else:
                st.info("Could not fetch negative review summary.")

elif selected_route == "ChromaDB Operations":
    st.header("ChromaDB Operations (/chroma)")

    st.subheader("Get Document by Keyword (/documents/{keyword}/)")
    keyword_doc = st.text_input("Enter keyword to search for document:")
    limit_doc = st.slider("Limit for Document Search", min_value=1, max_value=10, value=1, step=1)
    if st.button("Search Document"):
        if keyword_doc:
            with st.spinner("Searching for document..."):
                results = fetch_data(f"/chroma/documents/{keyword_doc}/", params={"limit": limit_doc})
                if results:
                    st.subheader(f"Document for '{keyword_doc}'")
                    st.write(f"**ID:** {results['id']}")
                    st.write(f"**Text:** {results['text']}")
                    st.write(f"**Metadata:** {results['metadata']}")
                else:
                    st.info(f"No document found for keyword: '{keyword_doc}'.")
        else:
            st.warning("Please enter a keyword to search for a document.")

    st.subheader("Get Documents by Distance (/documents/distance/{keyword})")
    keyword_distance = st.text_input("Enter keyword for distance search:")
    distance_bound_distance = st.slider("Distance Bound", min_value=0.1, max_value=2.0, value=1.1, step=0.1, key="distance_slider")
    if st.button("Search by Distance"):
        if keyword_distance:
            with st.spinner("Searching by distance..."):
                results = fetch_data(f"/chroma/documents/distance/{keyword_distance}", params={"distance_bound": distance_bound_distance})
                if results and results.get("documents"):
                    st.subheader(f"Documents near '{keyword_distance}' (Distance <= {distance_bound_distance})")
                    for i, doc in enumerate(results["documents"]):
                        st.markdown(f"**Document {i+1}:** {doc}")
                        st.write(f"**Distance:** {results['distances'][i]}")
                        st.write(f"**ID:** {results['ids'][i]}")
                        if results.get("metadatas") and results["metadatas"][i]:
                            st.write(f"**Metadata:** {results['metadatas'][i]}")
                        st.divider()
                else:
                    st.info(f"No documents found within the distance bound for '{keyword_distance}'.")
        else:
            st.warning("Please enter a keyword for distance search.")

    st.subheader("Get Entry Count (/documents/count)")
    if st.button("Get Document Count"):
        with st.spinner("Fetching document count..."):
            count_result = fetch_data("/chroma/documents/count")
            if count_result and "count" in count_result:
                st.write(f"**Total Documents in ChromaDB:** {count_result['count']}")
            else:
                st.info("Could not fetch document count.")

    st.subheader("Fetch All Reviews (Internal Function - Not a direct API endpoint)")
    if st.button("Fetch All Reviews"):
        with st.spinner("Fetching all reviews..."):
            all_reviews = fetch_data("/chroma/documents") # Assuming you might have a /chroma/documents endpoint
            if all_reviews:
                st.write("All Reviews:")
                st.write(all_reviews)
            else:
                st.info("Could not fetch all reviews.")