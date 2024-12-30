# 🍎 Ingredient Insight: Your Nutrition Guide  

### Overview  
**Ingredient Insight** is an intelligent application designed to evaluate product ingredients and provide actionable health and nutrition insights. This app simplifies ingredient information, ensures dietary compatibility, and suggests healthier options to help users make informed decisions.  

---

### Features  
- **Ingredient Analysis**: Breaks down ingredient lists into simple, easy-to-understand explanations.  
- **Dietary Compatibility Check**: Evaluates products for vegan, halal, kosher, and other major dietary restrictions.  
- **Additive and Preservative Detection**: Identifies artificial additives and questionable ingredients.  
- **Nutritional Rating**: Rates the product's nutritional value on a scale of 1 to 5.  
- **Health Implications**: Highlights potential health concerns.  
- **Healthier Alternatives**: Suggests evidence-based alternatives or modifications.  
- **Search-Driven Insights**: Utilizes Tavily Search API for accurate and updated context.  

---

### Technology Stack  
- **Phidata Agentic Framework**: For building and managing the application's intelligent agents.  
- **Tavily Search API**: Provides real-time search capabilities for ingredient information and dietary guidelines.  
- **Large Language Models (LLM)**: Used for advanced ingredient analysis and natural language explanations.  
- **Streamlit**: Powers the user-friendly web interface.

---

### How It Works  
1. **Input**: Upload an image of the ingredient label or manually input the list.  
2. **Analysis**: The app evaluates the ingredients, checks dietary restrictions, and flags issues.  
3. **Rating**: Assigns a nutritional score (1 to 5) and highlights health implications.  
4. **Suggestions**: Provides healthier alternatives and actionable recommendations.  
5. **Results**: Outputs insights in Markdown format for easy sharing or review.  

---

### How to Run  
1. Clone the repository:   
   
2. Install dependencies:
    ```
    pip install -r requirements.txt 
     ```

3. Add API Keys in .env 
    ```
    GOOGLE_API_KEY=
    TAVILY_API_KEY=
    ```
4. Run the application
    ```
    streamlit run app.py
    ```