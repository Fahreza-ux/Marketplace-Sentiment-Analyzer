import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import re
from datetime import datetime

print("🛍️ AI ANALISIS SENTIMENT REVIEW PRODUK - MARKETPLACE")

class ProductSentimentAnalyzer:
    def __init__(self):
        # Expanded dictionary untuk Bahasa Indonesia
        self.positive_words = [
            'mantap', 'bagus', 'puas', 'recommended', 'worth it', 'terjangkau', 
            'jernih', 'smooth', 'elegan', 'juara', 'berkualitas', 'cepat', 
            'tahan lama', 'sangat baik', 'memuaskan', 'keren', 'oke', 'sukses',
            'hebat', 'luar biasa', 'top', 'profesional', 'excellent', 'sempurna'
        ]
        
        self.negative_words = [
            'jelek', 'buruk', 'kecewa', 'lag', 'boros', 'mahal', 'panas', 
            'mengecewakan', 'lemot', 'tidak worth', 'biasa saja', 'gagal',
            'rusak', 'cacat', 'pelan', 'error', 'masalah', 'komplain',
            'rugi', 'tidak puas', 'sebel', 'frustasi'
        ]
        
        self.feature_keywords = {
            'baterai': ['baterai', 'charge', 'tahan lama', 'boros', 'daya'],
            'kamera': ['kamera', 'foto', 'selfie', 'jernih', 'low light', 'gambar'],
            'performance': ['performance', 'cepat', 'lag', 'lemot', 'smooth', 'responsif'],
            'harga': ['harga', 'terjangkau', 'mahal', 'worth it', 'murah', 'harga'],
            'desain': ['desain', 'elegan', 'layar', 'bodi', 'tampilan', 'bentuk'],
            'layanan': ['pelayanan', 'servis', 'customer service', 'respons', 'bantuan']
        }
    
    def analyze_sentiment(self, review_text):
        """Analisis sentiment berdasarkan kata kunci Bahasa Indonesia"""
        if not review_text or pd.isna(review_text):
            return "Neutral", 0
            
        review_lower = str(review_text).lower()
        
        positive_score = sum(1 for word in self.positive_words if word in review_lower)
        negative_score = sum(1 for word in self.negative_words if word in review_lower)
        
        if positive_score > negative_score:
            return "Positive", positive_score - negative_score
        elif negative_score > positive_score:
            return "Negative", negative_score - positive_score
        else:
            return "Neutral", 0
    
    def extract_features(self, review_text):
        """Ekstrak fitur produk yang disebutkan dalam review"""
        if not review_text or pd.isna(review_text):
            return []
            
        review_lower = str(review_text).lower()
        features = []
        
        for feature, keywords in self.feature_keywords.items():
            if any(keyword in review_lower for keyword in keywords):
                features.append(feature)
        
        return features
    
    def analyze_reviews(self, reviews_data):
        """Analisis semua review"""
        df = pd.DataFrame(reviews_data)
        
        results = []
        for _, review in df.iterrows():
            sentiment, confidence = self.analyze_sentiment(review['review'])
            features = self.extract_features(review['review'])
            
            results.append({
                'produk': review['produk'],
                'review': review['review'],
                'rating': review['rating'],
                'sentiment': sentiment,
                'confidence': confidence,
                'features': features,
                'tanggal': review.get('tanggal', '2024-01-01')
            })
        
        return pd.DataFrame(results)

def generate_product_report(df_analysis, product_name):
    """Generate laporan untuk produk tertentu"""
    product_reviews = df_analysis[df_analysis['produk'] == product_name]
    
    if len(product_reviews) == 0:
        return f"❌ Tidak ada review untuk {product_name}"
    
    total_reviews = len(product_reviews)
    positive_reviews = len(product_reviews[product_reviews['sentiment'] == 'Positive'])
    negative_reviews = len(product_reviews[product_reviews['sentiment'] == 'Negative'])
    neutral_reviews = len(product_reviews[product_reviews['sentiment'] == 'Neutral'])
    
    # Analisis fitur
    all_features = []
    for features in product_reviews['features']:
        all_features.extend(features)
    
    feature_counts = Counter(all_features)
    
    # Rating analysis
    avg_rating = product_reviews['rating'].mean()
    
    # Build report
    report = []
    report.append(f"📊 **LAPORAN ANALISIS: {product_name.upper()}**")
    report.append("=" * 40)
    report.append(f"📈 Total Review: {total_reviews}")
    report.append(f"⭐ Rating Rata-rata: {avg_rating:.1f}/5")
    report.append(f"😊 Sentiment Positif: {positive_reviews} ({positive_reviews/total_reviews*100:.1f}%)")
    report.append(f"😐 Sentiment Netral: {neutral_reviews} ({neutral_reviews/total_reviews*100:.1f}%)")
    report.append(f"😞 Sentiment Negatif: {negative_reviews} ({negative_reviews/total_reviews*100:.1f}%)")
    
    if feature_counts:
        report.append("\n🔍 **FITUR YANG SERING DISEBUT:**")
        for feature, count in feature_counts.most_common(5):
            percentage = (count / total_reviews) * 100
            report.append(f"   • {feature.title()}: {count}x ({percentage:.1f}%)")
    
    return "\n".join(report)

def main():
    # Sample data - realistic marketplace reviews
    sample_data = [
        {"produk": "Xiaomi Redmi Note 12", "review": "HP ini mantap banget, kamera jernih dan baterai tahan lama", "rating": 5},
        {"produk": "Xiaomi Redmi Note 12", "review": "Cepat panas dan sering lag, tidak worth it", "rating": 2},
        {"produk": "Samsung Galaxy A54", "review": "Layar bagus tapi baterai boros banget", "rating": 3},
        {"produk": "Samsung Galaxy A54", "review": "Produk Samsung selalu berkualitas, recommended!", "rating": 5},
        {"produk": "iPhone 14", "review": "Harga mahal tapi performance worth it, iOS smooth", "rating": 4},
        {"produk": "Oppo Reno 8", "review": "Desain elegan dan kamera depan bagus untuk selfie", "rating": 4},
        {"produk": "Vivo V27", "review": "Kamera low light-nya juara, tapi speaker kurang bagus", "rating": 4},
    ]
    
    analyzer = ProductSentimentAnalyzer()
    
    print("🔍 Menganalisis review produk...")
    df_analysis = analyzer.analyze_reviews(sample_data)
    
    # Display results
    print("\n" + "="*60)
    print("📈 HASIL ANALISIS SENTIMENT REVIEW PRODUK")
    print("="*60)
    
    for product in df_analysis['produk'].unique():
        report = generate_product_report(df_analysis, product)
        print(report)
        print()
    
    # Detailed review analysis
    print("\n📝 **DETAIL REVIEW:**")
    print("="*60)
    for idx, row in df_analysis.iterrows():
        sentiment_icon = "😊" if row['sentiment'] == "Positive" else "😐" if row['sentiment'] == "Neutral" else "😞"
        print(f"{idx+1}. {row['produk']} {sentiment_icon}")
        print(f"   💬: '{row['review']}'")
        print(f"   ⭐ Rating: {row['rating']}/5 | Confidence: {row['confidence']}")
        print(f"   🔧 Fitur: {', '.join(row['features']) if row['features'] else 'Tidak spesifik'}")
        print()

if __name__ == "__main__":
    main()
