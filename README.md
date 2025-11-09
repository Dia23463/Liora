##Inspiration
Many elderly residents in nursing homes experience chronic loneliness. They often reminisce about their younger days when life was full of social interaction, optimism, and hope. Liora was inspired by the idea that maybe technology can help people feel what it is constantly removing the need for- a little conversation that makes someone feel heard. So, we thought of Liora a personalized AI companion that provides emotional support, and cognitive engagement to seniors who may feel isolated.<br>

##What it does:<br>
Liora is an AI-powered companion platform designed for elderly users.<br> --> It allows seniors to:<br> 1) Chat with customizable AI companions (friendly grandchild, caring neighbor, supportive family member) as well create a new 'loved one' as a new agent in the chatbot they can converse in.<br> 2) Track and visualize their emotional well-being through sentiment analysis.<br> 3) Engage in simple, stimulating games like Wordle to keep the mind active.<br> -->For nurses or caregivers, Liora provides a dashboard to:<br> 1) View patient-specific mood trends thereby providing regular insights into a person's emotional wellbeing.<br> 2) Monitor emotional health over time in form of graphs.<br>

##How we built it:<br>
Frontend: Streamlit for a clean, interactive interface.<br> AI Chatbot: Google Gemini 2.5 for conversational agents with customizable personas.<br> Sentiment Analysis: pysentimiento to track emotional tone of user messages.<br> Data Storage: CSV-based persistence for users, chat history, and mental health analysis.<br> Python: to create Wordle-style brain games to boost cognitive activity as well for the overall workflow.<br>

##Challenges we ran into:<br>
1) Defining the idea of a minimalist and intuitive interface that is simple and accessible for elderly users.<br> 2) Managing multiple AI personas and preserving chat history across sessions.<br> 3) Combining mental health sentiment analysis with an enjoyable user experience.<br> 4) Working around basic Streamlit workflow implementations.<br> 5) Refining the codebase to give smoother transitions between pages.<br>

##Accomplishments that we're proud of:<br>
1) As beginners we are proud to have thought of an idea in which we can use technology to create a memorable experience for users.<br> 2) Created a system where seniors can interact with AI companions that feel warm and personalized.<br> 3) Built a nurse dashboard to monitor mood and engagement seamlessly.<br> 4) Integrated an interactive game to stimulate cognitive function while keeping the platform enjoyable.<br>

##What we learned:<br>
1) Small interactions and personalized attention can have a significant impact on elderly users’ engagement.<br> 2) Sentiment analysis combined with conversational AI can help detect subtle changes in mood over time and can give close-to-accurate numerical datapoints.<br> 3) Streamlit allows rapid prototyping of complex multi-role applications.<br>

##What's next for Liora:<br>
1) Add voice-based chat for accessibility and natural interaction.<br> 2) Expand the library of games and mental exercises.<br> 3) Include predictive analytics for early detection of emotional decline.<br> 4) Enhance AI personas with memory and context over long-term interactions.<br>

##Built With:
Gemini API, pandas, pysentimiento, python, streamlit
