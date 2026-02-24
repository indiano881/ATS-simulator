JOB_ADS = {
    "frontend": {
        "id": "frontend",
        "title": "Junior Frontend Developer",
        "company": "TechStart Inc.",
        "description": (
            "We are looking for a Junior Frontend Developer to join our growing team. "
            "You will work closely with designers and backend engineers to build responsive "
            "web applications.\n\n"
            "Requirements:\n"
            "- Proficiency in HTML, CSS, and JavaScript\n"
            "- Experience with React or similar frontend frameworks\n"
            "- Familiarity with Git and version control workflows\n"
            "- Understanding of responsive design and mobile-first development\n"
            "- Knowledge of RESTful APIs and asynchronous programming\n"
            "- Experience with TypeScript is a plus\n"
            "- Familiarity with testing frameworks (Jest, Cypress)\n"
            "- Good understanding of web accessibility (WCAG)\n\n"
            "Nice to have:\n"
            "- Experience with CSS preprocessors (Sass, LESS)\n"
            "- Knowledge of CI/CD pipelines\n"
            "- Portfolio of personal or open-source projects\n"
            "- Understanding of UX/UI design principles"
        ),
        "keywords": [
            "html",
            "css",
            "javascript",
            "react",
            "git",
            "responsive design",
            "rest api",
            "typescript",
            "testing",
            "jest",
            "cypress",
            "accessibility",
            "sass",
            "frontend",
            "web development",
            "version control",
            "mobile first",
            "ui",
            "ux",
            "agile",
            "node",
            "npm",
            "webpack",
            "figma",
        ],
    },
    "marketing": {
        "id": "marketing",
        "title": "Marketing Coordinator",
        "company": "BrandFlow Agency",
        "description": (
            "BrandFlow Agency is seeking a Marketing Coordinator to support our "
            "digital marketing campaigns and brand strategy efforts.\n\n"
            "Requirements:\n"
            "- Experience with social media management and content creation\n"
            "- Knowledge of SEO and SEM best practices\n"
            "- Familiarity with analytics tools (Google Analytics, social media insights)\n"
            "- Strong copywriting and content strategy skills\n"
            "- Experience with email marketing platforms (Mailchimp, HubSpot)\n"
            "- Understanding of campaign management and A/B testing\n"
            "- Basic graphic design skills (Canva, Adobe Creative Suite)\n\n"
            "Nice to have:\n"
            "- Experience with CRM systems\n"
            "- Knowledge of marketing automation\n"
            "- Video editing skills\n"
            "- Experience with influencer marketing\n"
            "- Understanding of brand positioning and market research"
        ),
        "keywords": [
            "social media",
            "content creation",
            "seo",
            "sem",
            "google analytics",
            "analytics",
            "copywriting",
            "content strategy",
            "email marketing",
            "mailchimp",
            "hubspot",
            "campaign management",
            "a/b testing",
            "graphic design",
            "canva",
            "adobe",
            "crm",
            "marketing automation",
            "brand",
            "market research",
            "digital marketing",
            "kpi",
            "roi",
            "engagement",
        ],
    },
}


def get_job_ads():
    return JOB_ADS


def get_job_ad(job_id):
    return JOB_ADS.get(job_id)
