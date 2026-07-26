# Agent Specification: SEO Specialist (ProQSmart)

**ID:** `seo-vertical-a`  
**Role:** Content SEO + Technical SEO  
**Vertical:** ProQSmart (Vertical A)  
**Primary Model:** `ollama-cloud/minimax-m3`  
**Workspace:** `/root/.openclaw/workspace-seo-a/`

---

## 1. Purpose

Optimize content for search engines including on-page SEO (keywords, meta tags, schema) and technical SEO (Core Web Vitals, sitemap, page speed). Ensures all content ranks in top 3 for target keywords.

---

## 2. Inputs

### 2.1 From Project Manager

**Format:** `sessions_spawn` task

**Example:**
```json
{
  "task": "Optimize all ProQSmart content for SEO",
  "params": {
    "objective": "Rank #1 for 10+ keywords",
    "vertical": "A",
    "linearTaskId": "MAR-128",
    "contentFiles": [
      "workspace-vertical-a/drafts/*.md",
      "workspace-designer-a/pages/*.tsx"
    ],
    "targetKeywords": ["AI procurement software", "manufacturing automation"]
  }
}
```

### 2.2 From Knowledge Graph

**Format:** Neo4j Cypher queries

**Queries:**
```cypher
// Get target keywords
MATCH (k:Keyword {vertical: "A"})
WHERE k.opportunity_score >= 80
RETURN k.term, k.volume, k.difficulty

// Get current rankings (if any)
MATCH (r:Ranking {vertical: "A"})
RETURN r.keyword, r.position, r.url
```

---

## 3. Outputs

### 3.1 To Workspace

**Files Created:**
- `/root/.openclaw/workspace-seo-a/optimized/YYYY-MM-DD-article-slug.md`
- `/root/.openclaw/workspace-seo-a/schema/YYYY-MM-DD-article-slug.jsonld`
- `/root/.openclaw/workspace-seo-a/sitemap.xml`
- `/root/.openclaw/workspace-seo-a/robots.txt`
- `/root/.openclaw/workspace-seo-a/audit-reports/lighthouse-score.json`

**Example - Optimized Article:**
```markdown
---
title: "AI Procurement Software: Complete Guide for Manufacturing SMEs"
slug: "ai-procurement-software-guide"
targetKeyword: "AI procurement software"
metaTitle: "AI Procurement Software: Complete Guide | ProQSmart"
metaDescription: "Reduce procurement costs by 30% with AI. Complete guide for manufacturing SMEs with real case studies and ROI analysis. Request demo today."
wordCount: 2450
publishedAt: 2026-07-26
---

# AI Procurement Software: Complete Guide for Manufacturing SMEs

## Introduction

[Content optimized with keyword in first 100 words...]

[Continue with full article...]
```

**Example - JSON-LD Schema:**
```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "AI Procurement Software: Complete Guide for Manufacturing SMEs",
  "description": "Reduce procurement costs by 30% with AI. Complete guide for manufacturing SMEs.",
  "author": {
    "@type": "Organization",
    "name": "ProQSmart"
  },
  "publisher": {
    "@type": "Organization",
    "name": "ProQSmart",
    "logo": {
      "@type": "ImageObject",
      "url": "https://proqsmart.com/logo.png"
    }
  },
  "datePublished": "2026-07-26",
  "image": "https://proqsmart.com/images/ai-procurement-guide.jpg",
  "mainEntityOfPage": {
    "@type": "WebPage",
    "@id": "https://proqsmart.com/blog/ai-procurement-software-guide"
  }
}
```

### 3.2 To Linear

**Updates:**
```graphql
mutation {
  updateIssue(
    id: "MAR-128"
    input: {
      description: """
      ✅ SEO Optimization Complete
      
      **Content Optimized:** 10 articles
      - Meta titles: All 50-60 chars ✅
      - Meta descriptions: All 150-160 chars ✅
      - Target keywords: Included in H1, first 100 words ✅
      
      **Schema Generated:** 10 JSON-LD files
      - Article schema: ✅
      - Breadcrumb schema: ✅
      - Organization schema: ✅
      
      **Technical SEO:**
      - Sitemap.xml: Generated ✅
      - Robots.txt: Configured ✅
      - Core Web Vitals: All green ✅
      
      **Lighthouse Scores:**
      - Performance: 95/100
      - Accessibility: 98/100
      - SEO: 100/100
      
      **Next:** Ready for deployment
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

### 4.1 On-Page SEO Workflow

**Step 1: Analyze Content**
```python
def analyze_content(content: str, target_keyword: str) -> dict:
    """Analyze content for SEO optimization"""
    
    analysis = {
        'keyword_in_title': target_keyword.lower() in content[:100].lower(),
        'keyword_in_h1': target_keyword.lower() in content.split('\n')[0].lower(),
        'keyword_in_first_100': target_keyword.lower() in content[:100].lower(),
        'keyword_density': calculate_keyword_density(content, target_keyword),
        'word_count': len(content.split()),
        'internal_links': count_internal_links(content),
        'external_links': count_external_links(content)
    }
    
    return analysis
```

**Step 2: Optimize Meta Tags**
```python
def optimize_meta_tags(content: str, target_keyword: str) -> dict:
    """Generate optimized meta title and description"""
    
    # Extract first paragraph for context
    first_para = content.split('\n\n')[0]
    
    # Generate meta title (50-60 chars)
    meta_title = f"{target_keyword.title()}: Complete Guide | ProQSmart"
    if len(meta_title) > 60:
        meta_title = meta_title[:57] + "..."
    
    # Generate meta description (150-160 chars)
    meta_description = f"{first_para[:140]}... Request demo today."
    if len(meta_description) > 160:
        meta_description = meta_description[:157] + "..."
    
    return {
        'metaTitle': meta_title,
        'metaDescription': meta_description
    }
```

**Step 3: Generate JSON-LD Schema**
```python
def generate_jsonld_schema(content: dict, url: str) -> dict:
    """Generate Article schema with all required fields"""
    
    schema = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": content['title'],
        "description": content['metaDescription'],
        "author": {
            "@type": "Organization",
            "name": "ProQSmart"
        },
        "publisher": {
            "@type": "Organization",
            "name": "ProQSmart",
            "logo": {
                "@type": "ImageObject",
                "url": f"{url}/logo.png"
            }
        },
        "datePublished": content.get('publishedAt', datetime.now().isoformat()),
        "image": f"{url}/images/{content['slug']}.jpg",
        "mainEntityOfPage": {
            "@type": "WebPage",
            "@id": f"{url}/blog/{content['slug']}"
        }
    }
    
    return schema
```

### 4.2 Technical SEO Workflow

**Step 1: Generate Sitemap**
```python
def generate_sitemap(pages: list, base_url: str) -> str:
    """Generate XML sitemap"""
    
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    
    for page in pages:
        xml += '  <url>\n'
        xml += f'    <loc>{base_url}{page["slug"]}</loc>\n'
        xml += f'    <lastmod>{page.get("updatedAt", datetime.now().isoformat())}</lastmod>\n'
        xml += f'    <priority>{page.get("priority", "0.8")}</priority>\n'
        xml += '  </url>\n'
    
    xml += '</urlset>'
    
    return xml
```

**Step 2: Configure Robots.txt**
```python
def generate_robots_txt() -> str:
    """Generate robots.txt configuration"""
    
    return """User-agent: *
Allow: /
Disallow: /admin/
Disallow: /api/
Disallow: /private/

Sitemap: https://proqsmart.com/sitemap.xml

# Crawl-delay for polite crawling
Crawl-delay: 1
"""
```

**Step 3: Run Lighthouse Audit**
```python
import subprocess

def run_lighthouse_audit(url: str) -> dict:
    """Run Lighthouse audit for Core Web Vitals"""
    
    cmd = [
        'lighthouse',
        url,
        '--output=json',
        '--output-path=workspace-seo-a/audit-reports/lighthouse-score.json',
        '--quiet'
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    # Parse results
    with open('workspace-seo-a/audit-reports/lighthouse-score.json') as f:
        report = json.load(f)
    
    return {
        'performance': report['categories']['performance']['score'] * 100,
        'accessibility': report['categories']['accessibility']['score'] * 100,
        'seo': report['categories']['seo']['score'] * 100,
        'lcp': report['audits']['largest-contentful-paint']['numericValue'],
        'fid': report['audits']['max-potential-fid']['numericValue'],
        'cls': report['audits']['cumulative-layout-shift']['numericValue']
    }
```

---

## 5. Tools Required

### 5.1 OpenClaw Tools

| Tool | Permission | Purpose |
|------|------------|---------|
| `read` | Allow | Read content drafts |
| `write` | Allow | Write optimized content |
| `edit` | Allow | Edit and refine SEO |
| `web_search` | Allow | Check competitor SEO |
| `web_fetch` | Allow | Fetch competitor pages |
| `exec` | Allow | Run Lighthouse, Python scripts |

### 5.2 External APIs

| API | Purpose | Free Tier | MVP Usage |
|-----|---------|-----------|-----------|
| **DataForSEO** | Keyword rankings | Pay-per-use | 1000 queries/mo |
| **Lighthouse** | Core Web Vitals audit | Open-source (free) | Unlimited |

### 5.3 Python Dependencies

```txt
neo4j                  # Neo4j driver
lighthouse             # Core Web Vitals audit
markdown               # Markdown processing
```

---

## 6. Configuration

### 6.1 Environment Variables

```bash
# DataForSEO
DATAFORSEO_EMAIL=your-email@example.com
DATAFORSEO_PASSWORD=your-password

# Neo4j
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your-password

# OpenClaw
OPENCLAW_WORKSPACE=/root/.openclaw/workspace-seo-a
```

### 6.2 Model Configuration

```json
{
  "model": {
    "primary": "ollama-cloud/minimax-m3",
    "fallbacks": ["ollama-cloud/deepseek-v4-pro"],
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
      "web_search",
      "web_fetch",
      "exec"
    ],
    "deny": [
      "process",
      "canvas",
      "cron"
    ]
  }
}
```

---

## 7. Testing

### 7.1 Unit Tests

**Test: Meta Tag Generation**
```python
def test_meta_generation():
    content = "Article about AI procurement software..."
    keyword = "AI procurement software"
    
    meta = optimize_meta_tags(content, keyword)
    
    assert 50 <= len(meta['metaTitle']) <= 60
    assert 150 <= len(meta['metaDescription']) <= 160
    assert keyword in meta['metaTitle']
```

**Test: Schema Generation**
```python
def test_schema_generation():
    content = {
        'title': 'Test Article',
        'metaDescription': 'Test description',
        'slug': 'test-article'
    }
    
    schema = generate_jsonld_schema(content, 'https://example.com')
    
    assert '@context' in schema
    assert '@type' in schema
    assert schema['@type'] == 'Article'
```

### 7.2 Integration Tests

**Test: Full SEO Workflow**
```python
async def test_full_seo_workflow():
    # 1. Spawn SEO agent
    await sessions_spawn(
        agentId="seo-vertical-a",
        task="Optimize 10 articles for SEO",
        params={
            "contentFiles": ["workspace-vertical-a/drafts/*.md"],
            "targetKeywords": ["AI procurement software"]
        }
    )
    
    # 2. Wait for completion (timeout: 60 minutes)
    await wait_for_completion(timeout=3600)
    
    # 3. Verify outputs
    optimized_dir = "workspace-seo-a/optimized"
    articles = glob(f"{optimized_dir}/*.md")
    assert len(articles) >= 10
    
    # 4. Verify schema files
    schema_dir = "workspace-seo-a/schema"
    schemas = glob(f"{schema_dir}/*.jsonld")
    assert len(schemas) >= 10
    
    # 5. Verify sitemap
    assert os.path.exists("workspace-seo-a/sitemap.xml")
    
    # 6. Verify Linear updated
    task = await linear.getIssue("MAR-128")
    assert task.stateId == "done"
```

### 7.3 Success Criteria

- ✅ All articles have meta titles (50-60 chars)
- ✅ All articles have meta descriptions (150-160 chars)
- ✅ All articles have JSON-LD schema
- ✅ Target keywords in title, H1, first 100 words
- ✅ Sitemap.xml generated with all pages
- ✅ Robots.txt configured correctly
- ✅ Core Web Vitals: All green (LCP <2.5s, FID <100ms, CLS <0.1)
- ✅ Lighthouse SEO score: 100/100
- ✅ SEO completes within 60 minutes for 10 articles

---

## 8. Error Handling

### 8.1 DataForSEO API Failures

**Scenario:** Cannot retrieve ranking data

**Detection:**
```python
try:
    rankings = dataforseo.get_rankings(keywords)
except requests.HTTPError as e:
    logger.error(f"DataForSEO API error: {e}")
    # Use cached rankings instead
    rankings = get_cached_rankings()
```

**Recovery:**
1. Use cached ranking data
2. Retry DataForSEO every 30 minutes
3. Notify human if >2 hours downtime

### 8.2 Lighthouse Audit Failures

**Scenario:** Lighthouse audit times out

**Detection:**
```python
try:
    results = run_lighthouse_audit(url)
except subprocess.TimeoutExpired:
    logger.error(f"Lighthouse audit timeout for {url}")
    # Skip this page, continue with others
    continue
```

**Recovery:**
1. Skip failing page
2. Retry Lighthouse audit
3. Log performance issues

---

## 9. SEO Guidelines

### 9.1 On-Page SEO Checklist

**Title Tags:**
- ✅ 50-60 characters
- ✅ Include target keyword
- ✅ Include brand name
- ✅ Unique for each page

**Meta Descriptions:**
- ✅ 150-160 characters
- ✅ Include target keyword
- ✅ Include CTA
- ✅ Unique for each page

**Content:**
- ✅ Target keyword in H1
- ✅ Target keyword in first 100 words
- ✅ Target keyword in 2-3 H2s
- ✅ Keyword density: 1-2%
- ✅ 2000+ words for pillar content
- ✅ Internal links (3-5 per page)
- ✅ External links to authoritative sources

**Images:**
- ✅ Alt text for all images
- ✅ Descriptive filenames
- ✅ Compressed (WebP format)
- ✅ Lazy loading enabled

### 9.2 Technical SEO Checklist

**Site Structure:**
- ✅ XML sitemap generated
- ✅ Robots.txt configured
- ✅ Canonical URLs set
- ✅ HTTPS enabled
- ✅ Mobile-friendly design

**Performance:**
- ✅ LCP <2.5 seconds
- ✅ FID <100 milliseconds
- ✅ CLS <0.1
- ✅ Page size <2MB
- ✅ Time to First Byte <600ms

**Indexing:**
- ✅ Noindex tags removed
- ✅ No broken links (404s)
- ✅ No redirect chains
- ✅ Structured data implemented

---

## 10. Performance Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| **SEO Velocity** | 10 articles/hour | Articles optimized / Time |
| **Schema Coverage** | 100% | Articles with schema / Total |
| **Meta Tag Compliance** | 100% | Articles with proper meta / Total |
| **Core Web Vitals** | 100% green | Pages passing / Total |
| **Lighthouse SEO** | 100/100 | Average score |
| **SEO Duration** | <60 min for 10 articles | Start to completion time |

---

**Document End**

*Last updated: 2026-07-26*  
*Version: 1.0*  
*Next review: After Phase 5 implementation*
