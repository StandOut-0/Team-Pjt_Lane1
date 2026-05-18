import requests
from bs4 import BeautifulSoup
import json

url = "https://www.pse.com/ko/pages/electric-cars/electric-vehicles-faq"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    faq_data = []
    
    # Extract titles
    title_divs = soup.find_all('div', class_='title-collapse')
    
    # Try different selectors for answers
    answer_divs = soup.find_all('div', class_='panel-collapse collapse in')
    if not answer_divs:
        answer_divs = soup.find_all('div', class_='panel-collapse')
    if not answer_divs:
        answer_divs = soup.find_all('div', class_='collapse-content')
    
    print(f"Found {len(title_divs)} titles and {len(answer_divs)} answers")
    
    # If still no answers, try to find them by looking for panel-body
    if not answer_divs:
        answer_divs = soup.find_all('div', class_='panel-body')
    
    print(f"After trying different selectors: {len(answer_divs)} potential answer containers")
    
    for i, title_div in enumerate(title_divs):
        # Extract title
        title_p = title_div.find('p')
        title = title_p.get_text(strip=True) if title_p else f"Title {i+1}"
        
        # Try to find corresponding answer
        answer = "Answer not found"
        
        # Method 1: Look for data-target in title and find matching id
        if title_p and title_p.get('data-target'):
            target_id = title_p.get('data-target').replace('#', '')
            answer_div = soup.find('div', id=target_id)
            if answer_div:
                answer_body = answer_div.find('div', class_='panel-body')
                if answer_body:
                    answer = answer_body.get_text(strip=True)
        
        # Method 2: If method 1 failed, try to find answer by index
        if answer == "Answer not found" and i < len(answer_divs):
            answer_body = answer_divs[i].find('div', class_='panel-body')
            if answer_body:
                answer = answer_body.get_text(strip=True)
            else:
                answer = answer_divs[i].get_text(strip=True)
        
        faq_item = {
            'id': i + 1,
            'title': title,
            'answer': answer
        }
        
        faq_data.append(faq_item)
        print(f"{i+1}. {title[:50]}...")
    
    # Save to JSON
    with open('faq_data.json', 'w', encoding='utf-8') as f:
        json.dump(faq_data, f, ensure_ascii=False, indent=2)
    
    print(f"\nSuccessfully saved {len(faq_data)} FAQ items to faq_data.json")
    
except requests.exceptions.RequestException as e:
    print(f"Error fetching the URL: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
