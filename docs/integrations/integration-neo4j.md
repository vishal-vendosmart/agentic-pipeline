# Integration Specification: Neo4j Knowledge Graph

**Service:** Neo4j Graph Database  
**Purpose:** Store facts, keywords, objectives, competitors  
**Integration Type:** Cypher queries + Python driver  
**Cost:** Self-hosted (free, open-source)  

---

## 1. Overview

Neo4j serves as the Knowledge Graph that prevents hallucinations by storing all verified facts, keywords, objectives, and competitor data. All agents query Neo4j before generating output to ensure fact-grounded content.

---

## 2. Setup

### 2.1 Docker Installation

```bash
docker run -d \
  --name neo4j \
  -p 7474:7474 -p 7687:7687 \
  -v neo4j-data:/data \
  -e NEO4J_AUTH=neo4j/your-secure-password \
  -e NEO4J_PLUGINS=apoc \
  neo4j:5.20-community
```

### 2.2 Access

- **Browser UI:** http://localhost:7474
- **Bolt endpoint:** bolt://localhost:7687
- **Username:** neo4j
- **Password:** your-secure-password

### 2.3 Install Python Driver

```bash
pip install neo4j
```

### 2.4 Configure Environment

```bash
# .env
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your-password
```

---

## 3. Schema

### 3.1 Node Types

```cypher
// Objectives
(:Objective {
  id: "obj-001",
  goal: "Generate 20 leads/month",
  vertical: "A",
  metrics: ["leads_per_month", "conversion_rate"],
  status: "active",
  createdAt: datetime(),
  updatedAt: datetime()
})

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
  id: "fact-001",
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
  contentGaps: ["no ROI calculator", "few case studies"],
  analyzedAt: datetime()
})

// Content
(:Article {
  title: "AI Procurement Software: Complete Guide",
  slug: "ai-procurement-software-guide",
  status: "published",
  targetKeyword: "AI procurement software",
  wordCount: 2450,
  publishedAt: datetime(),
  url: "https://proqsmart.com/blog/ai-procurement-software-guide"
})

// Verticals
(:Vertical {
  id: "A",
  name: "ProQSmart",
  domain: "proqsmart.com"
})
```

### 3.2 Relationships

```cypher
// Objective targets vertical
(:Objective)-[:TARGETS]->(:Vertical {id: "A"})

// Keyword targets vertical
(:Keyword)-[:TARGETS]->(:Vertical {id: "A"})

// Fact related to keyword
(:Fact)-[:RELATED_TO]->(:Keyword {term: "AI procurement software"})

// Competitor competes with vertical
(:Competitor)-[:COMPETES_WITH]->(:Vertical {id: "A"})

// Article ranks for keyword
(:Article)-[:RANKS_FOR]->(:Keyword {term: "AI procurement software"})

// Content belongs to vertical
(:Article)-[:BELONGS_TO]->(:Vertical {id: "A"})
```

### 3.3 Constraints

```cypher
// Ensure unique IDs
CREATE CONSTRAINT objective_id IF NOT EXISTS FOR (o:Objective) REQUIRE o.id IS UNIQUE;
CREATE CONSTRAINT fact_id IF NOT EXISTS FOR (f:Fact) REQUIRE f.id IS UNIQUE;
CREATE CONSTRAINT keyword_term IF NOT EXISTS FOR (k:Keyword) REQUIRE k.term IS UNIQUE;
CREATE CONSTRAINT competitor_domain IF NOT EXISTS FOR (c:Competitor) REQUIRE c.domain IS UNIQUE;
CREATE CONSTRAINT article_slug IF NOT EXISTS FOR (a:Article) REQUIRE a.slug IS UNIQUE;
```

---

## 4. Python Driver

### 4.1 Initialize Connection

```python
from neo4j import GraphDatabase

class Neo4jClient:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
    
    def close(self):
        self.driver.close()
    
    def query(self, cypher: str, params: dict = None):
        with self.driver.session() as session:
            result = session.run(cypher, params or {})
            return [dict(record) for record in result]
    
    def write(self, cypher: str, params: dict = None):
        with self.driver.session() as session:
            result = session.run(cypher, params or {})
            return result.consume()
```

### 4.2 Usage Example

```python
# Initialize
client = Neo4jClient(
    uri='bolt://localhost:7687',
    user='neo4j',
    password='your-password'
)

# Query
keywords = client.query("""
    MATCH (k:Keyword {vertical: "A"})
    WHERE k.opportunity_score >= 80
    RETURN k.term, k.volume, k.difficulty
    ORDER BY k.opportunity_score DESC
    LIMIT 10
""")

# Write
client.write("""
    CREATE (:Keyword {
        term: $term,
        volume: $volume,
        difficulty: $difficulty,
        intent: $intent,
        vertical: $vertical,
        opportunity_score: $score,
        discoveredAt: datetime(),
        source: "DataForSEO"
    })
""", {
    'term': 'AI procurement software',
    'volume': 2400,
    'difficulty': 45,
    'intent': 'commercial',
    'vertical': 'A',
    'score': 92
})

# Close
client.close()
```

---

## 5. Common Queries

### 5.1 Get Objectives

```cypher
// Get active objectives for vertical
MATCH (o:Objective {vertical: "A", status: "active"})
RETURN o.goal, o.metrics, o.createdAt
ORDER BY o.createdAt DESC
```

### 5.2 Get Keywords

```cypher
// Get top keywords by opportunity
MATCH (k:Keyword {vertical: "A"})
WHERE k.opportunity_score >= 80
RETURN k.term, k.volume, k.difficulty, k.intent
ORDER BY k.opportunity_score DESC
LIMIT 20

// Get keywords by intent
MATCH (k:Keyword {vertical: "A", intent: "commercial"})
RETURN k.term, k.volume
ORDER BY k.volume DESC
```

### 5.3 Get Facts

```cypher
// Get verified facts for topic
MATCH (f:Fact)
WHERE ANY(kw IN f.relatedKeywords WHERE kw CONTAINS "procurement")
AND f.verified = true
RETURN f.claim, f.source, f.sourceUrl, f.confidence
ORDER BY f.confidence DESC
LIMIT 10

// Get facts by confidence
MATCH (f:Fact {verified: true})
WHERE f.confidence >= 0.9
RETURN f.claim, f.source
ORDER BY f.confidence DESC
```

### 5.4 Get Competitors

```cypher
// Get competitors for vertical
MATCH (c:Competitor)-[:COMPETES_WITH]->(:Vertical {id: "A"})
RETURN c.name, c.domain, c.estimatedTraffic, c.contentGaps
ORDER BY c.estimatedTraffic DESC

// Get competitor keywords
MATCH (c:Competitor {domain: "procureai.com"})
RETURN c.rankingKeywords
```

### 5.5 Get Content

```cypher
// Get published articles
MATCH (a:Article {vertical: "A", status: "published"})
RETURN a.title, a.slug, a.wordCount, a.publishedAt
ORDER BY a.publishedAt DESC
LIMIT 10

// Get articles by keyword
MATCH (a:Article)-[:RANKS_FOR]->(k:Keyword {term: "AI procurement software"})
RETURN a.title, a.url
```

---

## 6. Write Patterns

### 6.1 Create Objective

```cypher
CREATE (:Objective {
  id: "obj-" + randomUUID(),
  goal: "Generate 20 leads/month",
  vertical: "A",
  metrics: ["leads_per_month", "conversion_rate"],
  status: "active",
  createdAt: datetime(),
  updatedAt: datetime()
})
```

### 6.2 Create Keyword

```cypher
CREATE (:Keyword {
  id: "kw-" + randomUUID(),
  term: "AI procurement software",
  volume: 2400,
  difficulty: 45,
  intent: "commercial",
  vertical: "A",
  opportunity_score: 92,
  discoveredAt: datetime(),
  source: "DataForSEO"
})
```

### 6.3 Create Fact

```cypher
CREATE (:Fact {
  id: "fact-" + randomUUID(),
  claim: "73% of SMEs plan AI adoption in 2026",
  source: "Manufacturing Tech Survey 2026",
  sourceUrl: "https://example.com/survey.pdf",
  confidence: 0.95,
  verified: true,
  relatedKeywords: ["AI adoption", "manufacturing SMEs"],
  verifiedAt: datetime()
})
```

### 6.4 Create Competitor

```cypher
MATCH (v:Vertical {id: "A"})
CREATE (c:Competitor {
  id: "comp-" + randomUUID(),
  name: "ProcureAI",
  domain: "procureai.com",
  rankingKeywords: ["AI procurement", "smart purchasing"],
  estimatedTraffic: 50000,
  contentGaps: ["no ROI calculator", "few case studies"],
  analyzedAt: datetime()
})-[:COMPETES_WITH]->(v)
```

### 6.5 Create Article

```cypher
MATCH (v:Vertical {id: "A"})
CREATE (a:Article {
  id: "art-" + randomUUID(),
  title: "AI Procurement Software: Complete Guide",
  slug: "ai-procurement-software-guide",
  status: "published",
  targetKeyword: "AI procurement software",
  wordCount: 2450,
  publishedAt: datetime(),
  url: "https://proqsmart.com/blog/ai-procurement-software-guide"
})-[:BELONGS_TO]->(v)
```

---

## 7. Backup Strategy

### 7.1 Daily Dumps

```bash
#!/bin/bash
# /root/scripts/backup-neo4j.sh

BACKUP_DIR="/backups/neo4j"
DATE=$(date +%Y-%m-%d)

docker exec neo4j neo4j-admin dump \
  --to-path=/backups \
  --database=neo4j

mv /var/lib/neo4j/data/dumps/neo4j.dump $BACKUP_DIR/neo4j-$DATE.dump

# Keep only last 7 days
find $BACKUP_DIR -name "neo4j-*.dump" -mtime +7 -delete
```

### 7.2 Restore from Backup

```bash
# Stop Neo4j
docker stop neo4j

# Restore
docker run --rm \
  -v neo4j-data:/data \
  -v /backups/neo4j:/backups \
  neo4j:5.20-community \
  neo4j-admin load \
    --from-path=/backups \
    --database=neo4j \
    --force

# Start Neo4j
docker start neo4j
```

---

## 8. Performance Optimization

### 8.1 Indexes

```cypher
// Create indexes for common queries
CREATE INDEX keyword_vertical IF NOT EXISTS FOR (k:Keyword) ON (k.vertical);
CREATE INDEX keyword_opportunity IF NOT EXISTS FOR (k:Keyword) ON (k.opportunity_score);
CREATE INDEX fact_verified IF NOT EXISTS FOR (f:Fact) ON (f.verified);
CREATE INDEX fact_keywords IF NOT EXISTS FOR (f:Fact) ON (f.relatedKeywords);
CREATE INDEX article_vertical IF NOT EXISTS FOR (a:Article) ON (a.vertical);
CREATE INDEX article_status IF NOT EXISTS FOR (a:Article) ON (a.status);
```

### 8.2 Query Optimization

**Good:**
```cypher
// Use indexes
MATCH (k:Keyword {vertical: "A"})
WHERE k.opportunity_score >= 80
RETURN k.term, k.volume
```

**Bad:**
```cypher
// No index usage
MATCH (k:Keyword)
WHERE k.vertical = "A" AND k.opportunity_score >= 80
RETURN k.term, k.volume
```

---

## 9. Testing

### 9.1 Unit Tests

```python
def test_create_keyword():
    client = Neo4jClient(URI, USER, PASSWORD)
    
    client.write("""
        CREATE (:Keyword {
            term: "test keyword",
            volume: 1000,
            vertical: "A"
        })
    """)
    
    result = client.query("""
        MATCH (k:Keyword {term: "test keyword"})
        RETURN k
    """)
    
    assert len(result) == 1
    assert result[0]['k']['volume'] == 1000
```

### 9.2 Integration Tests

```python
def test_full_workflow():
    # 1. Create objective
    client.write("CREATE (:Objective {goal: 'Test', vertical: 'A'})")
    
    # 2. Query objective
    objectives = client.query("MATCH (o:Objective) RETURN o")
    assert len(objectives) > 0
    
    # 3. Create keyword
    client.write("CREATE (:Keyword {term: 'test', vertical: 'A'})")
    
    # 4. Verify relationship
    client.write("""
        MATCH (o:Objective {goal: 'Test'}), (k:Keyword {term: 'test'})
        CREATE (o)-[:TARGETS]->(k)
    """)
    
    relationships = client.query("""
        MATCH (o:Objective)-[r:TARGETS]->(k:Keyword)
        RETURN type(r)
    """)
    assert len(relationships) > 0
```

---

## 10. Cost

| Component | Cost | Notes |
|-----------|------|-------|
| **Neo4j Community** | $0 | Open-source, self-hosted |
| **Docker** | $0 | Included in Hetzner server |
| **Storage** | $0 | 160GB NVMe included |
| **Backup Storage** | $0 | Included |

**Total Monthly Cost:** $0

---

**Document End**

*Last updated: 2026-07-26*  
*Version: 1.0*
