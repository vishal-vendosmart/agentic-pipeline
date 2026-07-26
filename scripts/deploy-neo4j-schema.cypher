// =============================================================================
// Agentic Pipeline - Neo4j Knowledge Graph Schema
// Version: 1.1 - Fixed index/constraint order
// =============================================================================

// -----------------------------------------------------------------------------
// 1. Drop existing indexes/constraints if they exist (for idempotency)
// -----------------------------------------------------------------------------

DROP INDEX keyword_term IF EXISTS;
DROP INDEX keyword_vertical IF EXISTS;
DROP INDEX fact_id IF EXISTS;
DROP INDEX competitor_name IF EXISTS;
DROP INDEX article_slug IF EXISTS;
DROP INDEX objective_id IF EXISTS;

DROP CONSTRAINT keyword_unique IF EXISTS;
DROP CONSTRAINT fact_unique IF EXISTS;
DROP CONSTRAINT article_unique IF EXISTS;

// -----------------------------------------------------------------------------
// 2. Create Constraints FIRST (they create indexes automatically)
// -----------------------------------------------------------------------------

CREATE CONSTRAINT keyword_unique FOR (k:Keyword) REQUIRE k.term IS UNIQUE;
CREATE CONSTRAINT fact_unique FOR (f:Fact) REQUIRE f.id IS UNIQUE;
CREATE CONSTRAINT article_unique FOR (a:Article) REQUIRE a.slug IS UNIQUE;

// -----------------------------------------------------------------------------
// 3. Create Additional Indexes
// -----------------------------------------------------------------------------

CREATE INDEX keyword_vertical FOR (k:Keyword) ON (k.vertical);
CREATE INDEX fact_confidence FOR (f:Fact) ON (f.confidence);
CREATE INDEX competitor_name FOR (c:Competitor) ON (c.name);
CREATE INDEX article_slug FOR (a:Article) ON (a.slug);

// -----------------------------------------------------------------------------
// 4. Create Root Node (Vertical A - ProQSmart)
// -----------------------------------------------------------------------------

MERGE (v:Vertical {id: 'A', name: 'ProQSmart'})
ON CREATE SET v.createdAt = datetime(),
              v.description = 'AI procurement software for manufacturing SMEs';

// -----------------------------------------------------------------------------
// 5. Create Sample Keywords (for testing)
// -----------------------------------------------------------------------------

MERGE (k1:Keyword {term: 'AI procurement software', vertical: 'A'})
ON CREATE SET k1.volume = 2400,
              k1.difficulty = 45,
              k1.intent = 'commercial',
              k1.createdAt = datetime();

MERGE (k2:Keyword {term: 'manufacturing automation', vertical: 'A'})
ON CREATE SET k2.volume = 1900,
              k2.difficulty = 52,
              k2.intent = 'informational',
              k2.createdAt = datetime();

MERGE (k3:Keyword {term: 'procurement automation software', vertical: 'A'})
ON CREATE SET k3.volume = 880,
              k3.difficulty = 38,
              k3.intent = 'commercial',
              k3.createdAt = datetime();

MERGE (k4:Keyword {term: 'AI purchasing system', vertical: 'A'})
ON CREATE SET k4.volume = 590,
              k4.difficulty = 42,
              k4.intent = 'commercial',
              k4.createdAt = datetime();

MERGE (k5:Keyword {term: 'smart procurement tools', vertical: 'A'})
ON CREATE SET k5.volume = 720,
              k5.difficulty = 35,
              k5.intent = 'commercial',
              k5.createdAt = datetime();

// -----------------------------------------------------------------------------
// 6. Create Sample Facts (verified information)
// -----------------------------------------------------------------------------

MERGE (f1:Fact {id: 'fact-001'})
ON CREATE SET f1.claim = 'AI procurement software reduces costs by 30%',
              f1.source = 'McKinsey Report 2025',
              f1.confidence = 0.95,
              f1.verified = true,
              f1.vertical = 'A',
              f1.createdAt = datetime();

MERGE (f2:Fact {id: 'fact-002'})
ON CREATE SET f2.claim = 'Manufacturing SMEs spend 15% of revenue on procurement',
              f2.source = 'Deloitte Manufacturing Survey 2025',
              f2.confidence = 0.92,
              f2.verified = true,
              f2.vertical = 'A',
              f2.createdAt = datetime();

MERGE (f3:Fact {id: 'fact-003'})
ON CREATE SET f3.claim = 'AI-powered procurement reduces processing time by 60%',
              f3.source = 'Gartner Procurement Trends 2025',
              f3.confidence = 0.89,
              f3.verified = true,
              f3.vertical = 'A',
              f3.createdAt = datetime();

// -----------------------------------------------------------------------------
// 7. Create Sample Competitors
// -----------------------------------------------------------------------------

MERGE (c1:Competitor {name: 'Coupa', vertical: 'A'})
ON CREATE SET c1.url = 'https://coupa.com',
              c1.strengths = ['Enterprise features', 'Large customer base'],
              c1.weaknesses = ['Expensive for SMEs', 'Complex setup'],
              c1.contentGaps = ['No AI-focused content', 'Limited manufacturing use cases'],
              c1.createdAt = datetime();

MERGE (c2:Competitor {name: 'Jaggaar', vertical: 'A'})
ON CREATE SET c2.url = 'https://jaggaar.com',
              c2.strengths = ['SME-focused', 'Affordable pricing'],
              c2.weaknesses = ['Limited AI features', 'Smaller brand'],
              c2.contentGaps = ['No ROI calculators', 'Few case studies'],
              c2.createdAt = datetime();

MERGE (c3:Competitor {name: 'Procol', vertical: 'A'})
ON CREATE SET c3.url = 'https://procol.io',
              c3.strengths = ['Indian market focus', 'Good UX'],
              c3.weaknesses = ['Limited global presence', 'Basic analytics'],
              c3.contentGaps = ['No AI thought leadership', 'Limited technical content'],
              c3.createdAt = datetime();

// -----------------------------------------------------------------------------
// 8. Create Sample Objective
// -----------------------------------------------------------------------------

MERGE (o:Objective {id: 'obj-001'})
ON CREATE SET o.title = 'Generate 20 leads/month from manufacturing SMEs',
              o.vertical = 'A',
              o.metric = 'leads_per_month',
              o.target = 20,
              o.current = 0,
              o.status = 'in-progress',
              o.createdAt = datetime();

// -----------------------------------------------------------------------------
// 9. Create Relationships
// -----------------------------------------------------------------------------

// Keywords relate to each other
MATCH (k1:Keyword {term: 'AI procurement software'}), (k2:Keyword {term: 'procurement automation software'})
MERGE (k1)-[:RELATES_TO {strength: 0.85}]->(k2);

MATCH (k1:Keyword {term: 'AI procurement software'}), (k3:Keyword {term: 'AI purchasing system'})
MERGE (k1)-[:RELATES_TO {strength: 0.75}]->(k3);

// Facts verify keywords
MATCH (f:Fact {id: 'fact-001'}), (k:Keyword {term: 'AI procurement software'})
MERGE (f)-[:VERIFIES]->(k);

MATCH (f:Fact {id: 'fact-003'}), (k:Keyword {term: 'manufacturing automation'})
MERGE (f)-[:VERIFIES]->(k);

// Competitors compete with vertical
MATCH (c:Competitor {vertical: 'A'}), (v:Vertical {id: 'A'})
MERGE (c)-[:COMPETES_WITH]->(v);

// Objective for vertical
MATCH (o:Objective {id: 'obj-001'}), (v:Vertical {id: 'A'})
MERGE (o)-[:BELONGS_TO]->(v);

// -----------------------------------------------------------------------------
// 10. Verification Queries
// -----------------------------------------------------------------------------

// Count all nodes by type
MATCH (n) RETURN labels(n)[0] as type, count(*) as count ORDER BY count DESC;

// Verify relationships
MATCH ()-[r]->() RETURN type(r) as relationship, count(*) as count ORDER BY count DESC;

// Test query: Get keywords with verified facts
MATCH (k:Keyword)-[:VERIFIES]-(f:Fact)
WHERE k.vertical = 'A' AND f.verified = true
RETURN k.term, k.volume, f.claim, f.confidence
ORDER BY k.volume DESC
LIMIT 10;

