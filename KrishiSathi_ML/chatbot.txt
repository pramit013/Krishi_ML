const { MongoClient } = require('mongodb');
const axios = require('axios');

// MongoDB connection string (replace <password> and <dbName> with your credentials)
const uri = 'mongodb+srv://<username>:<password>@cluster0.mongodb.net/<dbName>?retryWrites=true&w=majority';
const client = new MongoClient(uri, { useNewUrlParser: true, useUnifiedTopology: true });

async function storeQueryAndResponse(question, response) {
    try {
        await client.connect();
        const database = client.db('chatHistory'); // Database name
        const collection = database.collection('queries'); // Collection name

        const doc = {
            question: question,
            response: response,
            date: new Date() // Store timestamp
        };

        await collection.insertOne(doc); // Insert query and response into the collection
    } finally {
        await client.close();
    }
}

// Function to handle ChatGPT API query
async function queryChatGPT(userQuestion) {
    const openaiApiKey = 'sk-4MFy5CecNyjA2qdh9lZmVrrPb0q1amnIPED0el5b-KT3BlbkFJgcB72y1gNP8E-JTQgpk4cH12hZGZMfZDqaVwNesKAA'; // Replace this with your actual OpenAI API key
    const chatgptResponse = await axios.post(
        'https://api.openai.com/v1/chat/completions',
        {
            model: "gpt-3.5-turbo",
            messages: [{ role: "user", content: userQuestion }],
        },
        {
            headers: {
                'Authorization': `Bearer ${openaiApiKey}`,
                'Content-Type': 'application/json'
            }
        }
    );

    return chatgptResponse.data.choices[0].message.content;
}

// Function to handle speech query from the user
async function handleSpeechQuery(userQuestion) {
    const response = await queryChatGPT(userQuestion); // Get the response from ChatGPT
    await storeQueryAndResponse(userQuestion, response); // Store both the question and response in MongoDB
    return response;
}

module.exports = { handleSpeechQuery };

// In your server file (e.g., server.js)
app.get('/api/qa-data', async (req, res) => {
    try {
        // Fetch data from MongoDB
        const qaCollection = db.collection('qa'); // Replace 'qa' with your collection name
        const qaData = await qaCollection.find({}).toArray();
        res.json(qaData);
    } catch (error) {
        res.status(500).send('Error fetching Q&A data');
    }
});