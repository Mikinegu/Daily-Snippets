import random
import json
import time
from datetime import datetime, timedelta
from pathlib import Path
import logging

class SocialMediaAutomator:
    def __init__(self):
        self.content_templates = {
            'motivational': [
                "🚀 {quote} #motivation #success #inspiration",
                "💪 Remember: {quote} #mindset #growth #goals",
                "✨ Today's reminder: {quote} #positivity #life #motivation",
                "🌟 {quote} #inspiration #success #mindset",
                "🔥 {quote} #motivation #goals #success"
            ],
            'tech': [
                "💻 Tech tip: {tip} #programming #tech #coding",
                "🔧 Did you know? {tip} #technology #developer #coding",
                "⚡ Quick tech insight: {tip} #programming #tech #innovation",
                "🚀 {tip} #technology #coding #developer",
                "💡 Tech wisdom: {tip} #programming #innovation #tech"
            ],
            'business': [
                "💼 Business insight: {insight} #business #entrepreneur #success",
                "📈 {insight} #business #growth #entrepreneurship",
                "🎯 Key business lesson: {insight} #business #success #strategy",
                "💡 Business tip: {insight} #entrepreneur #business #growth",
                "🚀 {insight} #business #success #entrepreneurship"
            ],
            'lifestyle': [
                "🌿 {tip} #lifestyle #wellness #health",
                "✨ Life hack: {tip} #lifestyle #tips #life",
                "🌸 {tip} #lifestyle #wellness #mindfulness",
                "💫 Simple life tip: {tip} #lifestyle #health #wellness",
                "🌱 {tip} #lifestyle #mindfulness #wellness"
            ]
        }
        
        self.quotes = [
            "Success is not final, failure is not fatal: it is the courage to continue that counts.",
            "The only way to do great work is to love what you do.",
            "Believe you can and you're halfway there.",
            "The future belongs to those who believe in the beauty of their dreams.",
            "Don't watch the clock; do what it does. Keep going.",
            "The only limit to our realization of tomorrow is our doubts of today.",
            "Success usually comes to those who are too busy to be looking for it.",
            "The way to get started is to quit talking and begin doing.",
            "It always seems impossible until it's done.",
            "The best time to plant a tree was 20 years ago. The second best time is now."
        ]
        
        self.tech_tips = [
            "Use keyboard shortcuts to boost your productivity by 50%",
            "Regular code reviews improve code quality and team collaboration",
            "Documentation is as important as the code itself",
            "Test-driven development leads to better code design",
            "Version control is your best friend in software development",
            "Automation saves time and reduces human error",
            "Clean code is readable code",
            "Performance optimization should be measured, not guessed",
            "Security should be built-in, not bolted on",
            "Continuous learning is essential in tech"
        ]
        
        self.business_insights = [
            "Customer feedback is the most valuable data for business growth",
            "Focus on solving real problems, not just building features",
            "Consistency beats perfection in business execution",
            "Your network is your net worth in entrepreneurship",
            "Cash flow is more important than profit on paper",
            "Build systems, not just goals",
            "The best marketing is a great product",
            "Learn from failures, but don't dwell on them",
            "Adaptability is key in today's fast-changing business world",
            "Success is a journey, not a destination"
        ]
        
        self.lifestyle_tips = [
            "Start your day with 10 minutes of meditation",
            "Drink water first thing in the morning",
            "Take regular breaks to maintain focus and creativity",
            "Practice gratitude daily for better mental health",
            "Get 7-8 hours of quality sleep every night",
            "Exercise regularly to boost energy and mood",
            "Limit screen time before bed for better sleep",
            "Practice deep breathing when stressed",
            "Connect with nature regularly",
            "Learn something new every day"
        ]
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('social_media_automator.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
        # Load or create schedule
        self.schedule_file = Path('social_media_schedule.json')
        self.schedule = self.load_schedule()
    
    def load_schedule(self):
        """Load existing schedule or create new one"""
        if self.schedule_file.exists():
            try:
                with open(self.schedule_file, 'r') as f:
                    return json.load(f)
            except:
                return {'posts': [], 'last_post_date': None}
        return {'posts': [], 'last_post_date': None}
    
    def save_schedule(self):
        """Save schedule to file"""
        with open(self.schedule_file, 'w') as f:
            json.dump(self.schedule, f, indent=2)
    
    def generate_post(self, category=None):
        """Generate a random social media post"""
        if not category:
            category = random.choice(list(self.content_templates.keys()))
        
        template = random.choice(self.content_templates[category])
        
        if category == 'motivational':
            content = template.format(quote=random.choice(self.quotes))
        elif category == 'tech':
            content = template.format(tip=random.choice(self.tech_tips))
        elif category == 'business':
            content = template.format(insight=random.choice(self.business_insights))
        elif category == 'lifestyle':
            content = template.format(tip=random.choice(self.lifestyle_tips))
        
        return {
            'content': content,
            'category': category,
            'generated_at': datetime.now().isoformat(),
            'scheduled_for': None
        }
    
    def generate_content_batch(self, count=10, categories=None):
        """Generate multiple posts for different categories"""
        posts = []
        if not categories:
            categories = list(self.content_templates.keys())
        
        for i in range(count):
            category = categories[i % len(categories)]
            post = self.generate_post(category)
            posts.append(post)
        
        return posts
    
    def schedule_posts(self, posts, start_date=None, interval_hours=24):
        """Schedule posts with specified interval"""
        if not start_date:
            start_date = datetime.now()
        else:
            start_date = datetime.fromisoformat(start_date)
        
        scheduled_posts = []
        for i, post in enumerate(posts):
            scheduled_time = start_date + timedelta(hours=i * interval_hours)
            post['scheduled_for'] = scheduled_time.isoformat()
            scheduled_posts.append(post)
        
        return scheduled_posts
    
    def add_to_schedule(self, posts):
        """Add posts to the main schedule"""
        self.schedule['posts'].extend(posts)
        self.save_schedule()
        self.logger.info(f"Added {len(posts)} posts to schedule")
    
    def get_scheduled_posts(self, days_ahead=7):
        """Get posts scheduled for the next N days"""
        cutoff_date = datetime.now() + timedelta(days=days_ahead)
        return [
            post for post in self.schedule['posts']
            if post['scheduled_for'] and 
            datetime.fromisoformat(post['scheduled_for']) <= cutoff_date
        ]
    
    def mark_posted(self, post_index):
        """Mark a post as posted and remove from schedule"""
        if 0 <= post_index < len(self.schedule['posts']):
            posted_post = self.schedule['posts'].pop(post_index)
            self.schedule['last_post_date'] = datetime.now().isoformat()
            self.save_schedule()
            self.logger.info(f"Marked post as posted: {posted_post['content'][:50]}...")
            return posted_post
        return None
    
    def generate_hashtag_suggestions(self, category):
        """Generate relevant hashtags for a category"""
        hashtag_sets = {
            'motivational': ['#motivation', '#inspiration', '#success', '#mindset', '#goals', '#positivity', '#life', '#growth'],
            'tech': ['#programming', '#technology', '#coding', '#developer', '#tech', '#innovation', '#software', '#webdev'],
            'business': ['#business', '#entrepreneur', '#success', '#growth', '#entrepreneurship', '#strategy', '#leadership', '#startup'],
            'lifestyle': ['#lifestyle', '#wellness', '#health', '#mindfulness', '#tips', '#life', '#selfcare', '#balance']
        }
        return hashtag_sets.get(category, [])
    
    def analyze_engagement_potential(self, post):
        """Analyze potential engagement of a post"""
        content = post['content']
        score = 0
        
        # Length analysis
        if 100 <= len(content) <= 200:
            score += 20
        elif 200 < len(content) <= 300:
            score += 15
        
        # Hashtag analysis
        hashtag_count = content.count('#')
        if 3 <= hashtag_count <= 5:
            score += 20
        elif hashtag_count > 5:
            score += 10
        
        # Emoji analysis
        emoji_count = sum(1 for c in content if ord(c) > 127)
        if 1 <= emoji_count <= 3:
            score += 15
        
        # Question analysis
        if '?' in content:
            score += 10
        
        # Call to action analysis
        action_words = ['remember', 'try', 'start', 'learn', 'discover', 'explore']
        if any(word in content.lower() for word in action_words):
            score += 15
        
        return min(score, 100)
    
    def generate_report(self):
        """Generate a report of scheduled posts and analytics"""
        report = []
        report.append("=" * 60)
        report.append("SOCIAL MEDIA AUTOMATION REPORT")
        report.append("=" * 60)
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        # Schedule summary
        total_posts = len(self.schedule['posts'])
        report.append(f"Total posts in schedule: {total_posts}")
        
        if self.schedule['last_post_date']:
            report.append(f"Last posted: {self.schedule['last_post_date']}")
        
        # Category breakdown
        categories = {}
        for post in self.schedule['posts']:
            cat = post['category']
            categories[cat] = categories.get(cat, 0) + 1
        
        report.append("")
        report.append("Category Breakdown:")
        for cat, count in categories.items():
            report.append(f"  {cat.title()}: {count} posts")
        
        # Upcoming posts
        upcoming = self.get_scheduled_posts(7)
        report.append("")
        report.append(f"Upcoming posts (next 7 days): {len(upcoming)}")
        
        # Engagement analysis
        if self.schedule['posts']:
            avg_engagement = sum(self.analyze_engagement_potential(post) 
                               for post in self.schedule['posts']) / len(self.schedule['posts'])
            report.append(f"Average engagement potential: {avg_engagement:.1f}/100")
        
        report.append("=" * 60)
        return "\n".join(report)

def main():
    """Main function to run the social media automator"""
    print("📱 Social Media Content Automator")
    print("=" * 40)
    
    automator = SocialMediaAutomator()
    
    while True:
        print("\n🎯 Choose an option:")
        print("1. Generate single post")
        print("2. Generate content batch")
        print("3. Schedule posts")
        print("4. View scheduled posts")
        print("5. Mark post as posted")
        print("6. Generate hashtag suggestions")
        print("7. View analytics report")
        print("8. Exit")
        
        choice = input("\nEnter your choice (1-8): ").strip()
        
        if choice == '1':
            print("\n📝 Available categories:")
            for i, cat in enumerate(automator.content_templates.keys(), 1):
                print(f"{i}. {cat.title()}")
            
            cat_choice = input("Choose category (or press Enter for random): ").strip()
            category = None
            if cat_choice.isdigit() and 1 <= int(cat_choice) <= len(automator.content_templates):
                category = list(automator.content_templates.keys())[int(cat_choice) - 1]
            
            post = automator.generate_post(category)
            print(f"\n✨ Generated Post:")
            print(f"Category: {post['category'].title()}")
            print(f"Content: {post['content']}")
            print(f"Engagement Score: {automator.analyze_engagement_potential(post)}/100")
            
            save = input("\nSave to schedule? (y/n): ").lower().strip()
            if save == 'y':
                automator.add_to_schedule([post])
                print("✅ Post saved to schedule!")
        
        elif choice == '2':
            count = input("How many posts to generate? (default: 10): ").strip()
            count = int(count) if count.isdigit() else 10
            
            print("\n📝 Available categories:")
            for i, cat in enumerate(automator.content_templates.keys(), 1):
                print(f"{i}. {cat.title()}")
            
            cat_input = input("Choose categories (comma-separated, or press Enter for all): ").strip()
            categories = None
            if cat_input:
                categories = [cat.strip() for cat in cat_input.split(',')]
            
            posts = automator.generate_content_batch(count, categories)
            print(f"\n✨ Generated {len(posts)} posts:")
            
            for i, post in enumerate(posts, 1):
                print(f"\n{i}. {post['content']}")
                print(f"   Category: {post['category'].title()}")
                print(f"   Engagement: {automator.analyze_engagement_potential(post)}/100")
            
            save = input(f"\nSave all {len(posts)} posts to schedule? (y/n): ").lower().strip()
            if save == 'y':
                automator.add_to_schedule(posts)
                print("✅ Posts saved to schedule!")
        
        elif choice == '3':
            posts = automator.schedule['posts']
            if not posts:
                print("❌ No posts in schedule to organize!")
                continue
            
            print(f"\n📅 Scheduling {len(posts)} posts...")
            interval = input("Hours between posts (default: 24): ").strip()
            interval = int(interval) if interval.isdigit() else 24
            
            scheduled_posts = automator.schedule_posts(posts, interval_hours=interval)
            automator.schedule['posts'] = scheduled_posts
            automator.save_schedule()
            
            print("✅ Posts scheduled!")
            for i, post in enumerate(scheduled_posts[:5], 1):
                scheduled_time = datetime.fromisoformat(post['scheduled_for'])
                print(f"{i}. {scheduled_time.strftime('%Y-%m-%d %H:%M')} - {post['content'][:50]}...")
        
        elif choice == '4':
            upcoming = automator.get_scheduled_posts(7)
            if not upcoming:
                print("❌ No upcoming posts in the next 7 days!")
                continue
            
            print(f"\n📅 Upcoming posts (next 7 days):")
            for i, post in enumerate(upcoming, 1):
                scheduled_time = datetime.fromisoformat(post['scheduled_for'])
                print(f"{i}. {scheduled_time.strftime('%Y-%m-%d %H:%M')}")
                print(f"   {post['content']}")
                print(f"   Category: {post['category'].title()}")
                print()
        
        elif choice == '5':
            posts = automator.schedule['posts']
            if not posts:
                print("❌ No posts in schedule!")
                continue
            
            print(f"\n📝 Posts in schedule:")
            for i, post in enumerate(posts[:10], 1):
                scheduled_time = datetime.fromisoformat(post['scheduled_for']) if post['scheduled_for'] else "Not scheduled"
                print(f"{i}. {scheduled_time} - {post['content'][:50]}...")
            
            post_index = input("\nEnter post number to mark as posted: ").strip()
            if post_index.isdigit():
                posted = automator.mark_posted(int(post_index) - 1)
                if posted:
                    print(f"✅ Marked as posted: {posted['content'][:50]}...")
        
        elif choice == '6':
            print("\n📝 Available categories:")
            for i, cat in enumerate(automator.content_templates.keys(), 1):
                print(f"{i}. {cat.title()}")
            
            cat_choice = input("Choose category for hashtag suggestions: ").strip()
            if cat_choice.isdigit() and 1 <= int(cat_choice) <= len(automator.content_templates):
                category = list(automator.content_templates.keys())[int(cat_choice) - 1]
                hashtags = automator.generate_hashtag_suggestions(category)
                print(f"\n🏷️ Hashtag suggestions for {category}:")
                print(" ".join(hashtags))
        
        elif choice == '7':
            print("\n" + automator.generate_report())
        
        elif choice == '8':
            print("👋 Thanks for using Social Media Automator!")
            break
        
        else:
            print("❌ Invalid choice! Please try again.")

if __name__ == "__main__":
    main()
