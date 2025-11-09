Inspiration
Many elderly residents in nursing homes experience chronic loneliness. They often reminisce about their younger days when life was full of social interaction, optimism, and hope. Liora was inspired by the idea that maybe technology can help people feel what it is constantly removing the need for- a little conversation that makes someone feel heard. So, we thought of Liora a personalized AI companion that provides emotional support, and cognitive engagement to seniors who may feel isolated.

What it does
Liora is an AI-powered companion platform designed for elderly users. --> It allows seniors to: 1) Chat with customizable AI companions (friendly grandchild, caring neighbor, supportive family member) as well create a new 'loved one' as a new agent in the chatbot they can converse in. 2) Track and visualize their emotional well-being through sentiment analysis. 3) Engage in simple, stimulating games like Wordle to keep the mind active. -->For nurses or caregivers, Liora provides a dashboard to: 1) View patient-specific mood trends thereby providing regular insights into a person's emotional wellbeing. 2) Monitor emotional health over time in form of graphs.

How we built it
Frontend: Streamlit for a clean, interactive interface. AI Chatbot: Google Gemini 2.5 for conversational agents with customizable personas. Sentiment Analysis: pysentimiento to track emotional tone of user messages. Data Storage: CSV-based persistence for users, chat history, and mental health analysis. Python: to create Wordle-style brain games to boost cognitive activity as well for the overall workflow.

Challenges we ran into
1) Defining the idea of a minimalist and intuitive interface that is simple and accessible for elderly users. 2) Managing multiple AI personas and preserving chat history across sessions. 3) Combining mental health sentiment analysis with an enjoyable user experience. 4) Working around basic Streamlit workflow implementations. 5) Refining the codebase to give smoother transitions between pages.

Accomplishments that we're proud of
1) As beginners we are proud to have thought of an idea in which we can use technology to create a memorable experience for users. 2) Created a system where seniors can interact with AI companions that feel warm and personalized. 3) Built a nurse dashboard to monitor mood and engagement seamlessly. 4) Integrated an interactive game to stimulate cognitive function while keeping the platform enjoyable.

What we learned
1) Small interactions and personalized attention can have a significant impact on elderly users’ engagement. 2) Sentiment analysis combined with conversational AI can help detect subtle changes in mood over time and can give close-to-accurate numerical datapoints. 3) Streamlit allows rapid prototyping of complex multi-role applications.

What's next for Liora
1) Add voice-based chat for accessibility and natural interaction. 2) Expand the library of games and mental exercises. 3) Include predictive analytics for early detection of emotional decline. 4) Enhance AI personas with memory and context over long-term interactions.

Built With
api
gemini
pandas
pysentimiento
python
streamlit
