import os
import json

class ReviewSearchEngine:
    def __init__(self, dataset_dir, image_map_file=None):
        self.dataset_dir = dataset_dir
        self.image_map = self._load_image_map(image_map_file) if image_map_file else {}
        self.indexed_reviews = self._index_stories()

    def _load_image_map(self, image_map_file):
        with open(image_map_file, 'r') as f:
            return json.load(f)

    def _index_stories(self):
        reviews = []
        for file in os.listdir(self.dataset_dir):
            if file.endswith('.txt'):
                with open(os.path.join(self.dataset_dir, file), 'r', encoding='utf-8') as f:
                    title = file.replace('.txt', '').replace('_', ' ')
                    content = f.read()
                    
                    image_url = self.image_map.get(file.replace('.txt', ''), 
                        'https://upload.wikimedia.org/wikipedia/commons/a/a3/Image-not-found.png')
                    reviews.append({
                        'title': title,
                        'content': content,
                        'image': image_url
                    })
        print(f"Indexed {len(reviews)} reviews.")
        return reviews

    def search(self, query):
        query = query.lower()
        
        # Boolean logic: Handle AND, OR, NOT
        if " and " in query:
            terms = query.split(" and ")
            results = self._handle_and(terms)
        elif " or " in query:
            terms = query.split(" or ")
            results = self._handle_or(terms)
        elif " not " in query:
            terms = query.split(" not ")
            results = self._handle_not(terms)
        else:
            # Simple search without boolean operators
            results = self._simple_search(query)
        
        print(f"Found {len(results)} results for query '{query}'.")
        return results

    def _simple_search(self, query):
        results = []
        for review in self.indexed_reviews:
            if query in review['title'].lower() or query in review['content'].lower():
                results.append(review)
        return results

    def _handle_and(self, terms):
        term1, term2 = terms[0].strip(), terms[1].strip()
        results = []
        for review in self.indexed_reviews:
            if (term1 in review['title'].lower() or term1 in review['content'].lower()) and \
               (term2 in review['title'].lower() or term2 in review['content'].lower()):
                results.append(review)
        return results

    def _handle_or(self, terms):
        term1, term2 = terms[0].strip(), terms[1].strip()
        results = []
        for review in self.indexed_reviews:
            if term1 in review['title'].lower() or term1 in review['content'].lower() or \
               term2 in review['title'].lower() or term2 in review['content'].lower():
                results.append(review)
        return results

    def _handle_not(self, terms):
        term1, term2 = terms[0].strip(), terms[1].strip()
        results = []
        for review in self.indexed_reviews:
            if (term1 in review['title'].lower() or term1 in review['content'].lower()) and \
               term2 not in review['title'].lower() and term2 not in review['content'].lower():
                results.append(review)
        return results