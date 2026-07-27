# Agent Specification: Researcher (ProQSmart)

> **⚠ AMENDED 2026-07-27 — Real agent installation.**
> This agent is installed as a **real OpenClaw agent** in the isolated PM profile:
> registered in `/root/.openclaw-pm/openclaw.json` (`agents.list`), own workspace
> (`/root/.openclaw-pm/workspace-researcher-a`), own agentDir
> (`/root/.openclaw-pm/agents/researcher-a/agent/`). PM spawns it via
> `sessions_spawn`. The deterministic Python helper in `utilities/researcher-vertical-a/`
> is an exec utility it may call — it is NOT the agent itself.
> See architecture-spec.md §6.4 (Agent Installation Standard).
**ID:** `researcher-a`  
**Role:** Industry Research + Keyword Discovery  
**Vertical:** ProQSmart (Vertical A)  
**Primary Model:** `ollama-cloud/minimax-m3`  
**Workspace:** `/root/.openclaw-pm/workspace-vertical-a/research/`

---

## 1. Purpose

Autonomously discover keywords, industry trends, competitor strategies, and content opportunities for ProQSmart. All discoveries are stored in Neo4j Knowledge Graph with verified sources to prevent hallucinations.

---

## 2. Inputs

### 2.1 From Project Manager

**Format:** `sessions_spawn` task

**Example:**
```json
{
  "task": "Research manufacturing AI keywords",
  "params": {
    "objective": "Generate 20 leads/month from manufacturing SMEs",
    "vertical": "A",
    "linearTaskId": "MAR-124",
    "focusAreas": ["procurement automation", "AI in manufacturing", "SME tools"]
  }
}
```

### 2.2 From Knowledge Graph

**Format:** Neo4j Cypher queries

**Queries:**
```cypher
// Get existing objectives
MATCH (o:Objective {vertical: "A"})
RETURN o.goal, o.target_audience

// Get existing keywords (avoid duplicates)
MATCH (k:Keyword {vertical: "A"})
RETURN k.term, k.volume

// Get competitor info
MATCH (c:Competitor)-[:COMPETES_WITH]->(:Vertical {id: "A"})
RETURN c.name, c.domain
```

---

## 3. Outputs

### 3.1 To Workspace

**Files Created:**
- `/root/.openclaw-pm/workspace-vertical-a/research/keyword-strategy.json`
- `/root/.openclaw-pm/workspace-vertical-a/research/competitor-analysis.md`
- `/root/.openclaw-pm/workspace-vertical-a/research/industry-trends.md`

**Example - keyword-strategy.json:**
```json
{
  "primaryKeywords": [
    {
      "term": "AI procurement software",
      "volume": 2400,
      "difficulty": 45,
      "intent": "commercial",
      "cpc": 12.50,
      "opportunity_score": 92,
      "source": "DataForSEO 2026-07-26"
    }
  ],
  "longTailKeywords": [
    {
      "term": "procurement automation for SMEs",
      "volume": 590,
      "difficulty": 28,
      "intent": "commercial"
    }
  ],
  "contentGaps": [
    "No ROI calculators in top 10 results",
    "Few case studies with real numbers"
  ]
}
```

### 3.2 To Knowledge Graph

**Cypher Writes:**
```cypher
// Write keywords
CREATE (:Keyword {
  term: "AI procurement software",
  volume: 2400,
  difficulty: 45,
  intent: "commercial",
  vertical: "A",
  discoveredAt: datetime(),
  source: "DataForSEO"
})

// Write facts
CREATE (:Fact {
  claim: "73% of manufacturing SMEs plan to adopt AI in 2026",
  source: "Manufacturing Tech Survey 2026",
  sourceUrl: "https://example.com/survey-2026.pdf",
  confidence: 0.95,
  verified: true,
  relatedKeywords: ["AI adoption", "manufacturing SMEs"],
  verifiedAt: datetime()
})

// Write competitors
CREATE (:Competitor {
  name: "ProcureAI",
  domain: "procureai.com",
  rankingKeywords: ["AI procurement", "smart purchasing"],
  estimatedTraffic: 50000,
  contentGaps: ["no ROI calculator", "few case studies"]
})
```

### 3.3 To Linear

**Updates:**
```graphql
mutation {
  updateIssue(
    id: "MAR-124"
    input: {
      description: """
      ✅ Research Complete
      
      **Keywords Discovered:** 50
      - Primary: 10 (avg volume: 2,100/mo)
      - Long-tail: 40 (avg volume: 650/mo)
      
      **Competitors Analyzed:** 5
      - Top competitor: ProcureAI (50k monthly visitors)
      - Content gap: No ROI calculators
      
      **Key Insight:** 73% of SMEs plan AI adoption in 2026
      
      **Next:** Writer agent can start creating content
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

### 4.1 Keyword Discovery Workflow

**Step 1: Query DataForSEO**
```python
from dataforseo_client import DataForSEOClient

client = DataForSEOClient(email, password)

# Get keyword ideas
keywords = client.post(
    '/v3/dataforseo_labs/google/keyword_ideas',
    [{
        "location_name": "India",
        "language_name": "English",
        "keywords": ["AI procurement", "manufacturing automation", "SME tools"]
    }]
)

# Parse results
for kw in keywords['tasks'][0]['result']:
    keyword_data = {
        'term': kw['keyword'],
        'volume': kw['search_volume'],
        'difficulty': kw['competition_level'],
        'cpc': kw['cpc']
    }
```

**Step 2: Query SerpAPI for SERP Analysis**
```python
import serpapi

client = serpapi.Client(api_key)

for keyword in top_keywords:
    results = client.search(
        engine="google",
        q=keyword,
        location="India",
        hl="en"
    )
    
    # Analyze top 10 results
    competitors = []
    for result in results['organic_results'][:10]:
        competitors.append({
            'domain': result['domain'],
            'title': result['title'],
            'position': result['position']
        })
```

**Step 3: Calculate Opportunity Scores**
```python
def calculate_opportunity_score(keyword_data):
    volume = keyword_data['volume']
    difficulty = keyword_data['difficulty']
    cpc = keyword_data.get('cpc', 0)
    
    # Higher volume, lower difficulty, higher CPC = better opportunity
    score = (volume * 0.5) + ((100 - difficulty) * 0.3) + (cpc * 2)
    return min(100, score)  # Cap at 100

for kw in keywords:
    kw['opportunity_score'] = calculate_opportunity_score(kw)
```

**Step 4: Write to Neo4j**
```python
from neo4j import GraphDatabase

driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

with driver.session() as session:
    for kw in keywords:
        session.run("""
            CREATE (k:Keyword {
                term: $term,
                volume: $volume,
                difficulty: $difficulty,
                intent: $intent,
                vertical: $vertical,
                opportunity_score: $score,
                discoveredAt: datetime(),
                source: "DataForSEO"
            })
        """, **kw)
```

### 4.2 Competitor Analysis Workflow

**Step 1: Identify Competitors**
```python
# Search for top ranking domains
competitor_domains = set()

for keyword in primary_keywords:
    serp_results = serpapi.search(q=keyword, location="India")
    for result in serp_results.get('organic_results', [])[:10]:
        competitor_domains.add(result['domain'])

# Remove own domains
competitor_domains.discard('proqsmart.com')
competitor_domains.discard('proqsmart.app')
```

**Step 2: Analyze Each Competitor**
```python
for domain in competitor_domains:
    # Get domain overview from DataForSEO
    overview = dataforseo.get('/v3/dataforseo_labs/google/domain_rank_overview', {
        "target": domain,
        "location_name": "India"
    })
    
    # Get top keywords
    keywords = dataforseo.get('/v3/dataforseo_labs/google/ranked_keywords', {
        "target": domain,
        "location_name": "India"
    })
    
    # Identify content gaps
    gap_analysis = analyze_gaps(overview, keywords)
```

**Step 3: Store in KG**
```cypher
MATCH (v:Vertical {id: "A"})
CREATE (c:Competitor {
    name: "ProcureAI",
    domain: "procureai.com",
    rankingKeywords: ["AI procurement", "smart purchasing"],
    estimatedTraffic: 50000,
    contentGaps: ["no ROI calculator", "few case studies"],
    analyzedAt: datetime()
})-[:COMPETES_WITH]->(v)
```

### 4.3 Fact Discovery Workflow

**Step 1: Web Search for Industry Stats**
```python
from openclaw_tools import web_search, web_fetch

# Search for industry statistics
search_results = web_search("manufacturing SME AI adoption statistics 2026")

# Fetch top sources
for result in search_results[:10]:
    content = web_fetch(result['url'])
    
    # Extract statistics
    stats = extract_statistics(content)
    
    # Verify and store
    for stat in stats:
        if verify_source(stat['source']):
            write_to_neo4j(stat)
```

**Step 2: Verify Sources**
```python
def verify_source(source_url):
    # Check domain authority
    # Check publication date (must be <2 years old)
    # Check for peer review or industry recognition
    
    trusted_domains = [
        'mckinsey.com', 'gartner.com', 'forrester.com',
        'manufacturing.net', 'sme.org'
    ]
    
    domain = urlparse(source_url).netloc
    return any(trusted in domain for trusted in trusted_domains)
```

---

## 5. Tools Required

### 5.1 OpenClaw Tools

| Tool | Permission | Purpose |
|------|------------|---------|
| `web_search` | Allow | Search for industry trends |
| `web_fetch` | Allow | Fetch web pages for analysis |
| `browser-automation` | Allow | Complex web scraping |
| `read` | Allow | Read workspace files |
| `write` | Allow | Write research outputs |
| `edit` | Allow | Update research files |
| `exec` | Allow | Run Python scripts for APIs |

### 5.2 External APIs

| API | Purpose | Free Tier | MVP Usage |
|-----|---------|-----------|-----------|
| **DataForSEO** | Keyword volumes, difficulty, CPC | Pay-per-use (~$0.50/1000) | 5000 queries/mo |
| **SerpAPI** | SERP analysis, competitor tracking | 100 searches/mo | 100 searches/mo |
| **Neo4j** | Store keywords, facts, competitors | Self-hosted (free) | Unlimited |

### 5.3 Python Dependencies

```txt
dataforseo-client      # DataForSEO API
serpapi                # SerpAPI client
neo4j                  # Neo4j driver
python-dateutil        # Date parsing
beautifulsoup4         # HTML parsing
requests               # HTTP requests
```

---

## 6. Configuration

### 6.1 Environment Variables

```bash
# DataForSEO
DATAFORSEO_EMAIL=your-email@example.com
DATAFORSEO_PASSWORD=your-password

# SerpAPI
SERPAPI_KEY=your-api-key

# Neo4j
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your-password

# OpenClaw
OPENCLAW_WORKSPACE=/root/.openclaw-pm/workspace-vertical-a
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
      "web_search",
      "web_fetch",
      "browser-automation",
      "read",
      "write",
      "edit",
      "exec"
    ],
    "deny": [
      "process",
      "canvas",
      "cron",
      "github"
    ]
  }
}
```

---

## 7. Testing

### 7.1 Unit Tests

**Test: Keyword Discovery**
```python
def test_keyword_discovery():
    keywords = researcher.discover_keywords("AI procurement")
    assert len(keywords) >= 10
    assert all('volume' in kw for kw in keywords)
    assert all('difficulty' in kw for kw in keywords)
```

**Test: Opportunity Score Calculation**
```python
def test_opportunity_score():
    kw = {'volume': 2400, 'difficulty': 45, 'cpc': 12.50}
    score = calculate_opportunity_score(kw)
    assert 0 <= score <= 100
    assert score > 50  # High volume, moderate difficulty
```

### 7.2 Integration Tests

**Test: Full Research Workflow**
```python
async def test_full_research():
    # 1. Spawn researcher
    await sessions_spawn(
        agentId="researcher-a",
        task="Research manufacturing AI keywords"
    )
    
    # 2. Wait for completion (timeout: 30 minutes)
    await wait_for_completion(timeout=1800)
    
    # 3. Verify outputs
    assert os.path.exists("workspace-vertical-a/research/keyword-strategy.json")
    
    # 4. Verify KG populated
    driver = neo4j.GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    with driver.session() as session:
        result = session.run("MATCH (k:Keyword) RETURN count(k) as count")
        count = result.single()["count"]
        assert count >= 50
```

### 7.3 Success Criteria

- ✅ Discovers 50+ keywords per research session
- ✅ All keywords include volume + difficulty scores
- ✅ All facts have verified sources
- ✅ Zero hallucinated statistics
- ✅ Competitor analysis includes 5+ competitors
- ✅ Research completes within 30 minutes
- ✅ Linear task updated with summary

---

## 8. Error Handling

### 8.1 API Rate Limits

**Scenario:** DataForSEO or SerpAPI rate limit exceeded

**Detection:**
```python
try:
    response = dataforseo.post(endpoint, params)
except RateLimitError as e:
    logger.warning(f"Rate limit exceeded: {e}")
    # Wait and retry
    time.sleep(60)
    response = dataforseo.post(endpoint, params)
```

**Recovery:**
1. Implement exponential backoff (60s, 120s, 240s)
2. Queue remaining keywords for later
3. Update Linear task with progress

### 8.2 Neo4j Connection Failures

**Scenario:** Cannot connect to Neo4j

**Detection:**
```python
try:
    driver = GraphDatabase.driver(NEO4J_URI, auth=(...))
except ServiceUnavailable as e:
    logger.error(f"Neo4j unavailable: {e}")
    # Save to JSON file instead
    save_to_json(keywords)
```

**Recovery:**
1. Save outputs to JSON files
2. Retry Neo4j connection every 5 minutes
3. Notify human if >30 minutes downtime

### 8.3 Invalid Source Detection

**Scenario:** Unreliable source detected

**Detection:**
```python
if not verify_source(url):
    logger.warning(f"Unreliable source: {url}")
    # Skip this source
    continue
```

**Recovery:**
1. Skip unreliable sources
2. Search for alternative sources
3. Flag as "unverified" in KG if must include

---

## 9. Knowledge Graph Schema

### 9.1 Node Types

```cypher
// Keywords
(:Keyword {
  term: "AI procurement software",
  volume: 2400,
  difficulty: 45,
  intent: "commercial",
  vertical: "A",
  opportunity_score: 92,
  discoveredAt: datetime(),
  source: "DataForSEO"
})

// Facts
(:Fact {
  claim: "73% of SMEs plan AI adoption in 2026",
  source: "Manufacturing Tech Survey 2026",
  sourceUrl: "https://example.com/survey.pdf",
  confidence: 0.95,
  verified: true,
  relatedKeywords: ["AI adoption", "manufacturing SMEs"],
  verifiedAt: datetime()
})

// Competitors
(:Competitor {
  name: "ProcureAI",
  domain: "procureai.com",
  rankingKeywords: ["AI procurement", "smart purchasing"],
  estimatedTraffic: 50000,
  contentGaps: ["no ROI calculator"],
  analyzedAt: datetime()
})

// Objectives
(:Objective {
  goal: "Generate 20 leads/month",
  vertical: "A",
  status: "active",
  createdAt: datetime()
})
```

### 9.2 Relationships

```cypher
// Keyword targets vertical
(:Keyword)-[:TARGETS]->(:Vertical {id: "A"})

// Fact related to keyword
(:Fact)-[:RELATED_TO]->(:Keyword)

// Competitor competes with vertical
(:Competitor)-[:COMPETES_WITH]->(:Vertical)

// Objective targets vertical
(:Objective)-[:TARGETS]->(:Vertical)
```

### 9.3 Common Queries

```cypher
// Get top keywords by opportunity
MATCH (k:Keyword {vertical: "A"})
WHERE k.opportunity_score >= 80
RETURN k.term, k.volume, k.difficulty, k.opportunity_score
ORDER BY k.opportunity_score DESC
LIMIT 10

// Get verified facts for topic
MATCH (f:Fact)
WHERE ANY(kw IN f.relatedKeywords WHERE kw CONTAINS "procurement")
AND f.verified = true
RETURN f.claim, f.source, f.confidence
ORDER BY f.confidence DESC

// Get competitor gaps
MATCH (c:Competitor)-[:COMPETES_WITH]->(:Vertical {id: "A"})
RETURN c.name, c.contentGaps
```

---

## 10. Performance Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| **Keywords Discovered** | 50+ per session | Count of :Keyword nodes created |
| **Research Completeness** | 100% | All focus areas covered |
| **Fact Verification Rate** | 100% | Verified facts / Total facts |
| **API Success Rate** | 99%+ | Successful API calls / Total calls |
| **Research Duration** | <30 minutes | Start to completion time |
| **Linear Update Accuracy** | 100% | Updates reflect actual progress |

---

**Document End**

*Last updated: 2026-07-26*  
*Version: 1.0*  
*Next review: After Phase 2 implementation*
