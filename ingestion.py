import random
from datetime import datetime, timedelta

def generate_mock_emails(count=20):
    """Generate 20 realistic mock emails with good category distribution."""
    
    # Detailed email templates distributed across categories
    # Format: (sender, subject, body, intended_category)
    
    email_templates = [
        (
            "lottery@international-prize.com",
            "🎉 CONGRATULATIONS! You've Won $5,000,000 USD",
            """Dear Lucky Winner,

We are pleased to inform you that your email address has won FIVE MILLION US DOLLARS in our International Email Lottery Draw held on November 20, 2025.

Your winning ticket number is: LT-2025-8847392

To claim your prize, please send us the following information immediately:
- Full name and address
- Bank account details
- Copy of ID/Passport
- Processing fee of $500 USD

This is a limited time offer. Act now or lose your winnings!

Contact our claims department: claims@lottery-prize.net

Best of luck!
International Lottery Commission"""
        ),
        (
            "crypto-gains@invest-now.biz",
            "🚀 Make $10K/Day with This Secret Crypto Strategy!",
            """Hi there,

I discovered a SECRET cryptocurrency trading algorithm that generates $10,000 per day on autopilot!

This is NOT a scam. Real people are making real money. I made $450,000 in just 3 months using this system.

⭐ Zero experience needed
⭐ Fully automated trading
⭐ Guaranteed profits or money back
⭐ Limited spots available - Only 50 people!

Click here NOW to get instant access: http://bit.ly/crypto-scam-link

Don't miss this once-in-a-lifetime opportunity!

Mike Johnson
Crypto Trading Expert"""
        ),
        
        # IMPORTANT (5 emails)
        (
            "client.manager@techcorp.com",
            "URGENT: Project Deadline Extended to EOD Tomorrow",
            """Hi Team,

I just got off a call with the client, and they've agreed to extend our project deadline by 24 hours due to the scope changes we discussed last week.

CRITICAL ACTION ITEMS:
1. All developers must complete code reviews by 6 PM today
2. QA team needs to finish regression testing by 9 AM tomorrow
3. Final deployment must happen by 5 PM tomorrow (Nov 25)

The client is paying a premium for this project, and they're already concerned about the delays. We CANNOT miss this deadline. If we do, we risk losing a $500K contract and damaging our reputation.

Please confirm receipt of this email and your commitment to meeting the deadline.

This is our top priority. Cancel all other meetings if necessary.

Best regards,
Sarah Mitchell
Project Manager, TechCorp"""
        ),
        (
            "security@company.com",
            "CRITICAL: Security Breach Detected - Immediate Action Required",
            """SECURITY ALERT - CONFIDENTIAL

We have detected unauthorized access attempts to our company database from multiple IP addresses in the last 2 hours.

IMMEDIATE ACTIONS REQUIRED:
1. Change your password immediately using the company portal
2. Enable two-factor authentication if not already done
3. Review your recent account activity for any suspicious logins
4. Do NOT click on any links in emails from unknown senders
5. Report any suspicious activity to IT immediately

AFFECTED SYSTEMS:
- Employee database
- Customer records system
- Financial data warehouse

Our security team is investigating the breach. We believe this may be a targeted attack. All employees must complete mandatory security training by end of week.

If you notice anything unusual, contact IT Security immediately at x5555.

DO NOT forward this email or discuss it on unsecured channels.

Craig Williams
Chief Information Security Officer"""
        ),
        (
            "ceo@company.com",
            "Board Meeting Preparation - Need Your Input by EOD",
            """Hi,

I'm presenting our Q4 results to the board tomorrow morning, and I need your departmental performance data urgently.

Please send me by 5 PM today:
- Revenue figures for Q4
- Key achievements and metrics
- Budget variance analysis
- Q1 2026 projections

The board is particularly interested in our AI initiative progress and the new product launch timeline. Please highlight any risks or concerns we should address.

This presentation will determine our 2026 budget allocation, so accuracy is critical.

Let me know if you have any questions.

Thanks,
David Chen
CEO"""
        ),
        (
            "ops@company.com",
            "Production Server Downtime - Maintenance Window Tonight",
            """IMPORTANT: Planned Maintenance Notice

Our production servers will undergo critical maintenance tonight from 11 PM to 3 AM EST.

IMPACT:
- All web applications will be offline
- API services will be unavailable  
- Customer portal will show maintenance page
- Email services will continue to function

REASON FOR MAINTENANCE:
We're upgrading our database infrastructure to improve performance and security. This is a mandatory update that cannot be postponed.

ACTION ITEMS FOR YOUR TEAM:
1. Notify your customers about the downtime
2. Update status pages
3. Prepare support team for post-maintenance issues
4. Test critical workflows after systems come back online

We apologize for any inconvience. If you have concerns, please contact the operations team.

Best regards,
Infrastructure Team"""
        ),
        (
            "legal@company.com",
            "URGENT: GDPR Compliance Audit - Documentation Due Friday",
            """Dear Department Heads,

We have been selected for a random GDPR compliance audit by the EU Data Protection Authority. The audit begins next Monday, December 2nd.

REQUIRED DOCUMENTATION (Due by Friday, Nov 29):
1. Data processing records for the last 12 months
2. Evidence of customer consent management
3. Data breach incident reports (if any)
4. Employee privacy training completion certificates
5. Third-party data processor agreements

NON-COMPLIANCE PENALTIES:
Failure to provide complete documentation may result in fines up to €20 million or 4% of annual global revenue.

This is a mandatory request. Please treat this as highest priority.

Schedule a meeting with legal if you have questions about what documentation is needed.

Jennifer Park
Head of Legal & Compliance"""
        ),
        
        # NEWSLETTER (3 emails)
        (
            "newsletter@techweekly.io",
            "Tech Weekly: AI Agents Transform Software Development",
            """Welcome to Tech Weekly - Your source for tech industry insights

THIS WEEK'S TOP STORIES:

🤖 AI AGENTS REVOLUTIONIZE CODING
New research shows AI coding agents can now complete 80 percentage of routine programming tasks autonomously. Major tech companies are investing billions in this technology.

📱 APPLE ANNOUNCES FOLDABLE iPHONE
After years of speculation, Apple confirmed it's working on a foldable iPhone expected to launch in late 2026. Pre-orders are predicted to break records.

💼 TECH LAYOFFS CONTINUE
Despite strong earnings, major tech companies laid off 15,000 employees this month, citing "AI-driven efficiency improvements."

🔒 NEW CYBERSECURITY THREATS EMERGE
Security researchers discovered vulnerabilities affecting millions of IoT devices. Patch your systems immediately.

UPCOMING EVENTS:
- TechCrunch Disrupt: Dec 5-7
- AI Summit 2025: Dec 12-14
- DevOps World: Jan 15-17

Read the full stories at techweekly.io

Unsubscribe | Manage Preferences

© 2025 Tech Weekly"""
        ),
        (
            "communications@company.com",
            "Company Newsletter: November 2025 Highlights",
            """Dear Colleagues,

MONTHLY HIGHLIGHTS:

🎯 COMPANY ACHIEVEMENTS
- Reached 1 million active users milestone
- Expanded to 3 new countries in Europe
- Secured $50M Series B funding
- Launched 2 major product features

👥 PEOPLE & CULTURE
- Welcomed 45 new team members this month
- Employee satisfaction score improved to 4.2/5
- New parental leave policy announced
- Annual company retreat scheduled for January

🏆 TEAM SPOTLIGHT
Congratulations to the Marketing team for winning "Campaign of the Year" at the Digital Marketing Awards!

📅 UPCOMING:
- All-hands meeting: December 1st, 10 AM
- Holiday party: December 15th
- Year-end performance reviews: Dec 18-22

Stay connected | Internal Portal | Submit Ideas

Best wishes,
Communications Team"""
        ),
        (
            "updates@salesforce.com",
            "Salesforce Winter '26 Release: What's New",
            """Hi Salesforce Customer,

The Winter '26 Release is here with exciting new features!

KEY UPDATES:

✨ EINSTEIN AI ENHANCEMENTS
- Predictive lead scoring with 95% accuracy
- Automated email response suggestions
- Advanced sentiment analysis in customer calls

📊 ANALYTICS IMPROVEMENTS
- Real-time dashboard updates
- Custom report templates
- Data export to 15 new formats

🔧 PLATFORM UPDATES
- Improved API performance (50% faster)
- New mobile app features
- Enhanced security protocols

MIGRATION TIMELINE:
- Sandbox environments: Available now
- Production rollout: December 8-10
- Training webinars: Dec 1, 5, 8

RESOURCES:
- Release notes: salesforce.com/winter26
- Video tutorials: Available in Help Center
- Live Q&A session: Dec 5, 2 PM EST

Questions? Contact support@salesforce.com

Happy CRM-ing!
Salesforce Product Team"""
        ),
        
        # TO-DO (5 emails)
        (
            "calendar@company.com",
            "Meeting Invitation: Q4 Planning Session",
            """You're invited to a meeting:

MEETING: Q4 Budget Planning Session
DATE: Thursday, November 28, 2025
TIME: 2:00 PM - 4:00 PM EST
LOCATION: Conference Room 5B / Zoom Link: zoom.us/j/123456789

ATTENDEES:
- Finance Team
- Department Heads
- Operations Managers

AGENDA:
1. Review Q4 financial performance (30 mins)
2. Discuss 2026 budget proposals (45 mins)
3. Resource allocation planning (30 mins)
4. Q&A and next steps (15 mins)

PREPARATION REQUIRED:
Please review the attached budget template and come prepared with your department's funding requests for 2026.

RSVP: Click here to accept/decline
Add to Calendar

For questions, contact scheduling@company.com"""
        ),
        (
            "github@notifications.com",
            "Code Review Requested: Pull Request #402",
            """@developer - Review requested

PROJECT: Customer Portal Redesign
PULL REQUEST: #402 - Implement new authentication flow
AUTHOR: john.doe@company.com
STATUS: Ready for Review

CHANGES:
- Added OAuth2 authentication
- Implemented JWT token refresh
- Updated login UI components
- Added security tests
- Modified 15 files (+847, -234 lines)

BLOCKERS:
This PR blocks the release scheduled for next Tuesday. Please review ASAP.

REVIEW CHECKLIST:
□ Code quality and standards
□ Security vulnerabilities
□ Test coverage (current: 87%)
□ Performance implications
□ Documentation updates

TESTING NOTES:
All unit tests passing. Manual QA completed in staging environment.

View Pull Request: github.com/company/project/pull/402
Leave Review | Approve | Request Changes

GitHub Notifications"""
        ),
        (
            "manager@company.com",
            "Action Required: Approve Marketing Budget Proposal",
            """Hi,

I've submitted the Q1 marketing budget proposal for your approval. The document is in the shared drive under "Finance/Q1 2026 Budgets".

KEY HIGHLIGHTS:
- Total budget request: $250,000
- Digital advertising: $120,000
- Content creation: $50,000
- Events and conferences: $80,000

JUSTIFICATION:
This represents a 15% increase from last quarter, primarily due to our product launch campaign planned for February.

Expected ROI: 3.5x based on historical data.

REQUIRED ACTION:
Please review and approve by December 1st so we can finalize contracts with vendors.

The document includes detailed breakdowns, projected outcomes, and comparative analysis with previous quarters.

Let me know if you need any clarification or want to discuss any line items.

Thanks,
Amanda Roberts
Marketing Director"""
        ),
        (
            "finance@company.com",
            "Reminder: Submit November Expense Reports by Friday",
            """Dear Team,

This is a reminder that all November expense reports must be submitted by end of day Friday, November 29th.

SUBMISSION PROCESS:
1. Log into the expense portal: expenses.company.com
2. Upload receipts for all expenses over $25
3. Categorize each expense correctly
4. Add business justification in notes
5. Submit for manager approval

MISSING RECEIPTS:
If you've lost a receipt, fill out the Missing Receipt Declaration form.

COMMON MISTAKES TO AVOID:
- Personal expenses mixed with business expenses
- Missing merchant names or dates
- Incorrect currency conversions
- Duplicate submissions

APPROVAL TIMELINE:
- Submit by Nov 29
- Manager approval: Nov 30 - Dec 4
- Reimbursement: Dec 10 payroll

Questions? Contact finance@company.com or x3000

Thank you for your cooperation!

Finance Department"""
        ),
        (
            "hr@company.com",
            "Action Required: Complete Mandatory Compliance Training",
            """Dear Employee,

You have outstanding mandatory training courses that must be completed by December 15, 2025.

REQUIRED COURSES:
□ Cybersecurity Awareness (45 minutes)
□ Anti-Harassment Training (60 minutes)  
□ Data Privacy & GDPR (30 minutes)
□ Workplace Safety (20 minutes)

TOTAL TIME: Approximately 2.5 hours

WHY THIS MATTERS:
Completion of these courses is mandatory for continued employment. Failure to complete by the deadline may result in:
- Suspension of system access
- Formal warning in personnel file
- Potential termination

ACCESSING THE COURSES:
1. Visit: training.company.com
2. Login with your company credentials
3. Click "My Required Training"
4. Complete all modules

TRACKING:
Your manager receives weekly reports on training compliance. Currently, only 60% of employees have completed their training.

SUPPORT:
If you have technical issues, contact helpdesk@company.com

Please prioritize this task.

Best regards,
Human Resources"""
        ),
        
        # UNCATEGORIZED (5 emails)
        (
            "friend@gmail.com",
            "Happy Birthday! 🎉",
            """Hey!

Happy Birthday! Hope you have an amazing day celebrating with family and friends.

Can't believe another year has flown by. Remember when we were just starting our careers? Time flies!

Let me know if you want to grab dinner this weekend to celebrate properly. My treat!

Enjoy your special day!

Cheers,
Alex""",
        ),
        (
            "colleague@company.com",
            "Lunch today?",
            """Hey,

Want to grab lunch today around 12:30? I was thinking we could try that new taco place that opened downtown.

I also wanted to chat about the upcoming project. Nothing urgent, just wanted to bounce some ideas off you in a casual setting.

Let me know if you're free!

- Mike"""
        ),
        (
            "travel.buddy@outlook.com",
            "FWD: 10 Hidden Gems in Tokyo You Must Visit",
            """Hey! 

Saw this article and thought of you since you mentioned you might visit Japan next year. Some really cool recommendations here.

----------FORWARDED MESSAGE----------

Top 10 Hidden Gems in Tokyo:

1. Yanaka Ginza - Traditional shopping street
2. TeamLab Borderless - Digital art museum  
3. Shimokitazawa - Hip neighborhood with vintage shops
4. Omoide Yokocho - Tiny bars and izakayas
5. Koenji - Alternative culture district

... and 5 more!

Check out the full article for details, photos, and maps.

Would love to join you if you decide to go!

Sarah"""
        ),
        (
            "jokes@listserv.com",
            "Friday Funnies: Tech Jokes to End Your Week",
            """Happy Friday! Time for your weekly dose of tech humor:

Q: Why do programmers prefer dark mode?
A: Because light attracts bugs! 🐛

Q: How many programmers does it take to change a light bulb?
A: None. It's a hardware problem.

A SQL query walks into a bar, walks up to two tables and asks...
"Can I join you?" 😄

Why did the developer go broke?
Because he used up all his cache!

There are 10 types of people in the world:
Those who understand binary, and those who don't.

Have a great weekend! No deployments on Friday, please! 🚀

Unsubscribe | Send us your jokes"""
        ),
        (
            "events@community.org",
            "Local Tech Meetup: Networking Event Next Thursday",
            """Hi Tech Enthusiasts,

Join us for our monthly networking meetup!

WHAT: Tech Professionals Networking Night
WHEN: Thursday, December 5th, 6-9 PM
WHERE: The Innovation Hub, 123 Tech Street
WHO: Software engineers, designers, product managers, entrepreneurs

AGENDA:
- 6:00 PM: Registration & appetizers
- 6:30 PM: Lightning talks (5 mins each)
- 7:30 PM: Open networking
- 8:00 PM: Drinks & casual chat

SPEAKERS:
- "Building AI Products" - Jane Smith, CTO at AI Corp
- "Remote Work Best Practices" - Bob Jones, Engineering Manager

FREE to attend. Optional paid dinner at 9 PM at nearby restaurant.

RSVP at: meetup.com/tech-professionals

See you there!

Community Events Team"""
        ),
    ]
    
    emails = []
    
    # Generate exactly 20 emails with varied timestamps
    for i in range(20):
        sender, subject, body = email_templates[i]
        
        # Vary the timestamp for realism
        hours_ago = random.randint(1, 72)  # 1-72 hours ago
        minutes_ago = random.randint(0, 59)
        timestamp = datetime.now() - timedelta(hours=hours_ago, minutes=minutes_ago)
        
        email = {
            "id": i + 1,
            "sender": sender,
            "subject": subject,
            "body": body,
            "timestamp": timestamp,
            "category": "Uncategorized",  # Start uncategorized, LLM will categorize
            "action_items": [],
            "is_read": False
        }
        emails.append(email)
        
    return emails
