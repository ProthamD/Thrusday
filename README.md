# Thursday - The Ultimate Discord SuperMod Bot 🚀

Welcome to **Thursday**, your all-in-one Discord moderation and interaction bot. Thursday is not just a bot; it's your virtual assistant, moderator, and conversational partner rolled into one. Designed to handle moderation tasks efficiently while engaging in meaningful conversations, Thursday ensures your server remains a safe and enjoyable space for everyone.

---

## ✨ Features

### **1. Smart Moderation**
- **Automatic Bad Word Detection**: Thursday uses advanced AI to detect and filter out inappropriate language, including slurs, hate speech, and severe profanity.
- **Timeout System**: Users who violate server rules are automatically timed out for 1 hour. Admins can also manually timeout users with a simple command.
- **Message Deletion**: Offensive messages are instantly deleted to maintain a clean and respectful environment.

### **2. Conversational AI**
- **Context-Aware Chat**: Thursday remembers the context of your conversations, making interactions feel natural and engaging.
- **Personalized Responses**: The bot addresses users by their names and tailors responses based on the conversation history.
- **AI-Powered Responses**: Powered by OpenRouter.ai, Thursday delivers intelligent and contextually relevant replies.

### **3. Image Generation**
- **AI-Generated Art**: Thursday can create stunning images using the Stable Horde API. Just provide a prompt, and the bot will generate a unique image for you.
- **Customizable Parameters**: Control image size, style, and other settings to get the perfect output.

### **4. Channel Management**
- **Bulk Channel Creation**: Admins can create multiple channels at once with AI-generated names, making server setup a breeze.
- **Permission Control**: Only users with the appropriate permissions can execute moderation and management commands.

### **5. User Data Management**
- **Persistent User Profiles**: Thursday stores user preferences and conversation history, ensuring a personalized experience for each user.
- **Data Security**: User data is saved locally in a JSON file, ensuring privacy and control.

---

## 🛠️ Commands

### **Moderation Commands**
- **`!timeout @user`**: Timeout a user for 1 hour. (Requires `Moderate Members` permission)
- **`!create_channels <number_of_channels>`**: Create multiple channels with AI-generated names. (Requires `Manage Channels` permission)

### **Image Generation**
- **`!img <prompt>`**: Generate an image based on the provided prompt using Stable Horde.

### **Conversation**
- Mention Thursday in your message, and it will respond intelligently based on the conversation context.

---

## 🚀 Setup Instructions

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-repo/thursday-bot.git
   cd thursday-bot
## *Install Dependencies:*

  bash
    Copy
  pip install -r requirements.txt
  Set Up Environment Variables:

Create a .env file in the root directory.

Add the following variables:

plaintext
Copy
TOKEN=your_discord_bot_token
OPENROUTER_API_KEY=your_openrouter_api_key
STABLE_HORDE_API_KEY=your_stable_horde_api_key
Run the Bot:

bash
Copy
python bot.py
# **⚙️ Configuration**
Customizing Bad Words
Edit the bad_words list in the code to add or remove words that Thursday should filter.

Adjusting Conversation History Length
Modify the MAX_HISTORY_LENGTH variable to control how many messages Thursday remembers for each user.

### **Changing AI Model**
Update the model parameter in the OpenRouter API request to use a different AI model.

### **🤝 Support and Contributions**
If you encounter any issues or have suggestions for improvements, feel free to open an issue or submit a pull request. Your feedback is invaluable in making Thursday even better!

### **⚠️ Disclaimer**
Thursday is designed to maintain a respectful and safe environment. However, no AI system is perfect. If you notice any issues with moderation or behavior, please report them immediately.

### **📜 License**
This project is licensed under the MIT License. See the LICENSE file for details.

Enjoy your time with Thursday – the smart, stylish, and super-efficient Discord SuperMod bot! 🚀

Copy

### How to Use:
1. Copy the entire content above.
2. Create a file named `README.md` in your project directory.
3. Paste the copied content into the `README.md` file.
4. Save the file.
