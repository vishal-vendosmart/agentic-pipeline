# Agent Specification: Writer (ProQSmart)

**ID:** `writer-vertical-a`  
**Role:** Content Generation + SEO Writing  
**Vertical:** ProQSmart (Vertical A)  
**Primary Model:** `ollama-cloud/gemma4:31b`  
**Workspace:** `/root/.openclaw/workspace-vertical-a/drafts/`

---

## 1. Purpose

Generate SEO-optimized, fact-grounded content for ProQSmart including blog posts, landing pages, case studies, and social media posts. All content must cite verified facts from Neo4j Knowledge Graph with zero hallucinations.

---

## 2. Inputs

### 2.1 From Project Manager

**Format:** `sessions_spawn` task

**Example:**
```json
{
  "task": "Write 10 pillar articles for ProQSmart",
  "params": {
    "objective": "Generate 20 leads/month from manufacturing SMEs",
    "vertical": "A",
    "linearTaskId": "MAR-125",
    "contentTypes": ["blog posts", "landing pages"],
    "targetKeywords": ["AI procurement software", "manufacturing automation"],
    "wordCount": 2000
  }
}
```

### 2.2 From Researcher Agent

**Format:** JSON files in workspace

**Files:**
- `/root/.openclaw/workspace-vertical-a/research/keyword-strategy.json`
- `/root/.openclaw/workspace-vertical-a/research/competitor-analysis.md`
- `/root/.openclaw/workspace-vertical-a/research/industry-trends.md`

**Example - keyword-strategy.json:**
```json
{
  "primaryKeywords": [
    {
      "term": "AI procurement software",
      "volume": 2400,
      "difficulty": 45,
      "intent": "commercial"
    }
  ],
  "contentGaps": ["No ROI calculators", "Few case studies"]
}
```

### 2.3 From Knowledge Graph

**Format:** Neo4j Cypher queries

**Queries:**
```cypher
// Get keywords for topic
MATCH (k:Keyword {vertical: "A"})
WHERE k.term CONTAINS "procurement"
RETURN k.term, k.volume, k.difficulty, k.intent

// Get verified facts
MATCH (f:Fact)
WHERE ANY(kw IN f.relatedKeywords WHERE kw CONTAINS "procurement")
AND f.verified = true
RETURN f.claim, f.source, f.confidence
ORDER BY f.confidence DESC

// Get competitor content
MATCH (c:Competitor)-[:COMPETES_WITH]->(:Vertical {id: "A"})
RETURN c.name, c.contentGaps
```

---

## 3. Outputs

### 3.1 To Workspace

**Files Created:**
- `/root/.openclaw/workspace-vertical-a/drafts/YYYY-MM-DD-article-slug.md`
- `/root/.openclaw/workspace-vertical-a/drafts/YYYY-MM-DD-landing-page-slug.md`

**Example - Blog Post:**
```markdown
---
title: "AI Procurement Software: Complete Guide for Manufacturing SMEs"
slug: "ai-procurement-software-guide"
targetKeyword: "AI procurement software"
metaDescription: "Reduce procurement costs by 30% with AI. Complete guide for manufacturing SMEs with real case studies and ROI analysis."
wordCount: 2450
publishedAt: 2026-07-26
---

# AI Procurement Software: Complete Guide for Manufacturing SMEs

## Introduction

Manufacturing SMEs face increasing pressure to reduce costs while maintaining quality. Manual procurement processes are slow, error-prone, and miss savings opportunities.

**Key Insight:** 73% of manufacturing SMEs plan to adopt AI in 2026 (Manufacturing Tech Survey 2026).

AI procurement software reduces costs by 30% while improving supplier relationships (ProcureAI Case Study 2025).

## Current Challenges in Manufacturing Procurement

### Challenge 1: Manual Purchase Orders

Traditional procurement requires manual creation of purchase orders, leading to:
- 4-6 hours per order average
- 15% error rate in manual data entry
- Missed bulk discount opportunities

### Challenge 2: Supplier Management

Managing multiple suppliers without automation:
- No real-time price comparison
- Delayed payment tracking
- Poor supplier performance visibility

## How AI Procurement Software Works

[Continue with full article content...]

## Call to Action

Ready to transform your procurement process? [Request a demo](#) of ProQSmart's AI-powered procurement platform.

---

## Sources
1. Manufacturing Tech Survey 2026 - https://example.com/survey-2026.pdf
2. ProcureAI Case Study 2025 - https://procureai.com/case-study
```

**Example - Landing Page:**
```markdown
---
title: "AI-Powered Procurement for Manufacturing SMEs"
slug: "procurement-automation-landing"
targetKeyword: "procurement automation software"
metaDescription: "Reduce procurement costs by 30% with ProQSmart's AI platform. Trusted by 500+ manufacturing SMEs."
pageType: "landing"
cta: "Request Demo"
---

# Reduce Procurement Costs by 30% with AI

**ProQSmart** helps manufacturing SMEs automate procurement, reduce costs, and build stronger supplier relationships.

[Request Demo] [View Pricing]

## Trusted by 500+ Manufacturing Companies

[Logo grid...]

## Key Benefits

### 30% Cost Reduction
AI-powered supplier matching finds the best prices automatically.

### 80% Time Savings
Automate purchase orders, approvals, and payments.

### Real-Time Analytics
Track spending, supplier performance, and savings in one dashboard.

## How It Works

1. **Connect Suppliers** - Import your supplier list
2. **AI Matching** - Get optimal supplier recommendations
3. **Automate Orders** - Set up automated purchase orders
4. **Track Savings** - Monitor cost reduction in real-time

[Continue with full landing page...]

## Get Started Today

Join 500+ manufacturing SMEs saving with ProQSmart.

[Request Demo]
```

### 3.2 To Zernio (Social Media)

**Format:** Social media posts derived from content

**Example:**
```json
{
  "platform": "linkedin",
  "content": "🎯 New Guide: AI Procurement Software for Manufacturing SMEs\n\nKey findings from our latest research:\n✅ 73% of SMEs plan AI adoption in 2026\n✅ 30% cost reduction with AI procurement\n✅ 80% time savings on purchase orders\n\nRead the full guide: [link]\n\n#Manufacturing #AI #Procurement #SME",
  "hashtags": ["Manufacturing", "AI", "Procurement", "SME"],
  "scheduledFor": "2026-07-27T09:00:00Z"
}
```

### 3.3 To Linear

**Updates:**
```graphql
mutation {
  updateIssue(
    id: "MAR-125"
    input: {
      description: """
      ✅ Content Creation Complete
      
      **Articles Written:** 10
      - Blog posts: 7 (avg 2,350 words)
      - Landing pages: 3
      
      **SEO Optimization:**
      - Target keywords included: 100%
      - Meta descriptions: All complete
      - Internal links: 3-5 per article
      
      **Fact Verification:**
      - All claims cited: ✅
      - Sources verified: ✅
      - Zero hallucinations: ✅
      
      **Social Posts:** 10 scheduled via Zernio
      
      **Next:** Designer agent can create page layouts
      """
      stateId: "done"
    }
  ) {
    success
  }
}
```

---

## 4. Behaviors

### 4.1 Content Planning Workflow

**Step 1: Review Keyword Strategy**
```python
import json

# Load keyword strategy
with open('workspace-vertical-a/research/keyword-strategy.json') as f:
    keyword_data = json.load(f)

# Extract primary keywords
primary_keywords = keyword_data['primaryKeywords'][:10]

# Plan content around keywords
content_plan = []
for kw in primary_keywords:
    content_plan.append({
        'type': 'blog post',
        'target_keyword': kw['term'],
        'estimated_words': 2000,
        'angle': 'Complete guide'
    })
```

**Step 2: Query Knowledge Graph for Facts**
```python
from neo4j import GraphDatabase

driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

def get_facts_for_topic(topic: str) -> list:
    with driver.session() as session:
        result = session.run("""
            MATCH (f:Fact)
            WHERE ANY(kw IN f.relatedKeywords WHERE kw CONTAINS $topic)
            AND f.verified = true
            RETURN f.claim, f.source, f.sourceUrl, f.confidence
            ORDER BY f.confidence DESC
            LIMIT 10
        """, topic=topic)
        
        return [dict(record) for record in result]

# Get facts for each article
for article in content_plan:
    article['facts'] = get_facts_for_topic(article['target_keyword'])
```

**Step 3: Create Content Outline**
```python
def create_outline(keyword: str, facts: list) -> dict:
    return {
        'title': f"{keyword.title()}: Complete Guide",
        'sections': [
            'Introduction',
            'Current Challenges',
            f'How {keyword} Works',
            'Benefits',
            'Implementation Guide',
            'Case Studies',
            'Conclusion',
            'Call to Action'
        ],
        'facts_to_cite': facts,
        'estimated_word_count': 2000
    }
```

### 4.2 Content Generation Workflow

**Step 1: Generate Introduction**
```python
def generate_introduction(keyword: str, facts: list) -> str:
    prompt = f"""
    Write an engaging introduction for an article about "{keyword}".
    
    Requirements:
    - Hook: Start with a compelling statistic or problem statement
    - Context: Explain why this matters for manufacturing SMEs
    - Thesis: What reader will learn
    - Include 1-2 verified facts from the list below
    
    Facts to use:
    {json.dumps(facts[:3], indent=2)}
    
    Tone: Professional but accessible
    Length: 150-200 words
    """
    
    return llm_generate(prompt)
```

**Step 2: Generate Body Sections**
```python
def generate_section(section_name: str, keyword: str, facts: list) -> str:
    prompt = f"""
    Write the "{section_name}" section for an article about "{keyword}".
    
    Requirements:
    - Provide actionable information
    - Include relevant facts with citations
    - Use subheadings for readability
    - Include examples where relevant
    
    Available facts:
    {json.dumps(facts, indent=2)}
    
    Tone: Expert but accessible
    Length: 300-400 words
    """
    
    return llm_generate(prompt)
```

**Step 3: Generate Meta Information**
```python
def generate_meta_data(content: str, keyword: str) -> dict:
    prompt = f"""
    Based on the article content and target keyword "{keyword}", generate:
    
    1. Meta title (50-60 characters, include keyword)
    2. Meta description (150-160 characters, compelling CTA)
    3. Slug (URL-friendly, include keyword)
    4. 3-5 internal linking suggestions
    
    Content:
    {content[:500]}...
    """
    
    return llm_generate_json(prompt)
```

### 4.3 Fact Citation Workflow

**Rule:** Every statistic, claim, or non-obvious statement must cite a verified source.

**Implementation:**
```python
def add_citations(content: str, facts: list) -> str:
    """Add inline citations to content"""
    
    for fact in facts:
        claim = fact['claim']
        source = fact['source']
        url = fact.get('sourceUrl', '')
        
        # Find where claim appears in content
        if claim.lower() in content.lower():
            # Add citation
            citation = f" ({source})"
            if url:
                citation += f" - {url}"
            
            # Replace with cited version
            content = content.replace(claim, claim + citation)
    
    return content

# Add sources section at end
def add_sources_section(facts: list) -> str:
    sources = "\n\n## Sources\n\n"
    for i, fact in enumerate(facts, 1):
        sources += f"{i}. {fact['source']}"
        if fact.get('sourceUrl'):
            sources += f" - {fact['sourceUrl']}"
        sources += "\n"
    
    return sources
```

### 4.4 Social Media Post Generation

**Step 1: Extract Key Points**
```python
def extract_key_points(content: str) -> list:
    prompt = f"""
    Extract 3-5 key points from this article for social media:
    
    {content[:1000]}...
    
    Format as bullet points, each under 100 characters.
    Include statistics and numbers where available.
    """
    
    return llm_generate_list(prompt)
```

**Step 2: Generate Platform-Specific Posts**
```python
def generate_social_posts(key_points: list, article_url: str) -> dict:
    posts = {}
    
    # LinkedIn
    posts['linkedin'] = f"""
🎯 New Guide: [Article Title]

Key findings:
{chr(10).join(f"✅ {point}" for point in key_points)}

Read the full guide: {article_url}

#Manufacturing #AI #Procurement #SME
"""
    
    # Twitter/X
    posts['twitter'] = f"""
📊 New research: [Article Title]

{key_points[0]}
{key_points[1]}

Full guide: {article_url}

#AI #Manufacturing
"""
    
    return posts
```

**Step 3: Schedule via Zernio**
```python
import requests

def schedule_zernio_post(post_data: dict, scheduled_time: str):
    response = requests.post(
        'https://zernio.com/api/v1/posts',
        headers={
            'Authorization': f'Bearer {ZERNIO_API_KEY}',
            'Content-Type': 'application/json'
        },
        json={
            'content': post_data['content'],
            'platforms': [post_data['platform']],
            'scheduledAt': scheduled_time,
            'hashtags': post_data.get('hashtags', [])
        }
    )
    
    return response.json()
```

---

## 5. Tools Required

### 5.1 OpenClaw Tools

| Tool | Permission | Purpose |
|------|------------|---------|
| `read` | Allow | Read keyword strategy, research files |
| `write` | Allow | Write article drafts |
| `edit` | Allow | Edit and revise content |
| `sessions_history` | Allow | Access conversation context |
| `exec` | Allow | Run Python scripts for Neo4j, Zernio |

### 5.2 External APIs

| API | Purpose | Free Tier | MVP Usage |
|-----|---------|-----------|-----------|
| **Neo4j** | Query facts, keywords | Self-hosted (free) | Unlimited |
| **Zernio** | Social media scheduling | Already have API key | Unlimited |

### 5.3 Python Dependencies

```txt
neo4j                  # Neo4j driver
python-dateutil        # Date parsing
requests               # HTTP requests for Zernio
markdown               # Markdown processing
```

---

## 6. Configuration

### 6.1 Environment Variables

```bash
# Neo4j
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your-password

# Zernio
ZERNIO_API_KEY=sk_xxx  # Replace with actual key in .env
ZERNIO_BASE_URL=https://zernio.com/api/v1

# OpenClaw
OPENCLAW_WORKSPACE=/root/.openclaw/workspace-vertical-a
```

### 6.2 Model Configuration

```json
{
  "model": {
    "primary": "ollama-cloud/gemma4:31b",
    "fallbacks": ["ollama-cloud/glm-5.1"],
    "timeoutSeconds": 600
  }
}
```

### 6.3 Tool Configuration

```json
{
  "tools": {
    "allow": [
      "read",
      "write",
      "edit",
      "sessions_history",
      "exec"
    ],
    "deny": [
      "process",
      "browser",
      "canvas",
      "cron",
      "web_search",
      "web_fetch"
    ]
  }
}
```

---

## 7. Testing

### 7.1 Unit Tests

**Test: Fact Citation**
```python
def test_fact_citation():
    content = "73% of SMEs plan AI adoption"
    facts = [{
        'claim': '73% of SMEs plan AI adoption',
        'source': 'Manufacturing Tech Survey 2026',
        'sourceUrl': 'https://example.com/survey.pdf'
    }]
    
    result = add_citations(content, facts)
    assert '(Manufacturing Tech Survey 2026)' in result
    assert 'https://example.com/survey.pdf' in result
```

**Test: Meta Description Generation**
```python
def test_meta_generation():
    content = "Article about AI procurement software..."
    keyword = "AI procurement software"
    
    meta = generate_meta_data(content, keyword)
    
    assert 50 <= len(meta['title']) <= 60
    assert 150 <= len(meta['description']) <= 160
    assert keyword in meta['title'].lower()
```

### 7.2 Integration Tests

**Test: Full Content Generation**
```python
async def test_full_content_generation():
    # 1. Spawn writer agent
    await sessions_spawn(
        agentId="writer-vertical-a",
        task="Write 5 blog posts about AI procurement",
        params={
            "keywords": ["AI procurement software"],
            "wordCount": 2000
        }
    )
    
    # 2. Wait for completion (timeout: 60 minutes)
    await wait_for_completion(timeout=3600)
    
    # 3. Verify outputs
    drafts_dir = "workspace-vertical-a/drafts"
    articles = glob(f"{drafts_dir}/*.md")
    assert len(articles) >= 5
    
    # 4. Verify all articles have citations
    for article in articles:
        with open(article) as f:
            content = f.read()
            assert "## Sources" in content
            assert "http" in content  # URLs present
    
    # 5. Verify Linear updated
    task = await linear.getIssue("MAR-125")
    assert task.stateId == "done"
```

### 7.3 Success Criteria

- ✅ All articles include 3-5 verified facts with citations
- ✅ Zero hallucinated statistics or claims
- ✅ Meta descriptions 150-160 characters
- ✅ Target keywords in title, H1, first 100 words
- ✅ 3-5 internal linking suggestions per article
- ✅ Social posts generated for each article
- ✅ Writing completes within 60 minutes for 10 articles
- ✅ Linear task updated with summary

---

## 8. Error Handling

### 8.1 Missing Facts in KG

**Scenario:** No verified facts found for topic

**Detection:**
```python
facts = get_facts_for_topic(topic)
if not facts:
    logger.warning(f"No verified facts found for topic: {topic}")
    # Flag for human review
    await notify_human(f"⚠️ No facts available for '{topic}'")
```

**Recovery:**
1. Request researcher agent to find facts
2. Write article without statistics (general guide)
3. Flag article for fact-checking before publish

### 8.2 Zernio API Failures

**Scenario:** Cannot schedule social posts

**Detection:**
```python
try:
    response = schedule_zernio_post(post_data, scheduled_time)
except requests.HTTPError as e:
    logger.error(f"Zernio API error: {e}")
    # Save posts to file instead
    save_posts_to_file(post_data)
```

**Recovery:**
1. Save posts to JSON file
2. Retry Zernio API every 15 minutes
3. Notify human if >1 hour downtime

### 8.3 Content Quality Issues

**Scenario:** Generated content doesn't meet quality standards

**Detection:**
```python
def check_quality(content: str) -> dict:
    checks = {
        'word_count': len(content.split()) >= 2000,
        'has_citations': '## Sources' in content,
        'has_meta': '---' in content[:500],
        'has_cta': 'Request Demo' in content or '[link]' in content
    }
    
    return {
        'passed': all(checks.values()),
        'checks': checks
    }
```

**Recovery:**
1. Regenerate failing sections
2. If still failing, flag for human edit
3. Log quality issues for prompt improvement

---

## 9. Content Quality Guidelines

### 9.1 Writing Standards

**Tone:**
- Professional but accessible
- Expert without being condescending
- Actionable and practical
- No generic AI hype

**Structure:**
- Clear H1, H2, H3 hierarchy
- Short paragraphs (3-5 sentences)
- Bullet points for lists
- Bold for emphasis

**SEO Requirements:**
- Target keyword in title (H1)
- Target keyword in first 100 words
- Target keyword in 2-3 H2s
- Target keyword in conclusion
- Keyword density: 1-2%
- Meta description: 150-160 characters

### 9.2 Fact Citation Standards

**Must Cite:**
- All statistics (percentages, numbers)
- Research findings
- Case study results
- Non-obvious claims

**Don't Need Citation:**
- Common knowledge
- Your own product features
- General advice

**Citation Format:**
```markdown
According to Manufacturing Tech Survey 2026, 73% of SMEs plan AI adoption.

[Source]: Manufacturing Tech Survey 2026 - https://example.com/survey.pdf
```

### 9.3 Internal Linking Strategy

**Rules:**
- 3-5 internal links per article
- Link to pillar content first
- Use descriptive anchor text
- Avoid generic "click here"

**Examples:**
```markdown
✅ Good: "Learn more about [AI procurement benefits](/blog/ai-procurement-benefits)"
❌ Bad: "Click [here](/blog/ai-procurement-benefits) to learn more"
```

---

## 10. Performance Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| **Content Velocity** | 10 articles/hour | Articles completed / Time |
| **Fact Citation Rate** | 100% | Articles with citations / Total |
| **Zero Hallucinations** | 100% | Verified claims / Total claims |
| **SEO Compliance** | 95%+ | Articles meeting SEO rules / Total |
| **Social Posts Generated** | 1 per article | Posts created / Articles |
| **Writing Duration** | <60 min for 10 articles | Start to completion time |
| **Human Edit Rate** | <10% | Articles needing edits / Total |

---

## 11. Content Templates

### 11.1 Blog Post Template

```markdown
---
title: "[Keyword]: Complete Guide"
slug: "[keyword]-guide"
targetKeyword: "[primary keyword]"
metaDescription: "[150-160 char description with CTA]"
wordCount: 2000
publishedAt: YYYY-MM-DD
---

# [Keyword]: Complete Guide

## Introduction

[Hook with statistic] (Source)

[Context and problem statement]

[Thesis: What reader will learn]

## Current Challenges

### Challenge 1: [Name]

[Description with facts] (Source)

### Challenge 2: [Name]

[Description with facts] (Source)

## How [Keyword] Works

[Explanation with examples]

## Benefits

- **Benefit 1:** [Description] (Source if applicable)
- **Benefit 2:** [Description] (Source if applicable)
- **Benefit 3:** [Description] (Source if applicable)

## Implementation Guide

### Step 1: [Action]

[Detailed instructions]

### Step 2: [Action]

[Detailed instructions]

### Step 3: [Action]

[Detailed instructions]

## Case Studies

### Company X: [Result]

[Story with metrics] (Source)

## Conclusion

[Summary of key points]

[Final CTA]

## Sources

1. [Source Name] - [URL]
2. [Source Name] - [URL]
3. [Source Name] - [URL]
```

### 11.2 Landing Page Template

```markdown
---
title: "[Value Proposition] | ProQSmart"
slug: "[keyword]-landing"
targetKeyword: "[primary keyword]"
metaDescription: "[150-160 char with CTA]"
pageType: "landing"
cta: "[Primary CTA text]"
---

# [Headline: Main Value Proposition]

[Subheadline: Supporting statement]

[Primary CTA Button] [Secondary CTA Button]

## Trusted by [Number]+ Companies

[Logo Grid]

## The Problem

[Problem statement with stats] (Source)

## The Solution

[How ProQSmart solves it]

## Key Benefits

### [Benefit 1]

[Description with metric] (Source)

### [Benefit 2]

[Description with metric] (Source)

### [Benefit 3]

[Description with metric] (Source)

## How It Works

1. **[Step 1]** - [Description]
2. **[Step 2]** - [Description]
3. **[Step 3]** - [Description]
4. **[Step 4]** - [Description]

## Social Proof

> "[Testimonial quote]"
> 
> — [Name], [Title] at [Company]

## Pricing

[Simple pricing table or "Contact for pricing"]

## FAQ

### Q: [Common question]?

A: [Answer]

### Q: [Common question]?

A: [Answer]

## Final CTA

[Ready to get started?]

[Primary CTA Button]

---

## Sources

1. [Source Name] - [URL]
```

---

**Document End**

*Last updated: 2026-07-26*  
*Version: 1.0*  
*Next review: After Phase 3 implementation*
