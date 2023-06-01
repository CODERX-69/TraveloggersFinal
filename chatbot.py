chatbot_dictionary = {
    "what is your name": "I am the ChatBot. Nice to meet you!",
    "how are you": "I'm doing well, thank you. How about you",
    "what can you do": "I can help you with various tasks such as answering questions, providing information, and assisting with basic tasks.",
    "how does the weekend planner work": "The weekend planner suggests travel destinations based on your location. It takes into account your proximity and recommends exciting places to visit for the upcoming weekend.",
    "can i create a blog on this platform": "Yes, you can create a blog if you are a registered user. Simply navigate to the 'Create Blog' section and follow the prompts.",
    "how can i filter blogs by categories": "To filter blogs by categories, use the category filters available in the sidebar or dropdown menu. Select your desired category to view blogs specific to that category.",
    "how can i delete a blog i created": "As a blog creator, you can delete your own blogs by navigating to the 'Manage Blogs' section and selecting the option to delete the specific blog you wish to remove.",
    "can i edit a blog after publishing it": "Yes, you can edit your published blogs. Simply go to the 'Manage Blogs' section, locate the blog you want to edit, and choose the 'Edit' option to make changes.",
    "how are blog recommendations personalized": "Blog recommendations are personalized based on your browsing history and interests. The platform analyzes your interactions and suggests relevant blogs that align with your preferences.",
    "how does the profanity check work": "The profanity check analyzes the content of blog posts and filters out any inappropriate or offensive language. It ensures that the platform maintains a respectful and positive environment.",
    "what happens if an image fails the originality check": "If an image fails the originality check, it indicates that the image may be plagiarized or infringing on copyright. In such cases, the user will be prompted to provide an original image.",
    "how can i see the analytics for my blogs": "As a blog creator, you can access the analytics page, which displays important metrics such as like and comment counts for each of your blogs. Simply go to the 'Analytics' section to view these insights.",
}


def get_reply(message):
    return chatbot_dictionary.get(message.lower(), "I don't understand you, please try again")


if __name__ == '__main__':
    import nltk
    nltk.download('stopwords')